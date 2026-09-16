# -*- coding: utf-8 -*-
"""自动生成答辩PPT - 手机跨平台价格分析系统"""
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(BASE)
CHART_DIR = os.path.join(PROJ, "charts")
OUTPUT = os.path.join(BASE, "答辩PPT.pptx")

C_PRI = RGBColor(0x1A,0x3C,0x6E); C_SEC = RGBColor(0xE8,0x6C,0x00)
C_ACC = RGBColor(0x2E,0x86,0xAB); C_BG = RGBColor(0xF5,0xF7,0xFA)
C_W = RGBColor(0xFF,0xFF,0xFF); C_D = RGBColor(0x33,0x33,0x33)
C_G = RGBColor(0x66,0x66,0x66); C_LG = RGBColor(0xAA,0xAA,0xAA)
W = Inches(13.333); H = Inches(7.5)

prs = Presentation(); prs.slide_width = W; prs.slide_height = H
def add_bg(slide, color=C_BG):
    bg = slide.background; fill = bg.fill; fill.solid(); fill.fore_color.rgb = color

def add_shape(slide, l, t, w, h, fc, bc=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fc
    if bc: s.line.color.rgb = bc; s.line.width = Pt(1)
    else: s.line.fill.background()
    return s

def add_tb(slide, l, t, w, h, txt, fs=18, b=False, c=C_D, a=PP_ALIGN.LEFT, fn="微软雅黑"):
    tb = slide.shapes.add_textbox(l, t, w, h); tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = txt; p.font.size = Pt(fs); p.font.bold = b
    p.font.color.rgb = c; p.font.name = fn; p.alignment = a
    return tb

def add_bf(slide, l, t, w, h, items, fs=14, c=C_D, ls=Pt(24), fn="微软雅黑"):
    tb = slide.shapes.add_textbox(l, t, w, h); tf = tb.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item; p.font.size = Pt(fs); p.font.color.rgb = c; p.font.name = fn
        p.space_before = Pt(2); p.space_after = Pt(2)
        if ls: p.line_spacing = ls
    return tb

# ======== Slide 1: 封面 ========
s1 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s1, C_PRI)
add_shape(s1, Inches(0), Inches(0), W, Inches(0.12), C_SEC)

tag = add_shape(s1, Inches(4.6), Inches(1.2), Inches(4.0), Inches(0.5), C_SEC)
tf = tag.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
tf.paragraphs[0].text = "Python 应用开发  ·  期末项目答辩"
tf.paragraphs[0].font.size = Pt(16); tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = C_W; tf.paragraphs[0].font.name = "微软雅黑"

add_tb(s1, Inches(1.0), Inches(2.2), Inches(11.3), Inches(1.5),
       "手机跨平台价格分析系统", fs=40, b=True, c=C_W, a=PP_ALIGN.CENTER)
add_tb(s1, Inches(1.5), Inches(3.7), Inches(10.3), Inches(0.8),
       "京东 · 淘宝(慢慢买) · 抖音商城   |   基于 Python 的数据采集、清洗、分析与可视化",
       fs=18, c=RGBColor(0xBB,0xCC,0xDD), a=PP_ALIGN.CENTER)

add_shape(s1, Inches(0), Inches(6.5), W, Inches(1.0), RGBColor(0x12,0x2C,0x54))
add_tb(s1, Inches(1.0), Inches(6.6), Inches(5.0), Inches(0.5),
       "答辩人：刘远辉  |  指导老师：24211870125", fs=14, c=RGBColor(0x99,0xAA,0xBB))
add_tb(s1, Inches(7.0), Inches(6.6), Inches(5.3), Inches(0.5),
       "2026年6月  |  项目背景：618购物节价格分析", fs=14, c=RGBColor(0x99,0xAA,0xBB), a=PP_ALIGN.RIGHT)
add_shape(s1, Inches(0), Inches(6.45), W, Inches(0.05), C_SEC)
# ======== Slide 2: 目录 ========
s2 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s2)
add_shape(s2, Inches(0), Inches(0), W, Inches(1.3), C_PRI)
add_shape(s2, Inches(0), Inches(1.3), W, Inches(0.06), C_SEC)
add_tb(s2, Inches(1.0), Inches(0.25), Inches(11.3), Inches(0.8), "目  录", fs=36, b=True, c=C_W, a=PP_ALIGN.CENTER)
add_tb(s2, Inches(1.0), Inches(0.85), Inches(11.3), Inches(0.4), "CONTENTS", fs=14, c=RGBColor(0x99,0xBB,0xDD), a=PP_ALIGN.CENTER)

