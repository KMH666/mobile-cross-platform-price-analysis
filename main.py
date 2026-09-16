# -*- coding: utf-8 -*-
"""
主入口模块
协调整个项目流程：爬虫 -> 清洗 -> 分析 -> 可视化 -> 选购推荐
"""
import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, BASE_DIR)

from config import RAW_DATA_PATH, CLEANED_DATA_PATH
from crawlers.jd_crawler import get_data as get_jd_data
from crawlers.taobao_crawler import get_data as get_taobao_data
from crawlers.douyin_crawler import get_data as get_douyin_data
from analysis.clean import run as run_clean
from analysis.analyze import load_clean_data, generate_report, interactive_filter
from analysis.visualize import generate_all_charts


def run_crawlers():
    """第一阶段：爬取京东、淘宝、抖音三平台数据"""
    print("=" * 60)
    print("  第一阶段: 数据爬取")
    print("=" * 60)
    print(f"  搜索关键词: {__import__('config').KEYWORD}")
    jd_df = get_jd_data()
    tb_df = get_taobao_data()
    dy_df = get_douyin_data()
    total = len(jd_df) + len(tb_df) + len(dy_df)
    print(f"\n  三平台共获取: {total} 条原始数据")
    return total


def run_analysis():
    """第二阶段~第五阶段：清洗、分析、可视化、推荐"""
    print("\n" + "=" * 60)
    print("  第二阶段: 数据清洗与预处理")
    print("=" * 60)
    df = run_clean()

    print("\n" + "=" * 60)
    print("  第三阶段: 数据分析")
    print("=" * 60)
    report = generate_report(df)
    print(f"  分析报告已生成 ({len(report)} 字符)")
    report_path = os.path.join(BASE_DIR, "分析报告.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n分析报告已保存至: {report_path}")

    print("\n" + "=" * 60)
    print("  第四阶段: 可视化图表生成")
    print("=" * 60)
    chart_paths = generate_all_charts(df)

    print("\n" + "=" * 60)
    print("  第五阶段: 智能选购推荐")
    print("=" * 60)
    filtered = interactive_filter(df)

    print("\n" + "=" * 60)
    print("  分析完成！生成文件列表：")
    print("=" * 60)
    for path in chart_paths:
        print(f"  - {path}")
    print(f"  - {report_path}")
    print(f"  - {os.path.join(CLEANED_DATA_PATH, 'all_phones_clean.csv')}")
    print("=" * 60)


def main():
    """项目主入口"""
    print("=" * 60)
    print("   手机跨平台价格分析系统")
    print("   数据来源: 京东 / 淘宝(慢慢买) / 抖音商城")
    print("   项目背景: 618购物节价格分析")
    print("=" * 60)
    run_crawlers()
    run_analysis()


if __name__ == "__main__":
    main()
