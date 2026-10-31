"""Public version of the U-Net group-meeting deck: all figures self-made (see make_figures.py).

Run: uv run --no-project --with python-pptx python -I build_zh.py <out-dir> <figures-dir>
"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = Path(sys.argv[1])
FIG = Path(sys.argv[2])

# Palette: microscopy slate + cell teal, one coral accent
INK = RGBColor(0x1F, 0x2D, 0x3A)
SLATE = RGBColor(0x1F, 0x3A, 0x4D)
TEAL = RGBColor(0x2A, 0x9D, 0x8F)
TEAL_LIGHT = RGBColor(0xE3, 0xF2, 0xF0)
CORAL = RGBColor(0xE7, 0x6F, 0x51)
CORAL_LIGHT = RGBColor(0xFB, 0xE9, 0xE4)
GREY = RGBColor(0x6B, 0x7A, 0x86)
GRID = RGBColor(0xD5, 0xDD, 0xE2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xF4, 0xF7, 0xF8)

HEAD, BODY, EA = "Cambria", "Calibri", "Microsoft YaHei"
SRC = "Ronneberger, Fischer, Brox. U-Net. MICCAI 2015, arXiv:1505.04597"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def font(run, size, bold=False, color=INK, head=False, italic=False):
    f = run.font
    f.size, f.bold, f.italic = Pt(size), bold, italic
    f.color.rgb = color
    f.name = HEAD if head else BODY
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", EA)


def text(slide, x, y, w, h, paras, size=16, color=INK, bold=False, head=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=6, name=None):
    """paras: list of str or list of (str, opts) runs per paragraph."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space)
        runs = [(p, {})] if isinstance(p, str) else p
        for t, o in runs:
            r = para.add_run()
            r.text = t
            font(r, o.get("size", size), o.get("bold", bold), o.get("color", color),
                 o.get("head", head), o.get("italic", False))
    return tb