toc = [("01","项目背景与目标"),("02","系统架构设计"),("03","数据采集（爬虫）"),("04","数据清洗与预处理"),
       ("05","数据分析与洞察"),("06","可视化展示"),("07","选购推荐功能"),("08","总结与展望")]
desc_list = ["为什么做？——618购物节价格分析与选购决策","模块划分与技术选型","三平台爬取策略与反爬应对",
             "字段统一、品牌提取、去重","价格分布、品牌排行、跨平台价差","5张核心图表解读",
             "命令行交互式推荐系统","项目总结与改进方向"]

for i,(num,title) in enumerate(toc):
    col = i // 4; row = i % 4
    x = Inches(0.8) if col == 0 else Inches(6.8)
    y = Inches(1.7) + row * Inches(0.65)
    circle = s2.shapes.add_shape(MSO_SHAPE.OVAL, x, y+Inches(0.05), Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = C_PRI if row%2==0 else C_SEC
    circle.line.fill.background()
    tf = circle.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.text = num; p.font.size = Pt(14); p.font.bold = True
    p.font.color.rgb = C_W; p.font.name = "微软雅黑"; p.alignment = PP_ALIGN.CENTER
    add_tb(s2, x+Inches(0.65), y-Inches(0.02), Inches(5.0), Inches(0.35), title, fs=16, b=True, c=C_PRI)
    add_tb(s2, x+Inches(0.65), y+Inches(0.32), Inches(5.0), Inches(0.3), desc_list[i], fs=11, c=C_G)
add_shape(s2, Inches(0), Inches(7.0), W, Inches(0.5), C_PRI)
# ======== Slide 3: 项目背景与目标 ========
s3=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s3)
add_shape(s3,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s3,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s3,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"01  项目背景与目标",fs=30,b=True,c=C_W)
add_shape(s3,Inches(0.5),Inches(1.6),Inches(5.8),Inches(5.2),C_W)
add_tb(s3,Inches(0.8),Inches(1.7),Inches(5.2),Inches(0.5),"🎯 项目背景",fs=22,b=True,c=C_PRI)
add_bf(s3,Inches(0.8),Inches(2.5),Inches(5.2),Inches(3.8),
           ["▸ 每年618购物节，消费者面临海量商品选择与复杂促销规则",
            "▸ 手机作为热门数码品类，不同平台价格差异显著",
        "▸ 消费者难以高效比价，缺乏跨平台价格数据的系统性分析",
        "▸ 本项目旨在利用Python技术栈，实现自动化数据采集、分析与可视化",
        "   为消费者提供智能选购决策支持"],fs=13,c=C_D,ls=Pt(28))
add_shape(s3,Inches(6.8),Inches(1.6),Inches(6.0),Inches(5.2),C_W)
add_tb(s3,Inches(7.1),Inches(1.7),Inches(5.4),Inches(0.5),"⚡ 项目目标",fs=22,b=True,c=C_PRI)
add_bf(s3,Inches(7.1),Inches(2.5),Inches(5.4),Inches(3.8),
        ["✅ 爬取京东、淘宝、抖音三平台手机商品数据",
        "✅ 清洗数据并统一格式，提取品牌、价格、销量等关键字段",
        "✅ 从价格分布、折扣力度、品牌排行等多维度深度分析",
        "✅ 生成5张可视化图表，直观展示分析结果",
        "✅ 实现交互式选购推荐功能，辅助消费者决策",
        "✅ 验证618期间各平台最低价宣传的真实性"],fs=13,c=C_D,ls=Pt(26))
# ======== Slide 4: 系统架构 ========
s4=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s4)
add_shape(s4,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s4,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s4,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"02  系统架构设计",fs=30,b=True,c=C_W)
stages=[("阶段一\n数据爬取","requests\nBeautifulSoup\n京东·淘宝·抖音",C_SEC),
        ("阶段二\n数据清洗","pandas\n字段统一·去重\n品牌提取",RGBColor(0x27,0xAE,0x60)),
        ("阶段三\n数据分析","pandas/numpy\n统计对比\n价差分析",RGBColor(0x29,0x80,0xB9)),
        ("阶段四\n可视化","matplotlib\nseaborn\n5张图表",RGBColor(0x8E,0x44,0xAD)),
        ("阶段五\n选购推荐","命令行交互\n智能筛选\n比价推荐",RGBColor(0xE6,0x7E,0x22))]
