"""Public version of the U-Net group-meeting deck: all figures self-made (see make_figures.py).

Run: uv run --no-project --with python-pptx python -I build_en.py <out-dir> <figures-dir>
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
        text(s, 0.6, 0.4, 12.1, 0.95, [title], size=26, bold=True, head=True,
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
text(s, 0.8, 0.9, 7.0, 0.4, ["Group meeting · paper report · 2026-10-31"], size=14, color=TEAL_LIGHT)
text(s, 0.8, 1.45, 6.6, 2.6, ["A few dozen annotated images are enough to train a precise segmentation network"],
     size=34, bold=True, head=True, color=WHITE, name="Title")
text(s, 0.8, 4.15, 6.4, 1.2, [
    "U-Net: Convolutional Networks for Biomedical Image Segmentation",
    "Ronneberger, Fischer, Brox · MICCAI 2015 · arXiv:1505.04597",
], size=14, color=GRID)
box(s, 0.8, 5.45, 6.4, 1.2, RGBColor(0x2B, 0x4C, 0x63), radius=0.12)
text(s, 1.05, 5.55, 5.9, 1.0, [[("The problem: ", {"bold": True, "color": TEAL_LIGHT}),
                               ("with only 20–35 training images, how do we label every pixel correctly?", {"color": WHITE})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 7.75, 1.35, 4.95, 3.75, WHITE, radius=0.06)
picture(s, FIG / "fig1-unet.png", 7.95, 1.6, w=4.55, name="Fig1 thumbnail")
text(s, 7.75, 5.25, 4.95, 0.3, ["Schematic redrawn after paper Fig. 1"], size=10, color=GRID)
notes(s, "Core claim: a U-shaped network (shrink to see the whole, enlarge to localize, pass the details straight across), "
         "with heavy data augmentation, can be trained from very few annotated images and segments more accurately than the sliding-window method.")

# ---------- 2 sliding window ----------
s = slide_base("The sliding window decides patch by patch: slow, and “seeing wide” and “locating precisely” pull against each other")
n, cell, gx, gy = 9, 0.42, 0.9, 1.75
for i in range(n):
    for j in range(n):
        box(s, gx + j * cell, gy + i * cell, cell - 0.04, cell - 0.04, PALE, shape=MSO_SHAPE.RECTANGLE)
for (pi, pj, dash) in ((2, 1, False), (2, 2, True)):
    fr = box(s, gx + pj * cell - 0.03, gy + pi * cell - 0.03, 3 * cell + 0.02, 3 * cell + 0.02,
             WHITE, line=TEAL, shape=MSO_SHAPE.RECTANGLE)
    fr.fill.background()
    if dash:
        fr.line.dash_style = 4
    box(s, gx + (pj + 1) * cell, gy + (pi + 1) * cell, cell - 0.04, cell - 0.04,
        CORAL if not dash else CORAL_LIGHT, shape=MSO_SHAPE.RECTANGLE)
arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(gx + 1.5 * cell), Inches(gy + 1.55 * cell),
                               Inches(gx + 2.6 * cell), Inches(gy + 1.55 * cell))
arrow.line.color.rgb = CORAL
arrow.line.width = Pt(2.5)
arrow.line._get_or_add_ln().append(arrow.line._get_or_add_ln().makeelement(qn("a:tailEnd"), {"type": "triangle"}))
text(s, gx, gy + n * cell + 0.2, n * cell, 1.25, [
    [("■ ", {"color": CORAL}), ("Centre pixel: the only one the network classifies", {})],
    [("□ ", {"color": TEAL}), ("Patch: move one step, cut again, run the network again", {})],
], size=14, space=4)
cx = 5.6
box(s, cx, 1.75, 6.9, 1.9, TEAL_LIGHT)
badge(s, cx + 0.3, 1.95, "1")
text(s, cx + 1.0, 1.95, 5.6, 1.6, [[("Slow", {"bold": True, "size": 22})],
                                     "The network runs once for every pixel; neighbouring patches overlap almost completely, so most work is repeated"], size=16)
box(s, cx, 3.95, 6.9, 2.6, TEAL_LIGHT)
badge(s, cx + 0.3, 4.15, "2")
text(s, cx + 1.0, 4.15, 5.6, 2.3, [[("Trade-off", {"bold": True, "size": 22})],
                                     [("Large patch: ", {"bold": True}), ("more context, but it must be shrunk first, so localization gets coarse", {})],
                                     [("Small patch: ", {"bold": True}), ("precise localization, but very little context", {})]], size=16)
source(s, "Source: paper pp. 1–2; sliding-window method: Ciresan et al., NIPS 2012. Sketch drawn for this deck")
notes(s, "The sliding window is not another name for a CNN: the window holds a CNN that runs once per step. U-Net is a CNN too; "
         "the difference is that it takes the whole image in and gives the whole map out in one pass. Intuitively the sliding window seems finer, "
         "but a large patch has to be shrunk, which blurs the centre pixel's position. The paper sets out to overturn that intuition; slide 8 checks it.")

# ---------- 3 U-Net ----------
s = slide_base("U-Net = encoder–decoder + a skip connection at every level, whole image out at once")
picture(s, FIG / "fig1-unet.png", 0.6, 1.55, w=7.9, name="Fig1")
items = [
    (TEAL, "Left, going down (encoder)", "Shrinks step by step: 572×572 → about 30×30; sees the whole, loses position"),
    (TEAL, "Right, going up (decoder)", "Enlarges step by step and finally gives every pixel a class (output 388×388)"),
    (CORAL, "Grey arrows (skip connections)", "Copy the image from before shrinking across, recovering sharp edges and position"),
]
for k, (c, h, b) in enumerate(items):
    y = 1.6 + k * 1.75
    box(s, 8.85, y, 3.85, 1.5, TEAL_LIGHT if c == TEAL else CORAL_LIGHT)
    text(s, 9.1, y + 0.12, 3.4, 1.3, [[(h, {"bold": True, "color": c, "size": 16})], b], size=14, space=3)
source(s, "Schematic redrawn from the layer sizes in paper Fig. 1; original: " + SRC)
notes(s, "A plain encoder–decoder only gets the compressed bottom information, so edges blur; U-Net joins the uncompressed image of the same level at every step up. "
         "Left and right are only roughly symmetric: 64×2 = 128 channels where they join, back to 64 after two convolutions; the left 568 is cropped to 392 "
         "(unpadded convolutions lose a border each time). The 388×388 output is exactly the centre of the 572×572 input; large images use overlapping tiles, mirrored at the border. "
         "Why not pad so input and output match? Possible, and most later implementations do; the authors' reason is not to invent border pixels and to tile seamlessly, but the paper has no comparison. "
         "Doubling channels at each step was common practice (e.g. VGG); the paper neither explains it nor compares other numbers.")

# ---------- 4 augmentation ----------
s = slide_base("Elastic deformation turns existing images into new ones, without new annotation")
imgs = ["cells-original.png", "cells-elastic-1.png", "cells-elastic-2.png", "cells-elastic-3.png"]
caps = ["Original", "Elastic deformation 1", "Elastic deformation 2", "Elastic deformation 3"]
iw, gap, x0 = 2.75, 0.35, 0.6
for k, (f, c) in enumerate(zip(imgs, caps)):
    x = x0 + k * (iw + gap)
    picture(s, FIG / f, x, 1.6, w=iw, name=c)
    text(s, x, 1.6 + iw * 238 / 232 + 0.1, iw, 0.35, [c], size=14, bold=(k == 0),
         color=INK if k == 0 else TEAL, align=PP_ALIGN.CENTER)
box(s, 0.6, 5.25, 5.85, 1.45, PALE)
text(s, 0.85, 5.35, 5.4, 1.25, [[("Problem: ", {"bold": True, "color": CORAL}),
                                 ("only 20–35 training images; the network learns them by heart and fails on a new image", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.85, 5.25, 5.85, 1.45, TEAL_LIGHT)
text(s, 7.1, 5.35, 5.4, 1.25, [[("Method: ", {"bold": True, "color": TEAL}),
                                ("shift, rotation, grey values, plus random elastic deformation; tissue is soft, so real sections deform like this", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Synthetic cell image; deformations generated as the paper describes (random shifts on a coarse 3×3 grid, bicubic interpolation); real example: paper Fig. 3a")
notes(s, "U-Net takes whole images, so it cannot multiply samples by cutting patches like the sliding window; it makes new versions of the images instead, "
         "with the ground truth transformed alongside. The authors say elastic deformations 'seem to be the key concept' — their judgement only; "
         "the paper has no experiment that removes them and compares.")

# ---------- 5 weighted loss ----------
s = slide_base("Weight the narrow gaps between cells so the network learns to separate them")
picture(s, FIG / "fig3-weights.png", 0.6, 1.5, w=12.1, name="Fig3")
fig3_h = 12.1 * 279 / 1209
cy = 1.5 + fig3_h + 0.45
cards = [
    (CORAL_LIGHT, CORAL, "Problem", "The network outputs only “cell” or “background”. Touching cells have no background pixel between them, so they come out as one blob"),
    (PALE, INK, "Method", "Draw a background gap between cells in the ground truth (Fig. c); gap pixels cost more when wrong (Fig. d, red/yellow = high weight)"),
    (TEAL_LIGHT, TEAL, "Why weight it", "The gap is only a few pixels wide; unweighted, a mistake there costs almost nothing and the network “gets lazy”"),
]
cw = (12.1 - 2 * 0.35) / 3
for k, (fill, col, h, b) in enumerate(cards):
    x = 0.6 + k * (cw + 0.35)
    box(s, x, cy, cw, 6.75 - cy, fill)
    text(s, x + 0.25, cy + 0.18, cw - 0.5, 6.75 - cy - 0.3, [[(h, {"bold": True, "color": col, "size": 17})], b],
         size=14, space=4)
source(s, "Synthetic example (a image, b instances, c labels with gaps, d weight map by the paper's Eq. 2); original: paper Fig. 3; w0 = 10, σ ≈ 5 pixels")
notes(s, "The cell labels come from the challenge organizers (manual annotation); the gaps are computed by the authors from those labels with morphological operations, "
         "and the weights by a formula from the distances to the nearest and second-nearest cell. The same weight map also balances the class frequencies.")

# ---------- 6 mapping ----------
s = slide_base("Each part answers one of the original problems")
rows = [
    ("U-shaped network + skip connections", "Wide context vs precise location; patch-by-patch is slow", "Whole image in one pass; skip connections bring the detail back"),
    ("Elastic-deformation augmentation", "Only 20–35 training images; easy to learn by heart", "Sees more realistic variations, without new annotation"),
    ("Weighted loss on cell gaps", "Touching cells merge into one blob", "Forces the network to learn the narrow gaps"),
]
text(s, 1.4, 1.55, 3.6, 0.4, ["Part of the method"], size=14, bold=True, color=GREY)
text(s, 5.3, 1.55, 3.6, 0.4, ["Original problem it answers"], size=14, bold=True, color=GREY)
text(s, 9.2, 1.55, 3.5, 0.4, ["How it works"], size=14, bold=True, color=GREY)
for k, (a, b, c) in enumerate(rows):
    y = 2.05 + k * 1.55
    badge(s, 0.6, y + 0.35, str(k + 1), d=0.6, size=18)
    box(s, 1.4, y, 3.6, 1.3, TEAL_LIGHT)
    text(s, 1.6, y, 3.2, 1.3, [a], size=16, bold=True, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 5.3, y, 3.6, 1.3, CORAL_LIGHT)
    text(s, 5.5, y, 3.2, 1.3, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 9.2, y, 3.5, 1.3, PALE)
    text(s, 9.4, y, 3.1, 1.3, [c], size=14, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Source: paper pp. 1–6")
notes(s, "This is 'why it works': the three parts answer slide 2's trade-off and slowness, the small data, and merged cells. It is a design mapping only; "
         "how much each part contributes, the paper does not test (see slide 9).")

# ---------- 7 evaluation ----------
s = slide_base("Three public challenges, the answers held by the organizers")
data = [("Task", "Images", "Training", "Metric"),
        ("Neuronal structures\nISBI 2012", "Electron microscopy\nDrosophila larva nerve cord", "30 images\nfully annotated", "Warping / Rand / pixel error\nlower is better"),
        ("Cells PhC-U373\nISBI 2015", "Phase contrast\nglioblastoma cells", "35 images\npartially annotated", "IOU\nhigher is better"),
        ("Cells DIC-HeLa\nISBI 2015", "DIC microscopy\nHeLa cells", "20 images\npartially annotated", "IOU\nhigher is better")]
tbl = s.shapes.add_table(4, 4, Inches(0.6), Inches(1.6), Inches(8.0), Inches(4.6)).table
for j, wdt in enumerate((2.0, 2.4, 1.5, 2.1)):
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
    [("Test answers are secret", {"bold": True, "size": 18})],
    "Authors only submit predictions; the organizers score and rank every entry",
    "→ no peeking at answers to tune",
    "→ everyone takes the same exam",
], size=15, space=8)
source(s, "Source: paper pp. 6–7; IOU = overlap ÷ union of predicted and true area, 1 = perfect match")
notes(s, "Metrics in one sentence each: pixel error = share of wrong pixels, lower is better; Rand error = share of pixel pairs put in the wrong "
         "'same / different cell' group, lower is better, punishes merged or split cells; warping error = only mistakes that change the cell layout "
         "(merges, splits, holes), lower is better; IOU = overlap ÷ union, higher is better, 1 is perfect. "
         "The competitors include the sliding-window method (Ciresan et al., listed as IDSIA). The scores are credible; question marks: the EM challenge accepts "
         "repeated submissions (one team submitted 78 times), U-Net's count is not given; whole pipelines are compared; microscopy only.")

# ---------- 8 results ----------
s = slide_base("Without post-processing, U-Net already beats the sliding window")
text(s, 0.6, 1.5, 5.6, 0.4, ["EM task (ISBI 2012) · lower is better"], size=16, bold=True, color=GREY)
pairs = [("Warping error", "0.000353", "0.000420", "U-Net ranks 1st"), ("Rand error", "0.0382", "0.0504", "")]
for k, (m, u, b, note) in enumerate(pairs):
    y = 2.05 + k * 2.2
    box(s, 0.6, y, 5.6, 1.95, PALE)
    text(s, 0.85, y + 0.15, 5.1, 0.4, [m + ("  ·  " + note if note else "")], size=15, bold=True)
    text(s, 0.85, y + 0.6, 2.6, 1.2, [[(u, {"size": 30, "bold": True, "color": TEAL})], "U-Net"], size=14, space=0)
    text(s, 3.45, y + 0.6, 2.6, 1.2, [[(b, {"size": 30, "bold": True, "color": GREY})], "Sliding window (IDSIA)"], size=14, space=0)
text(s, 6.7, 1.5, 6.0, 0.4, ["Cell tasks (ISBI 2015) · IOU, higher is better"], size=16, bold=True, color=GREY)
cd = CategoryChartData()
cd.categories = ["PhC-U373", "DIC-HeLa"]
cd.add_series("U-Net", (0.92, 0.78))
cd.add_series("Second best", (0.83, 0.46))
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
source(s, "Source: paper Table 1 (ISBI 2012 leaderboard, 2015-03-06), Table 2 (ISBI 2015 cell tracking challenge)")
notes(s, "Reading the metrics: warping and Rand error count mistakes, so lower is better; IOU measures overlap, so higher is better. "
         "Slide 2's intuition 'the sliding window is finer': on the EM task both error rates are lower for U-Net, so it is in fact finer, thanks to the skip connections. "
         "U-Net uses no pre- or post-processing, but averages 7 rotated versions at test time. IDSIA's score was submitted by Ciresan's team, under different conditions.")

# ---------- 9 caveats ----------
s = slide_base("The scores are credible, but there is no evidence for why it is better")
cav = [
    ("Sliding window + post-processing has better Rand error", "IDSIA-SCI 0.0189, DIVE-SCI 0.0305 vs U-Net 0.0382; Table 1 is sorted by warping error"),
    ("No ablation experiment", "Credit cannot be split between architecture, elastic deformation and weighted loss; padding and channel counts not compared either"),
    ("“Faster” not measured under equal conditions", "Only U-Net's own speed: 512×512 in under 1 s, 10 h training (Titan, 6 GB)"),
    ("Narrow data", "Microscopy only, no CT or MRI; no error bars and no statistical test"),
]
cw2, ch2 = 5.9, 2.4
for k, (h, b) in enumerate(cav):
    x = 0.6 + (k % 2) * (cw2 + 0.3)
    y = 1.6 + (k // 2) * (ch2 + 0.3)
    box(s, x, y, cw2, ch2, CORAL_LIGHT if k < 2 else PALE)
    badge(s, x + 0.3, y + 0.3, str(k + 1), fill=CORAL if k < 2 else GREY)
    text(s, x + 1.0, y + 0.3, cw2 - 1.3, ch2 - 0.5, [[(h, {"bold": True, "size": 17})], b], size=15, space=6)
source(s, "Source: paper Table 1, pp. 6–8")
notes(s, "What is credible is the scores themselves: the organizers hold the answers. Precisely: U-Net without post-processing beats the sliding window without post-processing; "
         "the sliding window with dataset-specific post-processing beats it on Rand error. The paper never tries U-Net with the same post-processing.")

# ---------- 10 takeaway ----------
s = slide_base(None, dark=True)
text(s, 0.8, 0.6, 11.7, 1.5, ["The architecture can be used directly; a new task needs its own experiments"], size=32, bold=True, head=True,
     color=WHITE, name="Title")
box(s, 0.8, 2.3, 5.7, 4.1, RGBColor(0x2B, 0x4C, 0x63), radius=0.06)
text(s, 1.1, 2.55, 5.1, 3.7, [
    [("In one sentence", {"bold": True, "color": TEAL_LIGHT, "size": 18})],
    [("A ", {"bold": True, "color": TEAL_LIGHT}), ("the whole U-Net method (U shape + elastic deformation + gap weighting)", {"color": WHITE})],
    [("B ", {"bold": True, "color": GRID}), ("the sliding-window network (Ciresan et al.)", {"color": WHITE})],
    [("On microscopy segmentation with 20–35 training images, A is better without post-processing", {"color": WHITE, "bold": True})],
], size=16, space=12)
text(s, 7.0, 2.3, 5.5, 0.5, ["Questions for discussion"], size=18, bold=True, color=TEAL_LIGHT)
qs = ["Which ablations should we run first on our data?", "Padding or no padding?"]
for k, q in enumerate(qs):
    y = 3.0 + k * 1.6
    badge(s, 7.0, y + 0.2, str(k + 1), fill=CORAL, d=0.6, size=18)
    text(s, 7.85, y, 4.7, 1.0, [q], size=18, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
source(s, SRC, dark=True)
notes(s, "My judgement: for segmentation with small datasets the problem is solved; the scores come from the organizers and are credible; "
         "but without ablations, reusing the method on other datasets needs extra experiments to adapt the architecture and post-processing.")

out = OUT / "unet-group-meeting-en.pptx"
prs.save(out)
print(out)
