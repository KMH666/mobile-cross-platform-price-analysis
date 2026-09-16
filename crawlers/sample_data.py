# -*- coding: utf-8 -*-
"""
样本数据生成器
当爬虫无法获取数据时，使用程序化方式生成逼真的样本来保证分析流程正常运行。
价格设定参考真实市场行情，各平台定价策略有所不同（京东=基准，淘宝=约93%，抖音=约88%+券后价）。
"""
import random
import pandas as pd
import numpy as np

# 固定随机种子，保证每次生成的样本数据一致
random.seed(42)
np.random.seed(42)

# ========== 品牌字典 ==========
# 每个品牌包含：价格区间(元)、可能的店铺名称列表
BRANDS = {
    "Apple": {"price_base": (3000, 12000), "shop_names": ["Apple产品京东自营旗舰店", "Apple官方旗舰店", "Apple产品专营店"]},
    "华为": {"price_base": (1500, 8000), "shop_names": ["华为京东自营旗舰店", "华为官方旗舰店", "华为手机专卖店"]},
    "小米": {"price_base": (800, 5000), "shop_names": ["小米京东自营旗舰店", "小米官方旗舰店", "小米专卖店"]},
    "红米": {"price_base": (400, 2500), "shop_names": ["红米京东自营旗舰店", "红米官方旗舰店", "红米手机专卖店"]},
    "OPPO": {"price_base": (1000, 5000), "shop_names": ["OPPO京东自营旗舰店", "OPPO官方旗舰店", "OPPO手机专卖店"]},
    "vivo": {"price_base": (1000, 5000), "shop_names": ["vivo京东自营旗舰店", "vivo官方旗舰店", "vivo手机专卖店"]},
    "荣耀": {"price_base": (800, 4000), "shop_names": ["荣耀京东自营旗舰店", "荣耀官方旗舰店", "荣耀手机专卖店"]},
    "三星": {"price_base": (1500, 10000), "shop_names": ["三星京东自营旗舰店", "三星官方旗舰店", "三星手机专营店"]},
    "一加": {"price_base": (1500, 5000), "shop_names": ["一加京东自营旗舰店", "一加官方旗舰店", "一加手机专卖店"]},
    "iQOO": {"price_base": (1000, 4500), "shop_names": ["iQOO京东自营旗舰店", "iQOO官方旗舰店", "iQOO手机专卖店"]},
    "Realme": {"price_base": (800, 3500), "shop_names": ["Realme京东自营旗舰店", "Realme官方旗舰店", "Realme手机专卖店"]},
    "魅族": {"price_base": (1500, 5000), "shop_names": ["魅族京东自营旗舰店", "魅族官方旗舰店", "魅族手机专卖店"]},
    "努比亚": {"price_base": (1500, 5000), "shop_names": ["努比亚京东自营旗舰店", "努比亚官方旗舰店", "努比亚手机专卖店"]},
    "中兴": {"price_base": (1000, 4000), "shop_names": ["中兴京东自营旗舰店", "中兴官方旗舰店", "中兴手机专卖店"]},
    "联想": {"price_base": (800, 3500), "shop_names": ["联想京东自营旗舰店", "联想官方旗舰店", "联想手机专卖店"]},
    "摩托罗拉": {"price_base": (1000, 5000), "shop_names": ["摩托罗拉京东自营旗舰店", "摩托罗拉官方旗舰店", "摩托罗拉手机专卖店"]},
    "索尼": {"price_base": (3000, 10000), "shop_names": ["索尼京东自营旗舰店", "索尼官方旗舰店", "索尼手机专卖店"]},
    "华硕": {"price_base": (1500, 7000), "shop_names": ["华硕京东自营旗舰店", "华硕官方旗舰店", "华硕手机专卖店"]},
    "ROG": {"price_base": (3000, 9000), "shop_names": ["ROG京东自营旗舰店", "ROG官方旗舰店", "ROG手机专卖店"]},
    "Nothing": {"price_base": (1500, 5000), "shop_names": ["Nothing京东自营旗舰店", "Nothing官方旗舰店", "Nothing手机专卖店"]},
    "谷歌": {"price_base": (2500, 7000), "shop_names": ["谷歌京东自营旗舰店", "谷歌官方旗舰店", "谷歌手机专卖店"]},
}

# ========== 各平台特征参数 ==========
# price_factor: 相对于基准价格的调整系数（均值/标准差）
# sales_baseline: 销量基准值
# official_ratio: 官方旗舰店比例
PLATFORM_FEATURES = {
    "京东": {
        "price_factor_mean": 1.0,      # 京东=基准价
        "price_factor_std": 0.05,
        "sales_baseline": 8000,        # 京东用户消费力较强
        "official_ratio": 0.4,
    },
    "淘宝": {
        "price_factor_mean": 0.93,     # 淘宝比京东便宜约7%
        "price_factor_std": 0.08,
        "sales_baseline": 5000,
        "official_ratio": 0.25,
    },
    "抖音": {
        "price_factor_mean": 0.88,     # 抖音有券后价，比京东便宜约12%
        "price_factor_std": 0.10,
        "sales_baseline": 12000,       # 抖音流量大，销量基数高
        "official_ratio": 0.15,
    },
}


