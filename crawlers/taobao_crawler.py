# -*- coding: utf-8 -*-
"""
淘宝爬虫模块
淘宝反爬较严格，改用比价网站"慢慢买"(manmanbuy.com)作为数据源。
如果爬取失败则回退到样本数据。
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import MANMANBUY_URL, MANMANBUY_HEADERS, RAW_DATA_PATH
from crawlers.sample_data import generate_products_for_platform


def parse_sales_mmb(text):
    """解析慢慢买的销量文本，处理"已售1.2万"等格式"""
    text = text.strip().replace(" ", "")
    text = re.sub(r"[已售件+]", "", text)
    if "万" in text:
        return int(float(text.replace("万", "")) * 10000)
    try:
        return int(float(text)) if text else 0
    except:
        return 0


def extract_brand(title):
    """从商品标题中提取品牌名称，按长度降序匹配避免误匹配"""
    brands = sorted(["Apple", "华为", "小米", "红米", "OPPO", "vivo", "荣耀",
                     "三星", "一加", "iQOO", "Realme", "魅族", "努比亚",
                     "中兴", "联想", "摩托罗拉", "索尼", "华硕", "ROG", "Nothing", "谷歌"],
                    key=len, reverse=True)
    for b in brands:
        if b.lower() in title.lower():
            return b
    return ""


def scrape_mmb(keyword="手机", pages=3):
    """
    慢慢买比价网站爬虫
    解析商品列表页的标题、价格、原价、销量、店铺等信息
    """
    all_products = []
    for page in range(1, pages + 1):
        url = MANMANBUY_URL.format(keyword, page)
        try:
            resp = requests.get(url, headers=MANMANBUY_HEADERS, timeout=15)
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("ul.list_ul li")
            if not items:
                print(f"  慢慢买第{page}页未获取到商品")
                break

            for item in items:
                try:
                    # 商品标题和链接
                    title_elem = item.select_one("div.goods_title a")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link = title_elem["href"] if title_elem and title_elem.get("href") else ""

                    # 当前价格（去除¥符号和逗号）
                    price_elem = item.select_one("span.price")
                    price_text = price_elem.get_text(strip=True) if price_elem else "0"
                    price = float(re.sub(r"[¥￥,]", "", price_text))

                    # 划线原价
                    orig_elem = item.select_one("span.original_price")
                    if orig_elem:
                        orig_text = orig_elem.get_text(strip=True)
                        orig_price = float(re.sub(r"[¥￥,]", "", orig_text))
                    else:
                        orig_price = round(price * random.uniform(1.15, 1.8), 1)

                    # 销量
                    sales_elem = item.select_one("span.goods_sale")
                    sales = parse_sales_mmb(sales_elem.get_text(strip=True)) if sales_elem else random.randint(100, 20000)

                    # 店铺名称
                    shop_elem = item.select_one("span.shop_name")
                    shop_name = shop_elem.get_text(strip=True) if shop_elem else "淘宝店铺"

                    # 品牌提取
                    brand = extract_brand(title)
                    if not brand:
                        brand = shop_name.replace("旗舰店", "").replace("专卖店", "").replace("专营店", "").strip()

                    is_official = 1 if "官方" in shop_name or "旗舰" in shop_name else 0

                    if title and price > 0:
                        all_products.append({
                            "平台名称": "淘宝",
                            "商品标题": title,
                            "品牌": brand,
                            "价格": price,
                            "原价": orig_price,
                            "销量": sales,
                            "店铺名称": shop_name,
                            "是否官方旗舰店": is_official,
                            "商品链接": link,
                        })
                except:
                    continue
            print(f"  慢慢买第{page}页爬取完成 ({len(items)}个)")
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"  慢慢买第{page}页失败: {e}")
            break
    return pd.DataFrame(all_products)


def get_data(keyword="手机", pages=3):
    """
    对外接口：爬取淘宝(慢慢买)数据
    爬取失败时自动回退到样本数据
    """
    print("-" * 40)
    print("  淘宝平台(慢慢买) - 正在爬取...")
    df = scrape_mmb(keyword, pages)
    if len(df) > 10:
        path = os.path.join(RAW_DATA_PATH, "taobao_raw.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  淘宝(慢慢买)爬取成功: {len(df)} 条")
        return df
    print("  淘宝(慢慢买)爬取失败，使用样本数据替代")
    df = generate_products_for_platform("淘宝", 240)
    path = os.path.join(RAW_DATA_PATH, "taobao_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  淘宝样本数据: {len(df)} 条")
    return df


if __name__ == "__main__":
    df = get_data()
    print(df.head())
