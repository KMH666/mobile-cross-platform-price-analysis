# -*- coding: utf-8 -*-
"""
配置文件模块
集中管理所有常量、URL、路径等配置，避免硬编码
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(__file__)

# ========== 爬虫配置 ==========
KEYWORD = "手机"                # 搜索关键词
PAGES_PER_PLATFORM = 5               # 每平台爬取页数
ITEMS_PER_PAGE = 40                   # 每页商品数（估算）

# ========== 京东爬虫配置 ==========
JD_URL = "https://search.jd.com/Search?keyword={}&page={}"
JD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.jd.com/',
}

# ========== 淘宝/慢慢买爬虫配置 ==========
MANMANBUY_URL = "https://search.manmanbuy.com/Search?key={}&page={}"
MANMANBUY_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
}

# ========== 抖音爬虫配置 ==========
DOUYIN_SEARCH_URL = "https://www.douyin.com/search/{}?type=product"
DOUYIN_API_URL = "https://www.douyin.com/aweme/v1/web/search/item/"

# ========== 路径配置 ==========
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")              # 原始数据目录
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")      # 清洗后数据目录
CHART_DIR = os.path.join(BASE_DIR, "charts")                        # 图表输出目录

# 自动创建所需目录
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)