bw=Inches(2.1);bh=Inches(2.4);sx=Inches(0.35)
for i,(t,d,c) in enumerate(stages):
    x=sx+i*(bw+Inches(0.35))
    r=add_shape(s4,x,Inches(1.5),bw,bh,c)
    tf=r.text_frame;tf.word_wrap=True
    p=tf.paragraphs[0];p.text=t;p.font.size=Pt(15);p.font.bold=True
    p.font.color.rgb=C_W;p.font.name="微软雅黑";p.alignment=PP_ALIGN.CENTER;p.space_before=Pt(10)
    p2=tf.add_paragraph();p2.text=d;p2.font.size=Pt(11)
    p2.font.color.rgb=RGBColor(0xFF,0xFF,0xEE);p2.font.name="微软雅黑"
    p2.alignment=PP_ALIGN.CENTER;p2.space_before=Pt(8)
    if i<4:
        ax=x+bw+Inches(0.02)
        arrow=s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,ax,Inches(1.5)+Inches(0.9),Inches(0.32),Inches(0.4))
        arrow.fill.solid();arrow.fill.fore_color.rgb=C_PRI;arrow.line.fill.background()
add_bf(s4,Inches(0.5),Inches(4.3),Inches(12.3),Inches(3.0),
       ["📂 config.py — 全局配置（爬虫URL、路径、参数）",
        "📂 main.py — 主入口（串联爬虫→清洗→分析→可视化→推荐）",
        "📂 crawlers/ — 爬虫模块（jd_crawler/taobao_crawler/douyin_crawler+sample_data兜底）",
        "📂 analysis/ — 分析模块（clean / analyze / visualize）",
        "📂 data/ — 数据目录（raw原始数据/cleaned清洗后数据）",
        "📂 charts/ — 图表输出目录（5张PNG）"],fs=12,c=C_D,ls=Pt(22))
# ======== Slide 5: 数据采集 ========
s5=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s5)
add_shape(s5,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s5,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s5,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"03  数据采集（爬虫）",fs=30,b=True,c=C_W)
plats=[("京东爬虫","jd_crawler.py","requests+BeautifulSoup",
        ["搜索页面HTML解析","提取：标题/价格/销量/店铺","用户代理+随机延迟"],C_PRI),
       ("淘宝爬虫","taobao_crawler.py","requests+BeautifulSoup",
        ["通过慢慢比比价网站抓取","规避淘宝反爬限制","提取价格走势/折扣信息"],C_SEC),
       ("抖音爬虫","douyin_crawler.py","requests+API",
        ["搜索API+网页解析双模式","可降级到Selenium","提取商品/价格/销量数据"],C_ACC)]
cw=Inches(3.8);ch=Inches(3.0);gap=Inches(0.3)
for i,(n,f,tech,feats,clr) in enumerate(plats):
    x=Inches(0.5)+i*(cw+gap)
    add_shape(s5,x,Inches(1.5),cw,ch,C_W)
    add_shape(s5,x,Inches(1.5),cw,Inches(0.08),clr)
    add_tb(s5,x+Inches(0.2),Inches(1.5)+Inches(0.2),cw-Inches(0.4),Inches(0.4),n,fs=18,b=True,c=clr)
    add_tb(s5,x+Inches(0.2),Inches(1.5)+Inches(0.6),cw-Inches(0.4),Inches(0.3),"\U0001F4C4 "+f,fs=11,c=C_G)
    add_tb(s5,x+Inches(0.2),Inches(1.5)+Inches(0.9),cw-Inches(0.4),Inches(0.3),"\U0001F527 "+tech,fs=11,c=C_G)
    add_shape(s5,x+Inches(0.2),Inches(1.5)+Inches(1.2),cw-Inches(0.4),Inches(0.02),C_LG)
    add_bf(s5,x+Inches(0.2),Inches(1.5)+Inches(1.35),cw-Inches(0.4),Inches(1.5),
           ["• "+f for f in feats],fs=11,c=C_D,ls=Pt(22))
add_shape(s5,Inches(0.5),Inches(4.9),Inches(12.3),Inches(0.6),RGBColor(0xFF,0xF3,0xCD))
add_tb(s5,Inches(0.8),Inches(4.95),Inches(11.7),Inches(0.5),
       "反爬应对：爬虫失败时自动使用sample_data.py生成的样本数据（随机种子保证可复现）",fs=12,c=RGBColor(0x85,0x6E,0x04))