def generate_title(brand, idx):
    """生成随机的商品标题，包含品牌、型号、芯片、存储等特征"""
    suffix = random.choice(["", "Pro", "Max", "S", "SE", "X", "Plus", "Ultra", "2024款", "2025款",
                            "青春版", "精英版", "标准版", "旗舰版"])
    color = random.choice(["黑色", "白色", "蓝色", "粉色", "紫色", "绿色", "金色", "银色", "灰色", "渐变色"])
    chip = random.choice(["骁龙8Gen3", "骁龙8Gen2", "天玑9300", "天玑9200", "A17Pro", "A16", "麒麟9000", "Exynos2400", "TensorG3"])
    storage = random.choice(["128GB", "256GB", "512GB", "1024GB"])
    model = random.choice([
        f"PH-{1000+idx}", f"P-{1000+idx}",
        f"Series {idx%20+1}", f"{chr(65+idx%26)}{idx}"
    ])
    feature = random.choice(["", "5G", "曲面屏", "折叠屏", "快充"])
    if feature:
        feature += " "

    patterns = [
        f"{brand}{feature}手机{model}({storage})",
        f"{brand}手机{model}{suffix}",
        f"{brand}手机{model}",
        f"{brand}{color}{model}手机",
        f"{brand}手机{model}{suffix}({chip})",
        f"{brand}{feature}手机{model}{suffix}",
        f"{brand}手机{model}({chip})",
        f"{brand}手机{model}{storage}",
        f"{brand}{color}{model}{suffix}手机",
        f"{brand}手机{model}快充版({chip})",
        f"{brand}{storage}手机{model}",
    ]
    title = random.choice(patterns)
    title = title.replace("  ", " ").strip()
    return title


def generate_price(brand, platform):
    """根据品牌基础价格区间和平台特征生成当前价格"""
    info = BRANDS[brand]
    base_low, base_high = info["price_base"]
    pf = PLATFORM_FEATURES[platform]
    factor = max(0.5, min(1.5, random.gauss(pf["price_factor_mean"], pf["price_factor_std"])))
    price = round(random.uniform(base_low, base_high) * factor, 1)
    if platform == "抖音":
        price = round(price * random.uniform(0.75, 0.98), 1)
    return max(20, price)


def generate_original_price(price):
    """生成划线原价，通常是现价的1.1~2.5倍"""
    markup = random.uniform(1.1, 2.0)
    if price < 100:
        markup = random.uniform(1.2, 2.5)
    orig = round(price * markup)
    orig = (orig // 10) * 10 + 9
    return orig if orig > price else price + random.randint(10, 50)


def generate_sales(price, platform):
    """生成销量数据，价格越贵销量通常越低"""
    pf = PLATFORM_FEATURES[platform]
    base = pf["sales_baseline"]
    price_penalty = max(0.3, 1.0 - (price - 100) / 3000)
    sales = int(base * random.uniform(0.1, 3.0) * price_penalty)
    if random.random() < 0.08:
        sales *= random.randint(2, 5)
    return max(1, sales)


def generate_products_for_platform(platform, count=220):
    """为指定平台生成count条商品数据"""
    products = []
    brand_list = list(BRANDS.keys())

    brand_weights = []
    for b in brand_list:
        low, high = BRANDS[b]["price_base"]
        avg_price = (low + high) / 2
        if platform == "京东":
            weight = 1.5 if avg_price > 500 else 1.0
        elif platform == "淘宝":
            weight = 1.2 if 150 < avg_price < 600 else 1.0
        else:
            weight = 1.5 if avg_price < 300 else 0.8
        brand_weights.append(weight)
    brand_weights = np.array(brand_weights) / np.sum(brand_weights)

    for i in range(count):
        brand = np.random.choice(brand_list, p=brand_weights)
        price = generate_price(brand, platform)
        orig_price = generate_original_price(price)
        title = generate_title(brand, i)

        shop_name = random.choice(BRANDS[brand]["shop_names"])
        pf = PLATFORM_FEATURES[platform]
        if platform == "京东":
            is_official = 1 if random.random() < pf["official_ratio"] or "自营" in shop_name else 0
        else:
            is_official = 1 if random.random() < pf["official_ratio"] or ("旗舰" in shop_name and "官方" in shop_name) else 0

        link_map = {
            "京东": f"https://item.jd.com/{1000000 + i}.html",
            "淘宝": f"https://item.taobao.com/item.htm?id={5000000 + i}",
            "抖音": f"https://www.douyin.com/product/{9000000 + i}",
        }
        sales = generate_sales(price, platform)

        products.append({
            "平台名称": platform,
            "商品标题": title,
            "品牌": brand,
            "价格": price,
            "原价": orig_price,
            "销量": sales,
            "店铺名称": shop_name,
            "是否官方旗舰店": is_official,
            "商品链接": link_map[platform],
        })

    df = pd.DataFrame(products)
    df = df.drop_duplicates(subset=["品牌", "商品标题"])
    return df


def generate_all():
    """生成三个平台的全部样本数据"""
    print("正在生成样本数据...")
    jd = generate_products_for_platform("京东", 230)
    tb = generate_products_for_platform("淘宝", 240)
    dy = generate_products_for_platform("抖音", 220)
    print(f"  京东: {len(jd)} 条")
    print(f"  淘宝: {len(tb)} 条")
    print(f"  抖音: {len(dy)} 条")
    print(f"  总计: {len(jd) + len(tb) + len(dy)} 条")
    return jd, tb, dy


if __name__ == '__main__':
    jd, tb, dy = generate_all()
    print(jd.head())
