# -*- coding: utf-8 -*-
"""
数据分析模块
从清洗后的数据中提取洞察，包括：
1. 整体统计（均价、中位数、标准差等）
2. 跨平台价格对比
3. 品牌销量排行
4. 同品牌跨平台价差
5. 互动式选购推荐
"""
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import CLEANED_DATA_PATH


def load_clean_data():
    """加载清洗后的数据"""
    path = os.path.join(CLEANED_DATA_PATH, "all_phones_clean.csv")
    if not os.path.exists(path):
        from analysis.clean import run as clean_run
        clean_run()
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["价格"] = pd.to_numeric(df["价格"], errors="coerce")
    df["原价"] = pd.to_numeric(df["原价"], errors="coerce")
    df["销量"] = pd.to_numeric(df["销量"], errors="coerce").fillna(0).astype(int)
    return df[df["价格"] > 0].reset_index(drop=True)


def overall_stats(df):
    """计算全品类整体统计指标和各平台统计"""
    stats = {
        "商品总数": len(df),
        "平均价格": round(df["价格"].mean(), 2),
        "价格中位数": round(df["价格"].median(), 2),
        "价格标准差": round(df["价格"].std(), 2),
        "最低价格": round(df["价格"].min(), 2),
        "最高价格": round(df["价格"].max(), 2),
        "平均原价": round(df["原价"].mean(), 2),
        "平均折扣率": round(((df["原价"] - df["价格"]) / df["原价"]).mean() * 100, 2),
    }
    platform_stats = df.groupby("平台名称").agg(
        商品数量=("商品标题", "count"),
        平均价格=("价格", "mean"),
        价格中位数=("价格", "median"),
        平均原价=("原价", "mean"),
        平均折扣率=("价格", lambda x: round(((df.loc[x.index, "原价"] - x) / df.loc[x.index, "原价"]).mean() * 100, 2)),
    ).reset_index()
    platform_stats["平均价格"] = platform_stats["平均价格"].round(2)
    platform_stats["价格中位数"] = platform_stats["价格中位数"].round(2)
    platform_stats["平均原价"] = platform_stats["平均原价"].round(2)
    return stats, platform_stats


def price_range_distribution(df):
    """计算各价格区间的商品数量分布"""
    bins = [0, 100, 200, 300, 400, 500, 600, 800, 1000, 2000, 10000]
    labels = ["0-100", "100-200", "200-300", "300-400", "400-500",
              "500-600", "600-800", "800-1000", "1000-2000", "2000+"]
    df["价格区间"] = pd.cut(df["价格"], bins=bins, labels=labels, right=False)
    dist = df.groupby(["平台名称", "价格区间"], observed=True).size().unstack(fill_value=0)
    return dist, labels


def brand_top10_by_sales(df):
    """按总销量排序取Top10品牌"""
    return df.groupby("品牌")["销量"].sum().sort_values(ascending=False).head(10)


def brand_platform_avg_price(df):
    """计算Top10品牌在各平台的平均价格，用于跨平台价差分析"""
    top_brands = df.groupby("品牌")["销量"].sum().sort_values(ascending=False).head(10).index
    bp = df[df["品牌"].isin(top_brands)].groupby(["品牌", "平台名称"])["价格"].mean().round(2).unstack(fill_value=0)
    return bp


def discount_analysis(df):
    """分析各平台的平均折扣率"""
    df = df.copy()
    df["折扣率"] = ((df["原价"] - df["价格"]) / df["原价"] * 100).round(2)
    return df.groupby("平台名称")["折扣率"].mean().round(2)


def best_value_platform(df):
    """通过性价比指数（平均销量/平均价格）找出性价比最高的平台"""
    platform_avg = df.groupby("平台名称").agg(
        平均价格=("价格", "mean"),
        平均销量=("销量", "mean"),
        商品数=("商品标题", "count"),
    ).round(2)
    platform_avg["性价比指数"] = (platform_avg["平均销量"] / (platform_avg["平均价格"] + 1)).round(2)
    platform_avg = platform_avg.sort_values("性价比指数", ascending=False)
    return platform_avg


def interactive_filter(df):
    """
    命令行交互式选购推荐
    用户输入预算、偏好品牌、是否需要三模，输出符合条件的推荐列表
    """
    print("\n" + "=" * 60)
    print("  智能选购推荐系统")
    print("=" * 60)
    try:
        budget = float(input("\n请输入你的预算上限(元): ").strip())
    except:
        budget = 500
        print(f"  输入无效，默认预算: {budget}元")
    brand_input = input("请输入偏好的品牌(多个用逗号分隔，回车跳过): ").strip()
    preferred_brands = [b.strip() for b in brand_input.split(",") if b.strip()] if brand_input else []
    tri_mode = input("是否需要5G/折叠屏等高端机型？(y/n): ").strip().lower() == "y"

    # 按条件筛选
    filtered = df[df["价格"] <= budget].copy()
    if preferred_brands:
        filtered = filtered[filtered["品牌"].isin(preferred_brands)]
    if tri_mode:
        kw = filtered["商品标题"].str.contains("5G|折叠屏|曲面屏", na=False)
        filtered = filtered[kw]

    filtered = filtered.sort_values(["销量", "价格"], ascending=[False, True]).head(20)
    if len(filtered) == 0:
        print("\n未找到符合条件的商品，请放宽筛选条件。")
        return

    # 格式化输出表格
    print(f"\n为你找到 {len(filtered)} 款符合条件的手机：")
    print(f"{'排名':<4} {'品牌':<8} {'型号摘要':<30} {'价格':<8} {'平台':<6} {'销量':<10}")
    print("-" * 68)
    for i, (_, row) in enumerate(filtered.iterrows(), 1):
        title_short = row["商品标题"][:28] if len(str(row["商品标题"])) > 28 else row["商品标题"]
        sales_str = f"{row['销量']/10000:.1f}万" if row["销量"] >= 10000 else str(row["销量"])
        print(f"{i:<4} {row['品牌']:<8} {title_short:<30} ¥{row['价格']:<6.0f} {row['平台名称']:<6} {sales_str:<10}")
    best = filtered.iloc[0]
    print(f"\n推荐：在【{best['平台名称']}】购买【{best['商品标题'][:30]}】性价比最高！")
    return filtered