def box(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, name=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1.5)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def badge(slide, x, y, label, fill=TEAL, d=0.5, size=16):
    c = box(slide, x, y, d, d, fill, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    font(r, size, True, WHITE)
    return c


def slide_base(title, dark=False):
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = SLATE if dark else WHITE
    if title:
        text(s, 0.6, 0.45, 12.1, 0.9, [title], size=30, bold=True, head=True,
             color=WHITE if dark else INK, anchor=MSO_ANCHOR.MIDDLE, name="Title")
    return s


def source(slide, t, dark=False):
    text(slide, 0.6, 6.95, 12.1, 0.3, [t], size=10, color=GRID if dark else GREY, name="Source")


def notes(slide, t):
    slide.notes_slide.notes_text_frame.text = t


def picture(slide, path, x, y, w=None, h=None, name=None):
    kw = {}
    if w:
        kw["width"] = Inches(w)
    if h:
        kw["height"] = Inches(h)
    p = slide.shapes.add_picture(str(path), Inches(x), Inches(y), **kw)
    if name:
        p.name = name
    return p


# ---------- 1 title ----------
s = slide_base(None, dark=True)
text(s, 0.8, 0.9, 7.0, 0.4, ["组会论文报告 · 2026-10-31"], size=14, color=TEAL_LIGHT)
text(s, 0.8, 1.5, 6.6, 2.4, ["只有几十张标注图，也能训练出精细的分割网络"], size=40, bold=True,
     head=True, color=WHITE, name="Title")
text(s, 0.8, 4.15, 6.4, 1.2, [
    "U-Net: Convolutional Networks for Biomedical Image Segmentation",
    "Ronneberger, Fischer, Brox · MICCAI 2015 · arXiv:1505.04597",
], size=14, color=GRID)
box(s, 0.8, 5.45, 6.4, 1.2, RGBColor(0x2B, 0x4C, 0x63), radius=0.12)
text(s, 1.05, 5.6, 5.9, 0.9, [[("要解决的问题：", {"bold": True, "color": TEAL_LIGHT}),
                               ("训练图只有 20–35 张时，怎样给每个像素准确分类？", {"color": WHITE})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 7.75, 1.35, 4.95, 3.75, WHITE, radius=0.06)
picture(s, FIG / "fig1-unet.png", 7.95, 1.6, w=4.55, name="Fig1 thumbnail")
text(s, 7.75, 5.25, 4.95, 0.3, ["示意图：据论文图 1 重绘"], size=10, color=GRID)
notes(s, "核心论点：用 U 形网络（先缩小看整体，再放大定位，并把细节直接接过来），配合大量数据增强，"
         "只用很少的标注图像，就能训练出比滑动窗口方法更准的分割网络。")

# ---------- 2 sliding window ----------
s = slide_base("滑动窗口逐块判断：慢，而且“看得广”和“定得准”难两全")
n, cell, gx, gy = 9, 0.42, 0.9, 1.75
for i in range(n):
    for j in range(n):
        box(s, gx + j * cell, gy + i * cell, cell - 0.04, cell - 0.04, PALE, shape=MSO_SHAPE.RECTANGLE)
for (pi, pj, dash) in ((2, 1, False), (2, 2, True)):
    fr = box(s, gx + pj * cell - 0.03, gy + pi * cell - 0.03, 3 * cell + 0.02, 3 * cell + 0.02,
             WHITE, line=TEAL, shape=MSO_SHAPE.RECTANGLE)
    fr.fill.background()
    if dash:
        fr.line.dash_style = 4  # dash
    box(s, gx + (pj + 1) * cell, gy + (pi + 1) * cell, cell - 0.04, cell - 0.04,
        CORAL if not dash else CORAL_LIGHT, shape=MSO_SHAPE.RECTANGLE)
arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(gx + 1.5 * cell), Inches(gy + 1.55 * cell),
                               Inches(gx + 2.6 * cell), Inches(gy + 1.55 * cell))
arrow.line.color.rgb = CORAL
arrow.line.width = Pt(2.5)
arrow.line._get_or_add_ln().append(arrow.line._get_or_add_ln().makeelement(qn("a:tailEnd"), {"type": "triangle"}))
text(s, gx, gy + n * cell + 0.2, n * cell, 1.0, [
    [("■ ", {"color": CORAL}), ("中心像素：网络只判断它是哪一类", {})],
    [("□ ", {"color": TEAL}), ("小方块：挪一格，再截一块、再跑一遍", {})],
], size=14, space=4)
cx = 5.6
box(s, cx, 1.75, 6.9, 1.9, TEAL_LIGHT)
badge(s, cx + 0.3, 1.95, "1")
text(s, cx + 1.0, 1.95, 5.6, 1.6, [[("慢", {"bold": True, "size": 22})],
                                     "每个像素都单独跑一遍网络；相邻方块几乎完全重叠，大量重复计算"], size=16)
box(s, cx, 3.95, 6.9, 2.6, TEAL_LIGHT)
badge(s, cx + 0.3, 4.15, "2")
text(s, cx + 1.0, 4.15, 5.6, 2.3, [[("两难", {"bold": True, "size": 22})],
                                     [("方块大：", {"bold": True}), ("看得到更多周围，但要先缩小，定位变粗", {})],
                                     [("方块小：", {"bold": True}), ("定位准，但只看到很少的周围信息", {})]], size=16)
source(s, "来源：论文第 1–2 页；滑动窗口方法见 Ciresan et al., NIPS 2012。示意图为自绘")
notes(s, "滑动窗口不是 CNN 的别名：窗口里装的就是一个 CNN，每挪一格跑一次。U-Net 也是 CNN，区别在于整张图一次输入、一次输出。"
         "直觉上滑动窗口更精细，但方块一大就要缩小处理，中心像素的位置会变模糊——这是论文要推翻的直觉，结果页再核对。")

# ---------- 3 U-Net ----------
s = slide_base("U-Net = encoder–decoder + 每层跳跃连接，整张图一次输出")
picture(s, FIG / "fig1-unet.png", 0.6, 1.55, w=7.9, name="Fig1")
items = [
    (TEAL, "左边往下（encoder）", "一层层缩小：572×572 → 约 30×30，看清整体，位置变模糊"),
    (TEAL, "右边往上（decoder）", "一层层放大，最后给每个像素一个类别（输出 388×388）"),
    (CORAL, "灰色横线（跳跃连接）", "把缩小前的图复制过来拼上，找回清楚的边缘和位置"),
]
for k, (c, h, b) in enumerate(items):
    y = 1.6 + k * 1.75
    box(s, 8.85, y, 3.85, 1.5, TEAL_LIGHT if c == TEAL else CORAL_LIGHT)
    text(s, 9.1, y + 0.15, 3.4, 1.25, [[(h, {"bold": True, "color": c, "size": 17})], b], size=14, space=4)
source(s, "示意图：据论文图 1 的层尺寸重绘；原图见 " + SRC)
notes(s, "普通 encoder–decoder 只拿到最底层压缩后的信息，边缘会模糊；U-Net 每放大一层都拼上同一层未压缩的图。"
         "左右只是大致对称：拼接处通道数是 64×2=128，两次卷积后回到 64；尺寸上左边 568 要裁成 392（卷积不补边，每次少一圈）。"
         "输出 388×388 正好是输入 572×572 的正中间；大图用重叠分块，边缘镜像补齐。"
         "为什么不补边让输入输出一样大？可以，后来多数实现就这样做；作者的理由是不编造边缘像素、分块无缝，但论文没有对比实验。"
         "每次缩小通道翻倍是当时通用做法（如 VGG），论文没有解释，也没比较别的数字。")

# ---------- 4 augmentation ----------
s = slide_base("弹性形变把已有图变出新样子，不用再标注")
imgs = ["cells-original.png", "cells-elastic-1.png", "cells-elastic-2.png", "cells-elastic-3.png"]
caps = ["原图", "弹性形变 1", "弹性形变 2", "弹性形变 3"]
iw, gap, x0 = 2.75, 0.35, 0.6
for k, (f, c) in enumerate(zip(imgs, caps)):
    x = x0 + k * (iw + gap)
    picture(s, FIG / f, x, 1.6, w=iw, name=c)
    text(s, x, 1.6 + iw * 238 / 232 + 0.1, iw, 0.35, [c], size=14, bold=(k == 0),
         color=INK if k == 0 else TEAL, align=PP_ALIGN.CENTER)
box(s, 0.6, 5.25, 5.85, 1.45, PALE)
text(s, 0.85, 5.38, 5.4, 1.2, [[("问题：", {"bold": True, "color": CORAL}),
                                 ("训练图只有 20–35 张，网络容易背答案，换张新图就不行", {})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.85, 5.25, 5.85, 1.45, TEAL_LIGHT)
text(s, 7.1, 5.38, 5.4, 1.2, [[("办法：", {"bold": True, "color": TEAL}),
                                ("平移、旋转、灰度变化，加上随机弹性形变；组织是软的，真实切片里本来就有这种变形", {})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
source(s, "合成的细胞图；形变按论文描述生成（3×3 粗网格随机位移，双三次插值）；真实示例见论文图 3a")
notes(s, "U-Net 整张图输入，不能像滑动窗口那样切块增加样本，所以要把已有图变出新样子，标准答案跟着一起变。"
         "作者说弹性形变 'seem to be the key concept'——这只是作者的判断，论文没有做去掉弹性形变再比的实验。")

# ---------- 5 weighted loss ----------
s = slide_base("给细胞之间的窄缝加大权重，逼网络学会分开")
picture(s, FIG / "fig3-weights.png", 0.6, 1.5, w=12.1, name="Fig3")
fig3_h = 12.1 * 279 / 1209
cy = 1.5 + fig3_h + 0.45
cards = [
    (CORAL_LIGHT, CORAL, "问题", "网络只输出“细胞 / 背景”两种。两个细胞挨着时中间没有背景像素，输出连成一整块，看不出是几个"),
    (PALE, INK, "办法", "标准答案里在细胞之间画一条背景缝（图 c）；缝上的像素判错扣分更多（图 d，红黄 = 权重大）"),
    (TEAL_LIGHT, TEAL, "为什么要加权", "缝只有几个像素宽，不加权时判错几乎不扣分，网络会“变懒”忽略它"),
]
cw = (12.1 - 2 * 0.35) / 3
for k, (fill, col, h, b) in enumerate(cards):
    x = 0.6 + k * (cw + 0.35)
    box(s, x, cy, cw, 6.75 - cy, fill)
    text(s, x + 0.25, cy + 0.2, cw - 0.5, 6.75 - cy - 0.35, [[(h, {"bold": True, "color": col, "size": 18})], b],
         size=15, space=4)
source(s, "合成示例（a 图像，b 实例，c 带间隙的标签，d 按论文公式 2 计算的权重图）；原图见论文图 3；w0 = 10，σ ≈ 5 像素")
notes(s, "细胞本身的标签由挑战赛组织方提供（人工标注）；分隔缝由作者用形态学操作从已有标签自动算出，"
         "权重按到最近和第二近细胞的距离用公式算出。同一张权重图也用来平衡各类像素数量。")

# ---------- 6 mapping ----------
s = slide_base("每一部分对应一个原问题")
rows = [
    ("U 形网络 + 跳跃连接", "“看得广”和“定得准”难两全；逐块计算太慢", "整图一次算完，细节由跳跃连接找回"),
    ("弹性形变数据增强", "训练图只有 20–35 张，容易背答案", "见过更多真实可能的样子，不用再标注"),
    ("细胞间隙加权损失", "挨着的细胞连成一团", "逼网络学会细胞之间的窄缝"),
]
text(s, 1.4, 1.55, 3.6, 0.4, ["办法"], size=14, bold=True, color=GREY)
text(s, 5.3, 1.55, 3.6, 0.4, ["回应的原问题"], size=14, bold=True, color=GREY)
text(s, 9.2, 1.55, 3.5, 0.4, ["怎么起作用"], size=14, bold=True, color=GREY)
for k, (a, b, c) in enumerate(rows):
    y = 2.05 + k * 1.55
    badge(s, 0.6, y + 0.35, str(k + 1), d=0.6, size=18)
    box(s, 1.4, y, 3.6, 1.3, TEAL_LIGHT)
    text(s, 1.6, y, 3.2, 1.3, [a], size=17, bold=True, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 5.3, y, 3.6, 1.3, CORAL_LIGHT)
    text(s, 5.5, y, 3.2, 1.3, [b], size=15, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 9.2, y, 3.5, 1.3, PALE)
    text(s, 9.4, y, 3.1, 1.3, [c], size=15, anchor=MSO_ANCHOR.MIDDLE)
source(s, "来源：论文第 1–6 页")
notes(s, "这一页是“为什么有用”：三部分分别回应第 2 页的两难与慢、数据少、细胞粘连。注意这只是设计上的对应，各部分各自贡献多少，论文没有实验（见第 9 页）。")

# ---------- 7 evaluation ----------
s = slide_base("三个公开挑战赛，答案在组织方手里")
data = [("任务", "图像", "训练图", "指标"),
        ("神经结构分割\nISBI 2012", "电子显微镜\n果蝇幼虫神经组织", "30 张\n完整标注", "warping / Rand / pixel error\n越小越好"),
        ("细胞分割 PhC-U373\nISBI 2015", "相差显微镜\n脑肿瘤细胞", "35 张\n部分标注", "IOU\n越大越好"),
        ("细胞分割 DIC-HeLa\nISBI 2015", "微分干涉显微镜\nHeLa 细胞", "20 张\n部分标注", "IOU\n越大越好")]
tbl = s.shapes.add_table(4, 4, Inches(0.6), Inches(1.6), Inches(8.0), Inches(4.6)).table
for j, wdt in enumerate((2.3, 2.3, 1.3, 2.1)):
    tbl.columns[j].width = Inches(wdt)
for i, row in enumerate(data):
    tbl.rows[i].height = Inches(0.7 if i == 0 else 1.3)
    for j, val in enumerate(row):
        cell = tbl.cell(i, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SLATE if i == 0 else (PALE if i % 2 else WHITE)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.12)
        tf = cell.text_frame
        tf.word_wrap = True
        for k, line in enumerate(val.split("\n")):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = line
            font(r, 14 if i else 15, bold=(i == 0 or k == 0), color=WHITE if i == 0 else (INK if k == 0 else GREY))
box(s, 9.0, 1.6, 3.7, 4.6, TEAL_LIGHT)
badge(s, 9.3, 1.9, "!", fill=CORAL)
text(s, 9.3, 2.6, 3.15, 3.4, [
    [("测试集答案保密", {"bold": True, "size": 18})],
    "作者只能交预测结果，由组织方统一打分、排名",
    "→ 不能偷看答案调参数",
    "→ 所有队伍同一套试卷",
], size=15, space=8)
source(s, "来源：论文第 6–7 页；IOU = 重叠部分 ÷ 合起来的部分，1 表示完全重合")
notes(s, "对手是排行榜上的其他队伍，包括滑动窗口方法（Ciresan 等，榜上叫 IDSIA）。"
         "可信的是分数本身；但要打问号：电镜比赛可反复提交（脚注：一支队伍提交了 78 次），U-Net 提交次数没写；比的是整套方法；只有显微镜图像。")

# ---------- 8 results ----------
s = slide_base("不加后处理，U-Net 就好过滑动窗口")
text(s, 0.6, 1.5, 5.6, 0.4, ["电镜神经结构（ISBI 2012，越小越好）"], size=16, bold=True, color=GREY)
pairs = [("warping error", "0.000353", "0.000420", "U-Net 排第 1"), ("Rand error", "0.0382", "0.0504", "")]
for k, (m, u, b, note) in enumerate(pairs):
    y = 2.05 + k * 2.2
    box(s, 0.6, y, 5.6, 1.95, PALE)
    text(s, 0.85, y + 0.15, 5.1, 0.4, [m + ("  ·  " + note if note else "")], size=15, bold=True)
    text(s, 0.85, y + 0.6, 2.6, 1.2, [[(u, {"size": 30, "bold": True, "color": TEAL})], "U-Net"], size=14, space=0)
    text(s, 3.45, y + 0.6, 2.6, 1.2, [[(b, {"size": 30, "bold": True, "color": GREY})], "滑动窗口（IDSIA）"], size=14, space=0)
text(s, 6.7, 1.5, 6.0, 0.4, ["细胞分割（ISBI 2015，IOU 越大越好）"], size=16, bold=True, color=GREY)
cd = CategoryChartData()
cd.categories = ["PhC-U373", "DIC-HeLa"]
cd.add_series("U-Net", (0.92, 0.78))
cd.add_series("第二名", (0.83, 0.46))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.7), Inches(2.0), Inches(6.0), Inches(4.4), cd)
gf.name = "IOU chart"
ch = gf.chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(14)
ch.legend.font.name = BODY
for ser, col in zip(ch.series, (TEAL, GRID)):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = col
plot = ch.plots[0]
plot.gap_width = 80
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format, dl.number_format_is_linked = "0.00", False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size, dl.font.bold, dl.font.name = Pt(16), True, BODY
va = ch.value_axis
va.maximum_scale, va.minimum_scale = 1.0, 0
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = GRID
va.tick_labels.font.size = Pt(12)
va.tick_labels.font.color.rgb = GREY
va.format.line.fill.background()
ca = ch.category_axis
ca.tick_labels.font.size = Pt(14)
ca.tick_labels.font.color.rgb = INK
source(s, "来源：论文表 1（ISBI 2012 排行榜，2015-03-06）、表 2（ISBI 2015 细胞追踪挑战）")
notes(s, "第 2 页的直觉“滑动窗口更精细”：在电镜任务上两项错误率都是 U-Net 更低，反而更精细，靠的是跳跃连接。"
         "U-Net 不加预处理和后处理，但测试时对 7 个旋转版本取平均。IDSIA 的分数是 Ciresan 团队自己提交的，条件不同。")

# ---------- 9 caveats ----------
s = slide_base("分数可信，但“为什么更好”没有证据")
cav = [
    ("加后处理的滑动窗口，Rand error 更好", "IDSIA-SCI 0.0189、DIVE-SCI 0.0305，U-Net 0.0382；表 1 按 warping error 排序"),
    ("没有消融实验", "分不清功劳属于结构、弹性形变还是加权损失；补边、通道数等设计也没对比"),
    ("“更快”没有同条件测速", "只有 U-Net 自己的速度：512×512 不到 1 秒，训练 10 小时（Titan 6 GB）"),
    ("数据范围窄", "只有显微镜图像，没有 CT、MRI；没有误差范围，也没有统计检验"),
]
cw2, ch2 = 5.9, 2.4
for k, (h, b) in enumerate(cav):
    x = 0.6 + (k % 2) * (cw2 + 0.3)
    y = 1.6 + (k // 2) * (ch2 + 0.3)
    box(s, x, y, cw2, ch2, CORAL_LIGHT if k < 2 else PALE)
    badge(s, x + 0.3, y + 0.3, str(k + 1), fill=CORAL if k < 2 else GREY)
    text(s, x + 1.0, y + 0.3, cw2 - 1.3, ch2 - 0.5, [[(h, {"bold": True, "size": 18})], b], size=15, space=6)
source(s, "来源：论文表 1、第 6–8 页")
notes(s, "可信的是分数本身：答案在组织方手里。准确说法：不加后处理的 U-Net 好过不加后处理的滑动窗口；"
         "加了数据集专用后处理的滑动窗口在 Rand error 上能赢它。论文也没有试过 U-Net 加同样后处理。")

# ---------- 10 takeaway ----------
s = slide_base(None, dark=True)
text(s, 0.8, 0.7, 11.7, 1.4, ["结构可以直接用，迁移到新任务要自己做实验"], size=36, bold=True, head=True,
     color=WHITE, name="Title")
box(s, 0.8, 2.3, 5.7, 4.1, RGBColor(0x2B, 0x4C, 0x63), radius=0.06)
text(s, 1.1, 2.55, 5.1, 3.7, [
    [("一句话复述", {"bold": True, "color": TEAL_LIGHT, "size": 18})],
    [("A ", {"bold": True, "color": TEAL_LIGHT}), ("U-Net 整套方法（U 形网络+弹性形变+间隙加权）", {"color": WHITE})],
    [("B ", {"bold": True, "color": GRID}), ("滑动窗口网络（Ciresan 等）", {"color": WHITE})],
    [("在 20–35 张训练图的显微镜分割上，不加后处理时 A 更好", {"color": WHITE, "bold": True})],
], size=16, space=12)
text(s, 7.0, 2.3, 5.5, 0.5, ["想讨论的问题"], size=18, bold=True, color=TEAL_LIGHT)
qs = ["迁移到我们的数据，先做哪些消融实验？", "补边还是不补边？"]
for k, q in enumerate(qs):
    y = 3.0 + k * 1.6
    badge(s, 7.0, y + 0.2, str(k + 1), fill=CORAL, d=0.6, size=18)
    text(s, 7.85, y, 4.7, 1.0, [q], size=18, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
source(s, SRC, dark=True)
notes(s, "我的判断：在小数据集的分割任务上问题解决了；分数由比赛方给出，可信；但没有消融实验，"
         "要在其他数据集上复用，网络结构和后处理方案都需要额外实验来专门适配。")

out = OUT / "unet-group-meeting-zh.pptx"
prs.save(out)
print(out)
