# -*- coding: utf-8 -*-
"""
京东爬虫模块
使用 requests + BeautifulSoup 爬取京东搜索页面的商品信息。
由于京东有反爬机制，如果爬取失败会自动回退到样本数据。
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import JD_URL, JD_HEADERS, RAW_DATA_PATH
from crawlers.sample_data import generate_products_for_platform


def parse_sales(text):
    """解析京东销量文本，支持"1.2万+"格式转数字"""
    text = text.strip()
    if "万" in text:
        return int(float(text.replace("万", "").replace("+", "")) * 10000)
    if "亿" in text:
        return int(float(text.replace("亿", "").replace("+", "")) * 100000000)
    text = text.replace("+", "").replace("条评价", "").replace("已售", "").replace("件", "")
    try:
        return int(float(text))
    except:
        return 0


def scrape(keyword="手机", pages=5):
    """
    京东搜索页爬虫
    解析 div.gl-item 容器中的商品名称、价格、销量、店铺等信息
    """
    all_products = []
    for page in range(1, pages + 1):
        url = JD_URL.format(keyword, page)
        try:
            resp = requests.get(url, headers=JD_HEADERS, timeout=15)
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("div.gl-item")
            if not items:
                print(f"  京东第{page}页未获取到商品，可能触发反爬")
                break

            for item in items:
                try:
                    # 商品名称
                    name_elem = item.select_one("div.p-name a em")
                    if not name_elem:
                        continue
                    title = name_elem.get_text(strip=True).replace("\n", "").replace(" ", "")

                    # 当前价格
                    price_elem = item.select_one("div.p-price i")
                    price = float(price_elem.get_text(strip=True)) if price_elem else 0

                    # 划线原价（部分商品有）
                    orig_elem = item.select_one("div.p-price del")
                    orig_price = float(orig_elem.get_text(strip=True)) if orig_elem else price

                    # 评价数
                    commit_elem = item.select_one("div.p-commit a")
                    sales = parse_sales(commit_elem.get_text(strip=True)) if commit_elem else 0

                    # 店铺名称
                    shop_elem = item.select_one("div.p-shop a")
                    shop_name = shop_elem.get_text(strip=True) if shop_elem else "京东自营"

                    # 判断是否为自营/官方旗舰店
                    is_official = 1 if ("自营" in str(item) or "旗舰" in str(item)) else 0

                    # 商品链接
                    link_elem = item.select_one("div.p-name a")
                    link = "https:" + link_elem["href"] if link_elem and link_elem.get("href") else ""
                    if link and not link.startswith("http"):
                        link = "https:" + link

                    # 从标题中提取品牌名
                    brand = ""
                    for b in ["Apple", "华为", "小米", "红米", "OPPO", "vivo", "荣耀",
                              "三星", "一加", "iQOO", "Realme", "魅族", "努比亚",
                              "中兴", "联想", "摩托罗拉", "索尼", "华硕", "ROG", "Nothing", "谷歌"]:
                        if b.lower() in title.lower() or b in title:
                            brand = b
                            break
                    if not brand:
                        brand = shop_name.replace("京东自营旗舰店", "").replace("官方旗舰店", "").replace("旗舰店", "").strip()

                    if title and price > 0:
                        all_products.append({
                            "平台名称": "京东",
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
            print(f"  京东第{page}页爬取完成 ({len(items)}个)")
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"  京东第{page}页失败: {e}")
            break
    return pd.DataFrame(all_products)


def get_data(keyword="手机", pages=5):
    """
    对外接口：爬取京东数据
    如果爬取失败（不足10条），自动使用样本数据
    """
    print("-" * 40)
    print("  京东平台 - 正在爬取...")
    df = scrape(keyword, pages)
    if len(df) > 10:
        path = os.path.join(RAW_DATA_PATH, "jd_raw.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  京东爬取成功: {len(df)} 条")
        return df
    print("  京东爬取失败，使用样本数据替代")
    df = generate_products_for_platform("京东", 230)
    path = os.path.join(RAW_DATA_PATH, "jd_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  京东样本数据: {len(df)} 条")
    return df


if __name__ == "__main__":
    df = get_data()
    print(df.head())
