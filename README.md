# 手机跨平台价格分析系统

> 一个基于 Python 的电商跨平台手机价格采集与分析系统，覆盖 **数据爬取 → 数据清洗 → 数据分析 → 可视化 → 智能选购推荐** 全流程。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![pandas](https://img.shields.io/badge/pandas-1.5%2B-150458)
![License](https://img.shields.io/badge/License-MIT-green)

## 项目简介

每年 618 购物节期间，京东、淘宝、抖音商城等电商平台都会推出大量促销活动，消费者面对海量商品和复杂优惠规则，很难高效地进行跨平台比价。手机作为价格差异显著、关注度高的数码品类，正是这一痛点的典型代表。

本项目以 **618 购物节** 为背景，爬取三大平台的手机商品数据，从**价格分布、品牌销量、跨平台价差、折扣力度**等维度进行系统分析，最终生成文本分析报告、5 张可视化图表，并提供命令行交互式选购推荐。

> 说明：京东、淘宝、抖音均有较强反爬机制。当爬虫获取数据不足时，程序会**自动回退到内置样本数据**（固定随机种子、可复现），保证分析流程完整可演示。

## 功能特性

- **多平台数据采集**：京东（搜索页解析）、淘宝（经"慢慢买"比价网站）、抖音（开放 API + 网页解析，附 Selenium 备选方案）
- **健壮的降级策略**：任一爬虫失败自动使用样本数据，流程不中断
- **数据清洗**：统一价格/销量/品牌等字段格式，去除货币符号、解析"万/亿"单位、按标题提取品牌、去重
- **多维度分析**：整体统计、跨平台价格对比、折扣力度、销量 Top10 品牌、同品牌跨平台价差、性价比平台排行
- **可视化**：自动生成 5 张高质量图表（柱状图、堆叠直方图、横向柱状图、箱线图、散点图）
- **交互式推荐**：按预算、偏好品牌、是否高端机型筛选，输出性价比推荐

## 项目结构

```
24211870125刘远辉python期末项目/
├── config.py                  # 全局配置（关键词、URL、请求头、路径）
├── main.py                    # 主入口：爬虫 → 清洗 → 分析 → 可视化 → 推荐
├── requirements.txt           # 依赖清单
├── README.md                  # 项目说明（本文件）
├── 使用文档.md                # 详细使用文档
│
├── crawlers/                  # 爬虫模块
│   ├── sample_data.py         # 样本数据生成器（爬取失败时使用）
│   ├── jd_crawler.py          # 京东爬虫（requests + BeautifulSoup）
│   ├── taobao_crawler.py      # 淘宝爬虫（通过"慢慢买"比价网站）
│   └── douyin_crawler.py      # 抖音爬虫（API + 网页解析 + Selenium 备选）
│
├── analysis/                  # 分析模块
│   ├── clean.py               # 数据清洗（字段统一、品牌提取、去重）
│   ├── analyze.py             # 数据分析 + 命令行选购推荐
│   └── visualize.py           # 可视化（5 张图表）
│
├── data/                      # 数据目录
│   ├── raw/                   # 三平台原始数据（CSV）
│   └── cleaned/               # 清洗合并后的数据
│
├── charts/                    # 图表输出目录（5 张 PNG）
│
├── 辅助代码/                  # 辅助脚本
│   ├── create_ppt.py          # 答辩 PPT 自动生成
│   ├── generate_report.py     # 实验报告 PDF 生成
│   └── code_snippets.txt      # 代码片段参考
│
├── 分析报告.txt               # 自动生成的文本分析报告
└── 简单功能演示.mp4           # 运行效果演示视频
```

## 环境要求

- **Python 3.8+**
- 依赖库见 `requirements.txt`

```bash
pip install -r requirements.txt
```

| 依赖 | 用途 |
|------|------|
| pandas / numpy | 数据处理与数值计算 |
| matplotlib / seaborn | 图表绘制 |
| requests | HTTP 请求 |
| beautifulsoup4 / lxml | HTML 解析 |

## 使用方法

### 一键运行（推荐）

```bash
python main.py
```

依次执行：爬取数据 → 清洗 → 分析 → 生成图表 → 交互式选购推荐。

> 第 5 步为交互式输入，建议在 **cmd / 终端** 中直接运行，不要重定向输出。

### 分步运行

```bash
# 仅清洗数据
python -c "from analysis.clean import run; run()"

# 仅生成图表
python analysis/visualize.py

# 仅进入选购推荐
python -c "from analysis.analyze import load_clean_data, interactive_filter; interactive_filter(load_clean_data())"

# 单独调试某个爬虫
python crawlers/jd_crawler.py
python crawlers/taobao_crawler.py
python crawlers/douyin_crawler.py
```

## 输出结果

### 分析报告（`分析报告.txt`）

包含 6 个部分：整体统计、跨平台价格对比、折扣力度分析、销量 Top10 品牌、同品牌跨平台价差、性价比平台排行。

### 可视化图表（`charts/`）

| 文件 | 类型 | 说明 |
|------|------|------|
| `fig1_avg_price_bar.png` | 分组柱状图 | 三平台平均价格与中位数对比 |
| `fig2_price_distribution.png` | 堆叠直方图 | 三平台价格区间分布 |
| `fig3_brand_platform_price.png` | 横向柱状图 | Top10 品牌跨平台均价 |
| `fig4_price_boxplot.png` | 箱线图 | 三平台价格离散程度 |
| `fig5_price_vs_sales_scatter.png` | 散点图 | 价格 vs 销量关系 |

### 选购推荐示例

```
请输入你的预算上限(元): 3000
请输入偏好的品牌(多个用逗号分隔，回车跳过): 小米,荣耀
是否需要5G/折叠屏等高端机型？(y/n): y

推荐：在【抖音】购买【小米…】性价比最高！
```

## 常见问题

**Q：爬虫总是失败，只拿到样本数据？**
A：属正常现象，平台反爬机制较强。样本数据使用固定随机种子，可复现，不影响分析流程演示。

**Q：如何更换分析品类？**
A：修改 `config.py` 中的 `KEYWORD` 即可。

**Q：图表中文显示为方框？**
A：在 `analysis/visualize.py` 的 `font_names` 列表中加入本机已安装的中文字体名称。

**Q：如何增加数据量？**
A：调整 `config.py` 的 `PAGES_PER_PLATFORM`，以及 `crawlers/sample_data.py` 中的 `count` 参数。

更多细节见 [使用文档.md](使用文档.md)。

## 技术栈

Python 3 · requests · BeautifulSoup4 · pandas · numpy · matplotlib · seaborn

## 免责声明

本项目仅用于学习与教学演示，爬取的数据仅供研究分析使用。请遵守目标网站的服务条款与相关法律法规，合理控制请求频率。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