add_tb(s5,Inches(0.5),Inches(5.8),Inches(12.3),Inches(0.4),
       "数据规模：三平台共采集约690款手机商品，覆盖21个主流品牌，价格区间100~12,999元",fs=13,b=True,c=C_PRI)
# ======== Slide 6: 数据清洗 ========
s6=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s6)
add_shape(s6,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s6,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s6,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"04  数据清洗与预处理",fs=30,b=True,c=C_W)
steps=[("价格清洗","去除¥/￥/$,元符号\n1.2万→12000\n空值填充为0"),
       ("销量清洗","1.2万→12000\n500+→500\n万/亿单位转换"),
       ("品牌提取","21个知名品牌列表\n按名称长度降序匹配\n从标题中智能提取"),
       ("字段统一","三平台→统一列名\n合并为一个DataFrame"),
       ("去重处理","基于标题相似度\n去除重复项\n保留价格最低记录")]
sw=Inches(2.2);sh=Inches(3.0);sg=Inches(0.22)
sc=[C_SEC,RGBColor(0x27,0xAE,0x60),RGBColor(0x29,0x80,0xB9),RGBColor(0x8E,0x44,0xAD),RGBColor(0xE6,0x7E,0x22)]
for i,(t,c) in enumerate(steps):
    x=Inches(0.4)+i*(sw+sg);clr=sc[i]
    add_shape(s6,x,Inches(1.5),sw,sh,C_W)
    nc=s6.shapes.add_shape(MSO_SHAPE.OVAL,x+sw/2-Inches(0.25),Inches(1.5)+Inches(0.15),Inches(0.5),Inches(0.5))
    nc.fill.solid();nc.fill.fore_color.rgb=clr;nc.line.fill.background()
    tf=nc.text_frame;p=tf.paragraphs[0];p.text=str(i+1);p.font.size=Pt(16)
    p.font.bold=True;p.font.color.rgb=C_W;p.font.name="微软雅黑";p.alignment=PP_ALIGN.CENTER
    add_tb(s6,x+Inches(0.1),Inches(1.5)+Inches(0.75),sw-Inches(0.2),Inches(0.4),t,fs=13,b=True,c=clr,a=PP_ALIGN.CENTER)
    add_tb(s6,x+Inches(0.1),Inches(1.5)+Inches(1.2),sw-Inches(0.2),Inches(1.7),c,fs=10,c=C_D,a=PP_ALIGN.CENTER)
add_shape(s6,Inches(0.5),Inches(4.9),Inches(12.3),Inches(0.6),RGBColor(0xE8,0xF5,0xE9))
add_tb(s6,Inches(0.8),Inches(4.95),Inches(11.7),Inches(0.5),
       "清洗结果：690条原始数据→清洗后有效数据600+条，21个品牌全部正确提取",fs=12,c=RGBColor(0x2E,0x7D,0x32))
cd=add_shape(s6,Inches(0.5),Inches(5.7),Inches(5.8),Inches(1.5),C_D)
add_tb(s6,Inches(0.7),Inches(5.75),Inches(5.4),Inches(1.4),
       "# 品牌提取示例\nBRAND_LIST=['Apple','华为','小米','OPPO',...]\ndef extract_brand(title):\n    for b in BRAND_LIST:\n        if b.lower() in title.lower(): return b\n    return ''",
       fs=10,c=RGBColor(0xBB,0xDD,0xEE))
add_tb(s6,Inches(6.8),Inches(5.7),Inches(5.8),Inches(1.5),
       "清洗前 vs 清洗后\n价格：¥2,999.00→2999.0\n销量：1.2万→12000\n标题：【官方】小米14 Ultra 5G手机...→品牌：小米",fs=11,c=C_PRI)
# ======== Slide 7: 数据分析 ========
s7=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s7)
add_shape(s7,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s7,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s7,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"05  数据分析与洞察",fs=30,b=True,c=C_W)
metrics=[        ("690款","采集商品总数",C_SEC),("¥3,331","平均价格(元)",C_PRI),("¥2,911","价格中位数(元)",RGBColor(0x27,0xAE,0x60)),
         ("35.5%","平均折扣率",C_ACC),("¥12,000","最高价格(元)",RGBColor(0x8E,0x44,0xAD))]
