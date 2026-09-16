# -*- coding: utf-8 -*-
"""
抖音爬虫模块
抖音商城数据通过API接口和网页解析两种方式尝试获取。
API方式通过 /aweme/v1/web/search/item/ 接口获取商品JSON数据。
网页方式从RENDER_DATA中提取商品信息。
同时提供Selenium方案（备选）。
失败时回退到样本数据。
"""
import requests
import pandas as pd
import re
import json
import time
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DOUYIN_SEARCH_URL, RAW_DATA_PATH
from crawlers.sample_data import generate_products_for_platform

DOUYIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.douyin.com/",
}


def extract_brand(title):
    """从商品标题提取品牌名"""
    brands = sorted(["Apple", "华为", "小米", "红米", "OPPO", "vivo", "荣耀",
                     "三星", "一加", "iQOO", "Realme", "魅族", "努比亚",
                     "中兴", "联想", "摩托罗拉", "索尼", "华硕", "ROG", "Nothing", "谷歌"],
                    key=len, reverse=True)
    for b in brands:
        if b.lower() in title.lower():
            return b
    return ""


def parse_sales(text):
    """解析文本格式的销量"""
    text = text.strip()
    if "万" in text:
        return int(float(text.replace("万", "")) * 10000)
    if "亿" in text:
        return int(float(text.replace("亿", "")) * 100000000)
    text = re.sub(r"[已售+件]", "", text)
    try:
        return int(float(text)) if text else 0
    except:
        return 0


def scrape_douyin_api(keyword="手机"):
    """
    通过抖音开放API获取商品搜索数据
    使用 /aweme/v1/web/search/item/ 接口
    """
    all_products = []
    for page in range(1, 6):
        params = {
            "keyword": keyword,
            "type": "product",
            "offset": (page - 1) * 20,
            "count": 20,
        }
        try:
            resp = requests.get(
                "https://www.douyin.com/aweme/v1/web/search/item/",
                params=params,
                headers=DOUYIN_HEADERS,
                timeout=15,
            )
            data = resp.json()
            items = data.get("data", [])
            if not items:
                break
            for item in items:
                try:
                    product = item.get("product", {})
                    title = product.get("title", "")
                    price = float(product.get("price", 0))
                    orig_price = float(product.get("origin_price", price * 1.3))
                    sales = int(product.get("sales", 0))
                    shop_info = product.get("shop", {})
                    shop_name = shop_info.get("shop_name", "") if shop_info else ""
                    is_official = 1 if shop_name and ("官方" in shop_name or "旗舰" in shop_name) else 0
                    link = f"https://www.douyin.com/product/{product.get('product_id', page*1000)}"
                    brand = extract_brand(title)
                    if not brand:
                        brand = shop_name.replace("官方旗舰店", "").replace("旗舰店", "").replace("专卖店", "").strip()
                    if title and price > 0:
                        all_products.append({
                            "平台名称": "抖音",
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
            print(f"  抖音第{page}页爬取完成")
            time.sleep(random.uniform(2, 3))
        except Exception as e:
            print(f"  抖音第{page}页失败: {e}")
            break
    return pd.DataFrame(all_products)


def scrape_douyin_web(keyword="手机"):
    """
    从抖音网页版搜索页解析RENDER_DATA中的商品数据
    """
    all_products = []
    url = DOUYIN_SEARCH_URL.format(keyword)
    try:
        resp = requests.get(url, headers=DOUYIN_HEADERS, timeout=15)
        json_pattern = r'<script id="RENDER_DATA" type="application/json">(.*?)</script>'
        match = re.search(json_pattern, resp.text)
        if match:
            raw = match.group(1)
            if raw.startswith("{"):
                data = json.loads(raw)
                products = data.get("product", {}).get("productData", [])
                for item in products:
                    try:
                        title = item.get("title", "")
                        price = float(item.get("price", 0))
                        sales = int(item.get("sellCount", 0))
                        shop_name = item.get("shopName", "")
                        brand = extract_brand(title)
                        all_products.append({
                            "平台名称": "抖音",
                            "商品标题": title,
                            "品牌": brand,
                            "价格": price,
                            "原价": price * 1.3,
                            "销量": sales,
                            "店铺名称": shop_name,
                            "是否官方旗舰店": 1 if "官方" in shop_name else 0,
                            "商品链接": f"https://www.douyin.com/product/{item.get('productId', '')}",
                        })
                    except:
                        continue
        print(f"  抖音网页解析完成: {len(all_products)} 条")
    except Exception as e:
        print(f"  抖音网页解析失败: {e}")
    return pd.DataFrame(all_products)


def get_data(keyword="手机"):
    """
    对外接口：爬取抖音数据
    优先使用API，失败则用网页解析，再失败则回退样本数据
    """
    print("-" * 40)
    print("  抖音平台 - 正在爬取...")
    df = scrape_douyin_api(keyword)
    if len(df) < 10:
        df = scrape_douyin_web(keyword)
    if len(df) > 10:
        path = os.path.join(RAW_DATA_PATH, "douyin_raw.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  抖音爬取成功: {len(df)} 条")
        return df
    print("  抖音爬取失败，使用样本数据替代")
    df = generate_products_for_platform("抖音", 220)
    path = os.path.join(RAW_DATA_PATH, "douyin_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  抖音样本数据: {len(df)} 条")
    return df


def get_data_selenium(keyword="手机"):
    """
    使用Selenium模拟浏览器爬取抖音（备选方案）
    需要安装 selenium 和 ChromeDriver
    """
    print("-" * 40)
    print("  抖音平台(需Selenium) - 请先安装: pip install selenium")
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        url = DOUYIN_SEARCH_URL.format(keyword)
        driver.get(url)
        time.sleep(5)
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        products = driver.find_elements(By.CSS_SELECTOR, "[class*='product']")
        print(f"  抖音Selenium已加载{len(products)}个商品元素")
        driver.quit()
    except Exception as e:
        print(f"  Selenium不可用: {e}")
        print("  切换为API爬取方式")
    return get_data(keyword)


if __name__ == "__main__":
    df = get_data()
    print(df.head())
