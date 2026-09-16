# -*- coding: utf-8 -*-
"""
数据清洗模块
处理三平台原始数据的格式不统一问题，包括：
1. 价格去除¥符号和逗号
2. 销量将"1.2万"转为数字
3. 品牌从标题中提取
4. 统一字段名并去重
"""
import pandas as pd
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import RAW_DATA_PATH, CLEANED_DATA_PATH

# 品牌列表（按名称长度降序排列，优先匹配长名称）
BRAND_LIST = sorted([
    "Apple", "华为", "小米", "红米", "OPPO", "vivo", "荣耀",
    "三星", "一加", "iQOO", "Realme", "魅族", "努比亚",
    "中兴", "联想", "摩托罗拉", "索尼", "华硕", "ROG", "Nothing", "谷歌",
], key=len, reverse=True)


def extract_brand(title):
    """从商品标题中匹配品牌名称"""
    for b in BRAND_LIST:
        if b.lower() in str(title).lower():
            return b
    return ""


def clean_price(val):
    """清洗价格字段：去除¥符号、逗号，支持万字"""
    if pd.isna(val):
        return 0.0
    val = str(val)
    val = re.sub(r"[¥￥$,元]", "", val).strip()
    if "万" in val:
        return float(val.replace("万", "")) * 10000
    try:
        return float(val)
    except:
        return 0.0


def clean_sales(val):
    """清洗销量字段：去除中文后缀，支持万/亿单位"""
    if pd.isna(val):
        return 0
    val = str(val)
    val = re.sub(r"[已售+件条]", "", val).strip()
    if "万" in val:
        return int(float(val.replace("万", "")) * 10000)
    if "亿" in val:
        return int(float(val.replace("亿", "")) * 100000000)
    try:
        return int(float(val))
    except:
        return 0


def clean_platform(df, platform_name):
    """
    统一每个平台的字段名和数据格式
    标准化为9个字段：平台名称、商品标题、品牌、价格、原价、销量、店铺名称、是否官方旗舰店、商品链接
    """
    df = df.copy()
    df["平台名称"] = platform_name
    if "标题" in df.columns:
        df.rename(columns={"标题": "商品标题"}, inplace=True)

    df["价格"] = df["价格"].apply(clean_price)
    if "原价" in df.columns:
        df["原价"] = df["原价"].apply(clean_price)
    else:
        df["原价"] = df["价格"]
    df["销量"] = df["销量"].apply(clean_sales)

    # 品牌字段为空时从标题提取
    if "品牌" not in df.columns or df["品牌"].isna().all():
        df["品牌"] = ""
    df["品牌"] = df["品牌"].fillna("").astype(str)
    mask = df["品牌"].str.strip().eq("")
    df.loc[mask, "品牌"] = df.loc[mask, "商品标题"].apply(extract_brand)

    if "是否官方旗舰店" not in df.columns:
        df["是否官方旗舰店"] = 0
    df["是否官方旗舰店"] = df["是否官方旗舰店"].fillna(0).astype(int)

    # 确保所有标准列都存在
    cols = ["平台名称", "商品标题", "品牌", "价格", "原价", "销量", "店铺名称", "是否官方旗舰店", "商品链接"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]


def load_raw_data():
    """加载data/raw/目录下的所有原始CSV文件，清洗后合并"""
    frames = []
    for fname in os.listdir(RAW_DATA_PATH):
        if fname.endswith(".csv"):
            path = os.path.join(RAW_DATA_PATH, fname)
            df = pd.read_csv(path, encoding="utf-8-sig")
            # 从文件名识别平台（jd_raw.csv -> 京东）
            platform = fname.replace("_raw.csv", "")
            platform_map = {"jd": "京东", "taobao": "淘宝", "douyin": "抖音"}
            platform_name = platform_map.get(platform, platform)
            df = clean_platform(df, platform_name)
            frames.append(df)
            print(f"  已加载: {fname} ({len(df)}条)")
    if not frames:
        raise FileNotFoundError(f"未找到原始数据，请先运行爬虫获取数据 ({RAW_DATA_PATH})")

    df = pd.concat(frames, ignore_index=True)
    df = df[df["价格"] > 0]
    df = df.drop_duplicates(subset=["商品标题", "品牌", "平台名称"], keep="first")
    df = df.reset_index(drop=True)
    return df


def run():
    """执行完整清洗流程：加载 → 清理 → 去重 → 保存"""
    print("=" * 50)
    print("数据清洗")
    print("=" * 50)
    df = load_raw_data()
    print(f"\n清洗前: {len(df)} 条数据")
    df = df[df["价格"] > 0]
    df["品牌"] = df["品牌"].fillna("")
    df["店铺名称"] = df["店铺名称"].fillna("")
    df["商品标题"] = df["商品标题"].fillna("")
    df = df.reset_index(drop=True)
    print(f"清洗后: {len(df)} 条数据")

    path = os.path.join(CLEANED_DATA_PATH, "all_phones_clean.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"已保存至: {path}")
    print(f"\n各平台数据量:")
    print(df["平台名称"].value_counts().to_string())
    return df


if __name__ == "__main__":
    df = run()
    print(df.head())