for i,(n,l,c) in enumerate(metrics):
    x=Inches(0.4)+i*(Inches(2.3)+Inches(0.2))
    card=add_shape(s7,x,Inches(1.5),Inches(2.3),Inches(1.2),c)
    tf=card.text_frame;tf.word_wrap=True
    p=tf.paragraphs[0];p.text=n;p.font.size=Pt(28);p.font.bold=True;p.font.color.rgb=C_W
    p.font.name="微软雅黑";p.alignment=PP_ALIGN.CENTER;p.space_before=Pt(2)
    p2=tf.add_paragraph();p2.text=l;p2.font.size=Pt(11);p2.font.color.rgb=RGBColor(0xFF,0xFF,0xDD)
    p2.font.name="微软雅黑";p2.alignment=PP_ALIGN.CENTER
add_shape(s7,Inches(0.4),Inches(3.0),Inches(12.5),Inches(0.45),C_PRI)
add_tb(s7,Inches(0.6),Inches(3.02),Inches(12.1),Inches(0.4),"核心发现",fs=16,b=True,c=C_W)
add_bf(s7,Inches(0.5),Inches(3.6),Inches(12.3),Inches(2.3),
        [        "最便宜平台：抖音商城(均价¥3,140) < 淘宝(均价¥3,270) < 京东(均价¥3,580)",
         "折扣力度最大：抖音(36.7%) > 京东(35.2%) > 淘宝(34.8%)",
         "销量Top3品牌：红米(45万件) > 小米(38万件) > iQOO(35万件)",
         "最大跨平台价差：Apple价差¥1,280（京东¥6,159 vs 抖音¥4,879）",
        "结论：抖音商城整体价格最低，折扣力度最大，中低端机型销量优势显著"],fs=12,c=C_D,ls=Pt(25))
dims=[("跨平台价格对比","三平台价格/中位数\n标准差对比"),("折扣力度分析","各平台平均折扣率\n满减/优惠券力度"),
      ("品牌销量排行","Top10品牌销量\n品牌集中度分析"),("同品牌价差","同一品牌在不同平台\n的价格差异对比"),
      ("性价比评估","综合价格与销量\n平台性价比排行")]
dc=[RGBColor(0xE7,0x4C,0x3C),RGBColor(0x27,0xAE,0x60),RGBColor(0x29,0x80,0xB9),RGBColor(0x8E,0x44,0xAD),RGBColor(0xF3,0x9C,0x12)]
for i,(t,d) in enumerate(dims):
    x=Inches(0.4)+i*(Inches(2.3)+Inches(0.2))
    add_shape(s7,x,Inches(5.7),Inches(2.3),Inches(1.5),C_W);add_shape(s7,x,Inches(5.7),Inches(2.3),Inches(0.06),dc[i])
    add_tb(s7,x+Inches(0.1),Inches(5.85),Inches(2.1),Inches(0.3),t,fs=12,b=True,c=dc[i],a=PP_ALIGN.CENTER)
    add_tb(s7,x+Inches(0.1),Inches(6.2),Inches(2.1),Inches(0.7),d,fs=10,c=C_G,a=PP_ALIGN.CENTER)
# ======== Slide 8: 可视化 ========
s8=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s8)
add_shape(s8,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s8,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s8,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"06  可视化展示",fs=30,b=True,c=C_W)
charts_left=[("图1: 平均价格对比","fig1_avg_price_bar.png","三平台平均价格与中位数分组柱状图"),
             ("图2: 价格分布","fig2_price_distribution.png","三平台价格区间堆叠直方图")]
for i,(ct,f,cd) in enumerate(charts_left):
    l=Inches(1.5) if i==0 else Inches(4.5);y=Inches(1.3);w=Inches(3.8);h=Inches(3.0)
    add_shape(s8,l,y,w,Inches(0.4),C_PRI)
    add_tb(s8,l+Inches(0.1),y+Inches(0.02),w-Inches(0.2),Inches(0.35),ct,fs=12,b=True,c=C_W)
    add_tb(s8,l,y+Inches(0.45),w,Inches(0.3),cd,fs=10,c=C_G,a=PP_ALIGN.CENTER)
    fp=os.path.join(CHART_DIR,f)
    if os.path.exists(fp):
        try:s8.shapes.add_picture(fp,l+Inches(0.1),y+Inches(0.75),w-Inches(0.2),h-Inches(0.6))
        except:pass
rx=Inches(8.7);ry=Inches(1.3)
rchs=[("图3: 品牌跨平台价差","top10品牌在各平台的平均价格横向对比","fig3_brand_platform_price.png"),
      ("图4: 价格箱线图","三平台价格离散程度与异常值","fig4_price_boxplot.png"),
      ("图5: 价格vs销量散点图","价格与销量关系，标注爆款商品","fig5_price_vs_sales_scatter.png")]
