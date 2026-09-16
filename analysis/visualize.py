# -*- coding: utf-8 -*-
"""
可视化模块
生成5张分析图表，用于直观展示跨平台价格对比、分布、品牌价差等：
图1: 三平台平均价格与中位数对比柱状图
图2: 三平台价格分布堆叠直方图
图3: Top10品牌在各平台的平均价格横向柱状图
图4: 三平台价格箱线图
图5: 价格vs销量散点图（标注Top10销量品牌）
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
import sys
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import CHART_DIR

# 中文字体配置，按优先级尝试多个字体
font_names = ["SimHei", "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Arial Unicode MS"]
matplotlib.rcParams["font.sans-serif"] = font_names
matplotlib.rcParams["axes.unicode_minus"] = False

sns.set_style("whitegrid")
# 各平台品牌色：京东红、淘宝橙、抖音蓝
COLORS = {"京东": "#E4393C", "淘宝": "#FF6A00", "抖音": "#00A8EC"}


def fig1_avg_price_bar(df):
    """图1: 三平台平均价格与中位数对比 - 分组柱状图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    platform_stats = df.groupby("平台名称")["价格"].agg(["mean", "median", "std"]).round(2)
    x = range(len(platform_stats.index))
    width = 0.3
    colors = [COLORS.get(p, "#999") for p in platform_stats.index]

    # 平均价格柱
    bars = ax.bar(x, platform_stats["mean"], width, color=colors, edgecolor="white", linewidth=1.2, label="平均价格")
    for bar, val in zip(bars, platform_stats["mean"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f"¥{val:.0f}",
                ha="center", fontsize=12, fontweight="bold")

    # 中位数柱（半透明）
    med_x = [i + width for i in x]
    med_bars = ax.bar(med_x, platform_stats["median"], width, color=[c + "99" for c in colors],
                      edgecolor="white", linewidth=1.2, label="价格中位数")
    for bar, val in zip(med_bars, platform_stats["median"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f"¥{val:.0f}",
                ha="center", fontsize=10, color="#666")

    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(platform_stats.index, fontsize=13)
    ax.set_ylabel("价格 (元)", fontsize=12)
    ax.set_title("三平台平均价格与中位数对比", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11, loc="upper left")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "fig1_avg_price_bar.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  图1已保存: {path}")
    return path


def fig2_price_distribution(df):
    """图2: 三平台价格分布 - 堆叠直方图，展示各平台价格集中区间"""
    fig, ax = plt.subplots(figsize=(12, 6))
    bins = np.arange(0, df["价格"].quantile(0.95) + 50, 50)
    platforms = df["平台名称"].unique()
    colors = [COLORS.get(p, "#999") for p in platforms]
    data_list = [df[df["平台名称"] == p]["价格"].values for p in platforms]
    ax.hist(data_list, bins=bins, label=platforms, color=colors, alpha=0.7, edgecolor="white", linewidth=0.5)
    ax.set_xlabel("价格 (元)", fontsize=12)
    ax.set_ylabel("商品数量", fontsize=12)
    ax.set_title("三平台价格分布堆叠直方图", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "fig2_price_distribution.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  图2已保存: {path}")
    return path


def fig3_brand_platform_price(df):
    """图3: 热销Top10品牌在各平台的平均价格 - 横向柱状图"""
    fig, ax = plt.subplots(figsize=(14, 8))
    top_brands = df.groupby("品牌")["销量"].sum().sort_values(ascending=False).head(10).index
    bp = df[df["品牌"].isin(top_brands)].groupby(["品牌", "平台名称"])["价格"].mean().round(2).unstack(fill_value=0)
    bp = bp.loc[top_brands if all(b in bp.index for b in top_brands) else bp.index]
    platforms_in_data = [p for p in ["京东", "淘宝", "抖音"] if p in bp.columns]
    y = np.arange(len(bp.index))
    height = 0.25

    for i, p in enumerate(platforms_in_data):
        vals = bp[p].values if p in bp.columns else np.zeros(len(bp.index))
        offset = (i - (len(platforms_in_data)-1)/2) * height
        bars = ax.barh(y + offset, vals, height, label=p, color=COLORS.get(p, "#999"), alpha=0.85, edgecolor="white")
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                        f"¥{v:.0f}", va="center", fontsize=8, color="#333")

    ax.set_yticks(y)
    ax.set_yticklabels(bp.index, fontsize=11)
    ax.set_xlabel("平均价格 (元)", fontsize=12)
    ax.set_title("热销Top10品牌在各平台的平均价格对比（手机）", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11, loc="lower right")
    ax.grid(True, alpha=0.3, axis="x")
    ax.set_xlim(0, bp.values.max() * 1.3)
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "fig3_brand_platform_price.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  图3已保存: {path}")
    return path