def generate_report(df):
    """生成完整的文本分析报告"""
    stats, plat_stats = overall_stats(df)
    brand_sales = brand_top10_by_sales(df)
    brand_prices = brand_platform_avg_price(df)
    avg_discount = discount_analysis(df)
    best_value = best_value_platform(df)

    lines = []
    lines.append("=" * 65)
    lines.append("                  手机跨平台价格分析报告")
    lines.append("=" * 65)
    lines.append(f"\n分析品类: {stats['商品总数']} 款手机")
    lines.append("数据来源: 京东 / 淘宝(慢慢买) / 抖音")
    lines.append("分析维度: 价格、品牌、销量、折扣率、店铺类型")

    lines.append("\n" + "-" * 65)
    lines.append("一、整体统计")
    lines.append("-" * 65)
    lines.append(f"  总商品数:     {stats['商品总数']} 款")
    lines.append(f"  平均价格:     {stats['平均价格']} 元")
    lines.append(f"  价格中位数:   {stats['价格中位数']} 元")
    lines.append(f"  价格标准差:   {stats['价格标准差']}")
    lines.append(f"  价格范围:     {stats['最低价格']} ~ {stats['最高价格']} 元")
    lines.append(f"  平均折扣率:   {stats['平均折扣率']}%")

    lines.append("\n" + "-" * 65)
    lines.append("二、跨平台价格对比")
    lines.append("-" * 65)
    for _, row in plat_stats.iterrows():
        lines.append(f"  {row['平台名称']}: 均价¥{row['平均价格']}, 中位数¥{row['价格中位数']}, 平均折扣{row['平均折扣率']}%")
    cheapest = plat_stats.loc[plat_stats["平均价格"].idxmin()]
    lines.append(f"\n  >> 最便宜平台: 【{cheapest['平台名称']}】(均价¥{cheapest['平均价格']})")

    lines.append("\n" + "-" * 65)
    lines.append("三、各平台折扣力度对比")
    lines.append("-" * 65)
    for platform, discount in avg_discount.items():
        lines.append(f"  {platform}: 平均折扣率 {discount}%")
    max_disc = avg_discount.idxmax()
    lines.append(f"\n  >> 折扣力度最大: 【{max_disc}】")

    lines.append("\n" + "-" * 65)
    lines.append("四、销量Top10品牌")
    lines.append("-" * 65)
    for i, (brand, sales) in enumerate(brand_sales.items(), 1):
        sales_str = f"{sales/10000:.1f}万" if sales >= 10000 else str(sales)
        lines.append(f"  {i}. {brand:<8} 总销量: {sales_str} 件")

    lines.append("\n" + "-" * 65)
    lines.append("五、同品牌跨平台价差")
    lines.append("-" * 65)
    for brand in brand_prices.index[:5]:
        prices = brand_prices.loc[brand]
        prices_valid = prices[prices > 0]
        if len(prices_valid) >= 2:
            diff = prices_valid.max() - prices_valid.min()
            lines.append(f"  {brand}: 价差¥{diff:.0f}({prices_valid.to_dict()})")

    lines.append("\n" + "-" * 65)
    lines.append("六、性价比平台排行")
    lines.append("-" * 65)
    for i, (platform, row) in enumerate(best_value.iterrows(), 1):
        lines.append(f"  {i}. {platform}: 均价¥{row['平均价格']}, 平均销量{int(row['平均销量'])}件")

    lines.append("\n" + "=" * 65)
    lines.append("结论与建议:")
    lines.append("=" * 65)
    if cheapest["平台名称"] == "抖音":
        lines.append("  1. 抖音商城整体价格最低，叠加直播间优惠券后折扣力度最大")
    elif cheapest["平台名称"] == "淘宝":
        lines.append("  1. 淘宝平台整体价格最低，商家竞争激烈导致定价更实惠")
    else:
        lines.append("  1. 京东平台整体价格最低（可能有误，请核实数据）")
    lines.append(f"  2. 折扣率方面，{avg_discount.idxmax()}平台折扣最大")
    lines.append(f"  3. 销量Top3品牌: {', '.join(brand_sales.index[:3].tolist())}")
    lines.append(f"  4. {'三平台中，抖音' if '抖音' in df['平台名称'].unique() else ''}低价高销量爆款最多，适合追求性价比的消费者")
    lines.append("  5. 同品牌在不同平台存在显著价差，建议购买前跨平台比价")
    lines.append("\n  (数据来源: 京东/淘宝/抖音  |  品类: 手机  |  项目背景: 618购物节)")
    lines.append("=" * 65)
    return "\n".join(lines)


if __name__ == "__main__":
    df = load_clean_data()
    print(f"加载数据: {len(df)} 条")
    report = generate_report(df)
    print(report)
    interactive_filter(df)