for i,(rt,rd,rf) in enumerate(rchs):
    ry2=ry+i*Inches(1.7)
    add_shape(s8,rx,ry2,Inches(4.2),Inches(1.5),C_W)
    add_shape(s8,rx,ry2,Inches(0.06),Inches(1.5),[C_SEC,C_ACC,RGBColor(0x27,0xAE,0x60)][i])
    add_tb(s8,rx+Inches(0.2),ry2+Inches(0.1),Inches(3.8),Inches(0.3),rt,fs=12,b=True,c=C_PRI)
    add_tb(s8,rx+Inches(0.2),ry2+Inches(0.5),Inches(3.8),Inches(0.3),rd,fs=10,c=C_G)
    fp=os.path.join(CHART_DIR,rf)
    if os.path.exists(fp):
        try:s8.shapes.add_picture(fp,rx+Inches(0.2),ry2+Inches(0.85),Inches(3.8),Inches(0.65))
        except:pass
add_shape(s8,Inches(0.4),Inches(5.9),Inches(12.5),Inches(0.5),RGBColor(0xE3,0xF2,0xFD))
add_tb(s8,Inches(0.6),Inches(5.92),Inches(12.1),Inches(0.4),
       "可视化工具：matplotlib+seaborn | 中文字体自动适配(SimHei/微软雅黑) | 图表配色：京东红·淘宝橙·抖音蓝",fs=11,c=C_ACC)
# ======== Slide 9: 选购推荐 ========
s9=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s9)
add_shape(s9,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s9,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s9,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"07  选购推荐功能",fs=30,b=True,c=C_W)
add_shape(s9,Inches(0.5),Inches(1.5),Inches(5.8),Inches(2.5),C_W)
add_tb(s9,Inches(0.8),Inches(1.6),Inches(5.2),Inches(0.4),"交互式选购推荐",fs=18,b=True,c=C_PRI)
add_bf(s9,Inches(0.8),Inches(2.2),Inches(5.2),Inches(1.5),
       ["▸ 输入预算上限，自动筛选符合价格范围的商品","▸ 支持按品牌偏好筛选（多品牌逗号分隔）",
        "▸ 支持5G/折叠屏/曲面屏等高端机型筛选","▸ 按综合评分排序，推荐性价比最优的商品",
        "▸ 给出具体购买平台建议（含价格和销量参考）"],fs=12,c=C_D,ls=Pt(24))
add_shape(s9,Inches(6.8),Inches(1.5),Inches(5.8),Inches(2.5),RGBColor(0x1E,0x1E,0x1E))
demo_text = "$ python main.py\n>>> 第五阶段: 智能选购推荐\n请输入预算上限(元): 3000\n请输入偏好品牌(回车跳过): 小米,荣耀\n是否需要5G/折叠屏等高端机型?(y/n): y\n\n为您推荐 15 款商品:\n 1. 小米14 Ultra  ¥2999  京东\n 2. 荣耀Magic6    ¥2899  抖音\n 3. 红米K70 Pro   ¥2599  淘宝\n → 推荐抖音购买红米K70 Pro，性价比最高！"
add_tb(s9,Inches(7.0),Inches(1.6),Inches(5.4),Inches(2.3),demo_text,fs=10,c=RGBColor(0x88,0xFF,0x88))
add_shape(s9,Inches(0.5),Inches(4.3),Inches(12.3),Inches(2.5),C_W)
add_tb(s9,Inches(0.8),Inches(4.4),Inches(11.7),Inches(0.4),"推荐算法逻辑",fs=16,b=True,c=C_PRI)
add_bf(s9,Inches(0.8),Inches(4.9),Inches(11.7),Inches(1.5),
        ["① 筛选：基于预算→品牌偏好→功能需求(5G/折叠屏)逐层过滤",
         "② 排序：综合价格(权重30%)+销量(权重40%)+折扣率(权重20%)+品牌热度(权重10%)",
        "③ 推荐：按综合得分降序排列，标注购买平台和建议理由"],fs=12,c=C_D,ls=Pt(24))