def fig4_price_boxplot(df):
    """图4: 三平台价格箱线图 - 展示中位数、四分位距、异常值"""
    fig, ax = plt.subplots(figsize=(10, 7))
    platforms = df["平台名称"].unique()
    data_list = [df[df["平台名称"] == p]["价格"].values for p in platforms]
    colors = [COLORS.get(p, "#999") for p in platforms]
    bp = ax.boxplot(data_list, labels=platforms, patch_artist=True, widths=0.5,
                     showmeans=True, meanprops=dict(marker="D", markerfacecolor="red", markersize=8))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color + "66")
        patch.set_edgecolor(color)
        patch.set_linewidth(2)
    for whisker in bp["whiskers"]:
        whisker.set_color("#333")
        whisker.set_linewidth(1.5)
    for cap in bp["caps"]:
        cap.set_color("#333")
        cap.set_linewidth(1.5)
    for median in bp["medians"]:
        median.set_color("#E91E63")
        median.set_linewidth(2.5)
    for flier in bp["fliers"]:
        flier.set(marker="o", markersize=6, markerfacecolor="#FF9800", alpha=0.6)
    ax.set_ylabel("价格 (元)", fontsize=12)
    ax.set_title("三平台价格箱线图", fontsize=15, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "fig4_price_boxplot.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  图4已保存: {path}")
    return path


def fig5_price_vs_sales_scatter(df):
    """图5: 价格vs销量散点图 - 用颜色区分平台，标注高销量品牌"""
    fig, ax = plt.subplots(figsize=(12, 8))
    for platform in ["京东", "淘宝", "抖音"]:
        subset = df[df["平台名称"] == platform]
        if len(subset) == 0:
            continue
        ax.scatter(subset["价格"], subset["销量"], c=COLORS.get(platform, "#999"),
                   label=platform, alpha=0.5, s=35, edgecolors="white", linewidth=0.5)

    # 标注销量Top10商品的品牌名
    top10 = df.nlargest(10, "销量")
    for _, row in top10.iterrows():
        ax.annotate(row["品牌"], (row["价格"], row["销量"]),
                    fontsize=9, alpha=0.8, ha="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="yellow", alpha=0.3))
    ax.set_xlabel("价格 (元)", fontsize=12)
    ax.set_ylabel("销量", fontsize=12)
    ax.set_title("价格 vs 销量 散点图（标注销量Top10品牌—手机）", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHART_DIR, "fig5_price_vs_sales_scatter.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  图5已保存: {path}")
    return path


def generate_all_charts(df):
    """生成全部5张图表"""
    print("\n" + "=" * 50)
    print("生成可视化图表 (5张)")
    print("=" * 50)
    os.makedirs(CHART_DIR, exist_ok=True)
    paths = []
    paths.append(fig1_avg_price_bar(df))
    paths.append(fig2_price_distribution(df))
    paths.append(fig3_brand_platform_price(df))
    paths.append(fig4_price_boxplot(df))
    paths.append(fig5_price_vs_sales_scatter(df))
    print(f"\n所有图表已保存至: {CHART_DIR}")
    return paths


if __name__ == "__main__":
    from analysis.analyze import load_clean_data
    df = load_clean_data()
    generate_all_charts(df)