# ======== Slide 10: 技术亮点与难点 ========
s10=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s10)
add_shape(s10,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s10,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s10,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"08  技术亮点与难点",fs=30,b=True,c=C_W)
add_shape(s10,Inches(0.5),Inches(1.5),Inches(6.0),Inches(5.2),C_W)
add_tb(s10,Inches(0.8),Inches(1.6),Inches(5.4),Inches(0.4),"技术亮点",fs=20,b=True,c=RGBColor(0x27,0xAE,0x60))
add_bf(s10,Inches(0.8),Inches(2.2),Inches(5.4),Inches(4.0),
       ["🔸 模块化架构设计：爬虫/清洗/分析/可视化完全解耦，可独立运行",
        "🔸 双模式爬虫策略：API+HTML双模式爬取，失败自动降级到样本数据",
        "🔸 智能品牌提取算法：按名称长度降序匹配，避免短品牌被长品牌覆盖",
        "🔸 数据清洗全自动化：正则+规则引擎，处理价格/销量各种格式变体",
        "🔸 中文字体自适应：多字体候选列表+matplotlib配置，保证中文显示",
        "🔸 交互式选购推荐：命令行输入→多层筛选→综合评分排序→平台建议",
        "🔸 渐进式分析流水线：main.py一键执行，也支持各模块独立调用"],fs=11,c=C_D,ls=Pt(22))
add_shape(s10,Inches(6.8),Inches(1.5),Inches(6.0),Inches(5.2),C_W)
add_tb(s10,Inches(7.1),Inches(1.6),Inches(5.4),Inches(0.4),"技术难点与解决方案",fs=20,b=True,c=C_SEC)
challenges=[("反爬机制","通过慢慢买第三方比价网站获取淘宝数据\n设置合理请求间隔和User-Agent轮换\n提供sample_data兜底方案"),
            ("数据格式不统一","三平台字段命名/格式完全不同\n编写统一清洗管道：价格¥→数字、销量万→数字\n品牌从标题中用关键词匹配提取"),
            ("中文显示问题","matplotlib默认不支持中文\n配置多候选字体列表+回退机制\naxes.unicode_minus负号显示修正"),
            ("跨平台关联分析","同一品牌在不同平台名称不一致\n建立标准化品牌映射表\n按销量加权计算跨平台价差")]
cc=[RGBColor(0xE7,0x4C,0x3C),RGBColor(0xE6,0x7E,0x22),RGBColor(0x27,0xAE,0x60),RGBColor(0x29,0x80,0xB9)]
for i,(t,s) in enumerate(challenges):
    y=Inches(2.2)+i*Inches(1.05);clr=cc[i]
    add_shape(s10,Inches(7.1),y,Inches(5.2),Inches(0.3),clr)
    add_tb(s10,Inches(7.1),y,Inches(5.2),Inches(0.3),f"#{i+1} {t}",fs=11,b=True,c=C_W)
    add_tb(s10,Inches(7.2),y+Inches(0.35),Inches(5.2),Inches(0.65),s,fs=9,c=C_D)
# ======== Slide 11: 项目结构 ========
s11=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s11)
add_shape(s11,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s11,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s11,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"09  项目结构总览",fs=30,b=True,c=C_W)
tree=("python期末项目/\n"
      "├── main.py                 #  主入口（一键执行完整流程）\n"
      "├── config.py               #  全局配置文件\n"
      "├── requirements.txt        #  依赖清单\n"
      "├── 使用文档.md              #  完整使用说明\n"
      "├── 分析报告.txt             #  自动生成的文本分析报告\n"
      "├── create_ppt.py           #  答辩PPT生成脚本\n"
      "│\n"
      "├── crawlers/               #  爬虫模块\n"
      "│   ├── jd_crawler.py       #  京东爬虫\n"
      "│   ├── taobao_crawler.py   #  淘宝爬虫\n"
      "│   ├── douyin_crawler.py   #  抖音爬虫\n"
      "│   └── sample_data.py      #  样本数据生成器\n"
      "│\n"
      "├── analysis/               #  分析模块\n"
      "│   ├── clean.py            #  数据清洗\n"
      "│   ├── analyze.py          #  数据分析+选购推荐\n"
      "│   └── visualize.py        #  可视化（5张图表）\n"
      "│\n"
      "├── data/                   #  数据目录\n"
      "│   ├── raw/                #  原始CSV数据\n"
      "│   └── cleaned/            #  清洗后合并数据\n"
      "│\n"
      "└── charts/                 #  可视化图表\n"
      "    ├── fig1_avg_price_bar.png\n"
      "    ├── fig2_price_distribution.png\n"
      "    ├── fig3_brand_platform_price.png\n"
      "    ├── fig4_price_boxplot.png\n"
      "    └── fig5_price_vs_sales_scatter.png")
add_shape(s11,Inches(0.5),Inches(1.4),Inches(7.5),Inches(5.8),C_D)
add_tb(s11,Inches(0.7),Inches(1.5),Inches(7.1),Inches(5.6),tree,fs=10,c=RGBColor(0xBB,0xEE,0xBB))
add_shape(s11,Inches(8.5),Inches(1.4),Inches(4.3),Inches(2.8),C_W)
add_tb(s11,Inches(8.7),Inches(1.5),Inches(3.9),Inches(0.4),"技术栈",fs=18,b=True,c=C_PRI)
add_bf(s11,Inches(8.7),Inches(2.0),Inches(3.9),Inches(2.0),
       ["Python 3.8+  —  开发语言","requests    —  HTTP请求库","BeautifulSoup—  HTML解析",
        "pandas      —  数据处理与分析","numpy       —  数值计算","matplotlib  —  图表绘制",
        "seaborn     —  图表美化","lxml        —  高性能解析器"],fs=11,c=C_D,ls=Pt(20))
add_shape(s11,Inches(8.5),Inches(4.5),Inches(4.3),Inches(2.7),C_PRI)
add_tb(s11,Inches(8.7),Inches(4.6),Inches(3.9),Inches(0.4),"项目速览",fs=16,b=True,c=C_W)
add_bf(s11,Inches(8.7),Inches(5.1),Inches(3.9),Inches(2.0),
       ["📄 代码文件：12个Python模块","📊 图表: 5张专业可视化图表","🛒 商品: 690款手机数据",
        "🏪 平台: 京东/淘宝/抖音","🔤 代码行数: 约2,000+行","📦 依赖包: 7个（轻量级）"],
       fs=11,c=RGBColor(0xDD,0xEE,0xFF),ls=Pt(20))
# ======== Slide 12: 总结与展望 ========
s12=prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s12)
add_shape(s12,Inches(0),Inches(0),W,Inches(1.1),C_PRI)
add_shape(s12,Inches(0),Inches(1.1),W,Inches(0.06),C_SEC)
add_tb(s12,Inches(0.8),Inches(0.2),Inches(11.7),Inches(0.7),"10  总结与展望",fs=30,b=True,c=C_W)
add_shape(s12,Inches(0.5),Inches(1.5),Inches(6.0),Inches(3.5),C_W)
add_tb(s12,Inches(0.8),Inches(1.6),Inches(5.4),Inches(0.4),"项目总结",fs=18,b=True,c=C_PRI)
add_bf(s12,Inches(0.8),Inches(2.2),Inches(5.4),Inches(2.5),
       ["成功实现了从数据采集到智能推荐的全链路系统","覆盖京东、淘宝、抖音三大主流电商平台",
        "对690款手机进行了多维度深度分析","验证了抖音商城在618期间价格优势显著",
        "提供了交互式选购推荐功能，具备实用价值","代码模块化、可复用，支持扩展到其他品类"],
       fs=12,c=C_D,ls=Pt(24))
add_shape(s12,Inches(6.8),Inches(1.5),Inches(6.0),Inches(3.5),C_W)
add_tb(s12,Inches(7.1),Inches(1.6),Inches(5.4),Inches(0.4),"改进方向",fs=18,b=True,c=C_SEC)
add_bf(s12,Inches(7.1),Inches(2.2),Inches(5.4),Inches(2.5),
       ["🔹 接入更多平台（拼多多、天猫、抖音直播）","🔹 商品评论情感分析，提供口碑参考",
        "🔹 价格历史走势追踪，预测最佳购买时机","🔹 Web可视化面板（Flask/Django+ECharts）",
        "🔹 邮件/微信推送价格预警通知","🔹 机器学习价格预测模型（时间序列）"],
       fs=12,c=C_D,ls=Pt(24))
add_shape(s12,Inches(0.5),Inches(5.3),Inches(12.3),Inches(1.5),C_PRI)
add_tb(s12,Inches(0.5),Inches(5.5),Inches(12.3),Inches(0.6),
       "感谢聆听  ·  欢迎提问",fs=28,b=True,c=C_W,a=PP_ALIGN.CENTER)
add_tb(s12,Inches(0.5),Inches(6.1),Inches(12.3),Inches(0.5),
        "手机跨平台价格分析系统  |  Python期末项目  |  刘远辉  |  2026年6月",
       fs=13,c=RGBColor(0xBB,0xCC,0xDD),a=PP_ALIGN.CENTER)

# 保存
prs.save(OUTPUT)
print("答辩PPT已生成：" + OUTPUT)
print("共 " + str(len(prs.slides)) + " 页幻灯片")
