"""Public version of the U-Net group-meeting deck: all figures self-made (see make_figures.py).

Run: uv run --no-project --with python-pptx python -I build_de.py <out-dir> <figures-dir>
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
text(s, 0.8, 0.9, 7.0, 0.4, ["Gruppenmeeting · Paper-Vorstellung · 2026-10-31"], size=14, color=TEAL_LIGHT)
text(s, 0.8, 1.45, 6.6, 2.6, ["Ein paar Dutzend annotierte Bilder reichen für ein präzises Segmentierungsnetz"],
     size=34, bold=True, head=True, color=WHITE, name="Title")
text(s, 0.8, 4.15, 6.4, 1.2, [
    "U-Net: Convolutional Networks for Biomedical Image Segmentation",
    "Ronneberger, Fischer, Brox · MICCAI 2015 · arXiv:1505.04597",
], size=14, color=GRID)
box(s, 0.8, 5.45, 6.4, 1.2, RGBColor(0x2B, 0x4C, 0x63), radius=0.12)
text(s, 1.05, 5.55, 5.9, 1.0, [[("Das Problem: ", {"bold": True, "color": TEAL_LIGHT}),
                               ("Wie bekommt jedes Pixel das richtige Label, wenn es nur 20–35 Trainingsbilder gibt?", {"color": WHITE})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, 7.75, 1.35, 4.95, 3.75, WHITE, radius=0.06)
picture(s, FIG / "fig1-unet.png", 7.95, 1.6, w=4.55, name="Fig1 thumbnail")
text(s, 7.75, 5.25, 4.95, 0.3, ["Schema nach Paper Abb. 1 neu gezeichnet"], size=10, color=GRID)
notes(s, "Kernaussage: Ein U-förmiges Netz (verkleinern, um das Ganze zu sehen, vergrößern, um zu lokalisieren, Details direkt hinüberreichen) "
         "lässt sich mit starker Datenaugmentierung aus sehr wenigen annotierten Bildern trainieren und segmentiert genauer als die Sliding-Window-Methode.")

# ---------- 2 sliding window ----------
s = slide_base("Sliding Window: langsam, und „weit sehen“ und „genau lokalisieren“ ziehen gegeneinander")
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
text(s, gx, gy + n * cell + 0.2, n * cell, 1.45, [
    [("■ ", {"color": CORAL}), ("Mittelpixel: das einzige, das das Netz klassifiziert", {})],
    [("□ ", {"color": TEAL}), ("Ausschnitt: einen Schritt weiter, neu schneiden, Netz neu laufen lassen", {})],
], size=14, space=4)
cx = 5.6
box(s, cx, 1.75, 6.9, 1.9, TEAL_LIGHT)
badge(s, cx + 0.3, 1.95, "1")
text(s, cx + 1.0, 1.95, 5.6, 1.6, [[("Langsam", {"bold": True, "size": 22})],
                                     "Das Netz läuft für jedes Pixel einmal; benachbarte Ausschnitte überlappen fast völlig, also wird die meiste Arbeit wiederholt"], size=16)
box(s, cx, 3.95, 6.9, 2.6, TEAL_LIGHT)
badge(s, cx + 0.3, 4.15, "2")
text(s, cx + 1.0, 4.15, 5.6, 2.3, [[("Zielkonflikt", {"bold": True, "size": 22})],
                                     [("Großer Ausschnitt: ", {"bold": True}), ("mehr Kontext, muss aber erst verkleinert werden, daher grobe Lokalisierung", {})],
                                     [("Kleiner Ausschnitt: ", {"bold": True}), ("genaue Lokalisierung, aber sehr wenig Kontext", {})]], size=16)
source(s, "Quelle: Paper S. 1–2; Sliding-Window-Methode: Ciresan et al., NIPS 2012. Skizze für diesen Foliensatz gezeichnet")
notes(s, "Das Sliding Window ist kein anderer Name für ein CNN: Im Fenster steckt ein CNN, das pro Schritt einmal läuft. U-Net ist auch ein CNN; "
         "der Unterschied: Es nimmt das ganze Bild und gibt die ganze Karte in einem Durchgang aus. Intuitiv wirkt das Sliding Window feiner, "
         "aber ein großer Ausschnitt muss verkleinert werden, was die Position des Mittelpixels verwischt. Das Paper will diese Intuition widerlegen; Folie 8 prüft es.")

# ---------- 3 U-Net ----------
s = slide_base("U-Net = Encoder–Decoder + eine Skip-Verbindung auf jeder Ebene, das ganze Bild in einem Durchgang")
picture(s, FIG / "fig1-unet.png", 0.6, 1.55, w=7.9, name="Fig1")
items = [
    (TEAL, "Links abwärts (Encoder)", "Verkleinert Schritt für Schritt: 572×572 → etwa 30×30; sieht das Ganze, verliert die Position"),
    (TEAL, "Rechts aufwärts (Decoder)", "Vergrößert Schritt für Schritt und gibt jedem Pixel eine Klasse (Ausgabe 388×388)"),
    (CORAL, "Graue Pfeile (Skip-Verbindungen)", "Kopieren das Bild vor dem Verkleinern hinüber; holen Kanten und Position zurück"),
]
for k, (c, h, b) in enumerate(items):
    y = 1.6 + k * 1.75
    box(s, 8.85, y, 3.85, 1.5, TEAL_LIGHT if c == TEAL else CORAL_LIGHT)
    text(s, 9.1, y + 0.12, 3.4, 1.3, [[(h, {"bold": True, "color": c, "size": 16})], b], size=14, space=3)
source(s, "Schema nach den Ebenengrößen in Paper Abb. 1 neu gezeichnet; Original: " + SRC)
notes(s, "Ein einfacher Encoder–Decoder bekommt nur die komprimierte unterste Information, die Kanten verschwimmen; U-Net fügt bei jedem Schritt aufwärts das unkomprimierte Bild derselben Ebene an. "
         "Links und rechts sind nur ungefähr symmetrisch: 64×2 = 128 Kanäle an der Verbindung, nach zwei Faltungen wieder 64; links 568 wird auf 392 zugeschnitten "
         "(Faltungen ohne Padding verlieren jedes Mal einen Rand). Die 388×388-Ausgabe ist genau die Mitte der 572×572-Eingabe; große Bilder nutzen überlappende Kacheln, am Rand gespiegelt. "
         "Warum nicht Padding, damit Ein- und Ausgabe gleich sind? Möglich, die meisten späteren Implementierungen tun es; die Autoren wollen keine Randpixel erfinden und nahtlos kacheln, aber das Paper vergleicht es nicht. "
         "Kanäle pro Schritt zu verdoppeln war gängige Praxis (z. B. VGG); das Paper erklärt es nicht und vergleicht keine anderen Zahlen.")

# ---------- 4 augmentation ----------
s = slide_base("Elastische Verformung macht aus vorhandenen Bildern neue, ohne neue Annotation")
imgs = ["cells-original.png", "cells-elastic-1.png", "cells-elastic-2.png", "cells-elastic-3.png"]
caps = ["Original", "Elastische Verformung 1", "Elastische Verformung 2", "Elastische Verformung 3"]
iw, gap, x0 = 2.75, 0.35, 0.6
for k, (f, c) in enumerate(zip(imgs, caps)):
    x = x0 + k * (iw + gap)
    picture(s, FIG / f, x, 1.6, w=iw, name=c)
    text(s, x, 1.6 + iw * 238 / 232 + 0.1, iw, 0.35, [c], size=14, bold=(k == 0),
         color=INK if k == 0 else TEAL, align=PP_ALIGN.CENTER)
box(s, 0.6, 5.25, 5.85, 1.45, PALE)
text(s, 0.85, 5.35, 5.4, 1.25, [[("Problem: ", {"bold": True, "color": CORAL}),
                                 ("nur 20–35 Trainingsbilder; das Netz lernt sie auswendig und scheitert an einem neuen Bild", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.85, 5.25, 5.85, 1.45, TEAL_LIGHT)
text(s, 7.1, 5.35, 5.4, 1.25, [[("Methode: ", {"bold": True, "color": TEAL}),
                                ("Verschiebung, Drehung, Grauwerte, dazu zufällige elastische Verformung; Gewebe ist weich, echte Schnitte verformen sich so", {})]],
     size=15, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Synthetisches Zellbild; Verformungen wie im Paper beschrieben (grobes 3×3-Gitter, bikubisch); echtes Beispiel: Paper Abb. 3a")
notes(s, "U-Net nimmt ganze Bilder und kann Beispiele nicht wie das Sliding Window durch Ausschnitte vermehren; stattdessen erzeugt es neue Versionen der Bilder, "
         "die Referenz wird mitverändert. Die Autoren sagen, elastische Verformungen 'seem to be the key concept' — nur ihr Urteil; "
         "das Paper hat kein Experiment, das sie weglässt und vergleicht.")

# ---------- 5 weighted loss ----------
s = slide_base("Die schmalen Lücken zwischen Zellen gewichten, damit das Netz sie trennen lernt")
picture(s, FIG / "fig3-weights.png", 0.6, 1.5, w=12.1, name="Fig3")
fig3_h = 12.1 * 279 / 1209
cy = 1.5 + fig3_h + 0.45
cards = [
    (CORAL_LIGHT, CORAL, "Problem", "Das Netz gibt nur „Zelle“ oder „Hintergrund“ aus. Zwischen sich berührenden Zellen liegt kein Hintergrundpixel, sie erscheinen als ein Klumpen"),
    (PALE, INK, "Methode", "In der Referenz eine Lücke zwischen Zellen zeichnen (Abb. c); Fehler dort kosten mehr (Abb. d, rot/gelb = hohes Gewicht)"),
    (TEAL_LIGHT, TEAL, "Warum gewichten", "Die Lücke ist nur wenige Pixel breit; ungewichtet kostet ein Fehler dort fast nichts, und das Netz „wird faul“"),
]
cw = (12.1 - 2 * 0.35) / 3
for k, (fill, col, h, b) in enumerate(cards):
    x = 0.6 + k * (cw + 0.35)
    box(s, x, cy, cw, 6.75 - cy, fill)
    text(s, x + 0.25, cy + 0.18, cw - 0.5, 6.75 - cy - 0.3, [[(h, {"bold": True, "color": col, "size": 17})], b],
         size=14, space=4)
source(s, "Synthetisches Beispiel (a Bild, b Instanzen, c Labels mit Lücken, d Gewichtskarte nach Gl. 2 des Papers); Original: Paper Abb. 3; w0 = 10, σ ≈ 5 Pixel")
notes(s, "Die Zelllabels stammen von den Veranstaltern der Challenge (manuelle Annotation); die Lücken berechnen die Autoren daraus mit morphologischen Operationen, "
         "die Gewichte mit einer Formel aus den Abständen zur nächsten und zweitnächsten Zelle. Dieselbe Gewichtskarte gleicht auch die Klassenhäufigkeiten aus.")

# ---------- 6 mapping ----------
s = slide_base("Jeder Teil beantwortet eines der ursprünglichen Probleme")
rows = [
    ("U-förmiges Netz + Skip-Verbindungen", "Weiter Kontext gegen genaue Position; Ausschnitt für Ausschnitt ist langsam", "Ganzes Bild in einem Durchgang; Skip-Verbindungen holen die Details zurück"),
    ("Augmentierung durch elastische Verformung", "Nur 20–35 Trainingsbilder; leicht auswendig zu lernen", "Sieht mehr realistische Varianten, ohne neue Annotation"),
    ("Gewichteter Verlust auf Zelllücken", "Sich berührende Zellen verschmelzen zu einem Klumpen", "Zwingt das Netz, die schmalen Lücken zu lernen"),
]
text(s, 1.4, 1.55, 3.6, 0.4, ["Teil der Methode"], size=14, bold=True, color=GREY)
text(s, 5.3, 1.55, 3.6, 0.4, ["Ursprüngliches Problem"], size=14, bold=True, color=GREY)
text(s, 9.2, 1.55, 3.5, 0.4, ["Wie es wirkt"], size=14, bold=True, color=GREY)
for k, (a, b, c) in enumerate(rows):
    y = 2.05 + k * 1.55
    badge(s, 0.6, y + 0.35, str(k + 1), d=0.6, size=18)
    box(s, 1.4, y, 3.6, 1.3, TEAL_LIGHT)
    text(s, 1.6, y, 3.2, 1.3, [a], size=16, bold=True, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 5.3, y, 3.6, 1.3, CORAL_LIGHT)
    text(s, 5.5, y, 3.2, 1.3, [b], size=14, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 9.2, y, 3.5, 1.3, PALE)
    text(s, 9.4, y, 3.1, 1.3, [c], size=14, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Quelle: Paper S. 1–6")
notes(s, "Das ist 'warum es wirkt': Die drei Teile beantworten Zielkonflikt und Langsamkeit von Folie 2, die wenigen Daten und verschmolzene Zellen. Es ist nur eine Zuordnung im Design; "
         "wie viel jeder Teil beiträgt, testet das Paper nicht (siehe Folie 9).")

# ---------- 7 evaluation ----------
s = slide_base("Drei öffentliche Challenges, die Lösungen liegen bei den Veranstaltern")
data = [("Aufgabe", "Bilder", "Training", "Metrik"),
        ("Neuronale Strukturen\nISBI 2012", "Elektronenmikroskopie\nNervenstrang der Drosophila-Larve", "30 Bilder\nvollständig annotiert", "Warping / Rand / Pixel Error\nkleiner ist besser"),
        ("Zellen PhC-U373\nISBI 2015", "Phasenkontrast\nGlioblastomzellen", "35 Bilder\nteilweise annotiert", "IOU\ngrößer ist besser"),
        ("Zellen DIC-HeLa\nISBI 2015", "DIC-Mikroskopie\nHeLa-Zellen", "20 Bilder\nteilweise annotiert", "IOU\ngrößer ist besser")]
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
    [("Testlösungen sind geheim", {"bold": True, "size": 18})],
    "Autoren reichen nur Vorhersagen ein; die Veranstalter bewerten und ranken jede Einreichung",
    "→ kein Blick in die Lösungen zum Abstimmen",
    "→ alle schreiben dieselbe Prüfung",
], size=15, space=8)
source(s, "Quelle: Paper S. 6–7; IOU = Überlappung ÷ Vereinigung von vorhergesagter und wahrer Fläche, 1 = perfekt")
notes(s, "Metriken in je einem Satz: Pixel Error = Anteil falscher Pixel, kleiner ist besser; Rand Error = Anteil der Pixelpaare in der falschen Gruppe "
         "'gleiche / verschiedene Zelle', kleiner ist besser, bestraft verschmolzene oder aufgespaltene Zellen; Warping Error = nur Fehler, die die Zellanordnung ändern "
         "(Verschmelzungen, Aufspaltungen, Löcher), kleiner ist besser; IOU = Überlappung ÷ Vereinigung, größer ist besser, 1 ist perfekt. "
         "Zu den Konkurrenten gehört die Sliding-Window-Methode (Ciresan et al., als IDSIA gelistet). Die Punktzahlen sind glaubwürdig; Fragezeichen: Die EM-Challenge erlaubt "
         "wiederholte Einreichungen (ein Team reichte 78-mal ein), die Zahl für U-Net fehlt; ganze Pipelines werden verglichen; nur Mikroskopie.")

# ---------- 8 results ----------
s = slide_base("Ohne Nachbearbeitung schlägt U-Net das Sliding Window bereits")
text(s, 0.6, 1.5, 5.6, 0.4, ["EM-Aufgabe (ISBI 2012) · kleiner ist besser"], size=16, bold=True, color=GREY)
pairs = [("Warping Error", "0,000353", "0,000420", "U-Net auf Platz 1"), ("Rand Error", "0,0382", "0,0504", "")]
for k, (m, u, b, note) in enumerate(pairs):
    y = 2.05 + k * 2.2
    box(s, 0.6, y, 5.6, 1.95, PALE)
    text(s, 0.85, y + 0.15, 5.1, 0.4, [m + ("  ·  " + note if note else "")], size=15, bold=True)
    text(s, 0.85, y + 0.6, 2.6, 1.2, [[(u, {"size": 30, "bold": True, "color": TEAL})], "U-Net"], size=14, space=0)
    text(s, 3.45, y + 0.6, 2.6, 1.2, [[(b, {"size": 30, "bold": True, "color": GREY})], "Sliding Window (IDSIA)"], size=14, space=0)
text(s, 6.7, 1.5, 6.0, 0.4, ["Zellaufgaben (ISBI 2015) · IOU, größer ist besser"], size=16, bold=True, color=GREY)
cd = CategoryChartData()
cd.categories = ["PhC-U373", "DIC-HeLa"]
cd.add_series("U-Net", (0.92, 0.78))
cd.add_series("Zweitbester", (0.83, 0.46))
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
source(s, "Quelle: Paper Tabelle 1 (Rangliste ISBI 2012, 2015-03-06), Tabelle 2 (ISBI 2015 Cell Tracking Challenge)")
notes(s, "Metriken lesen: Warping und Rand Error zählen Fehler, also ist kleiner besser; IOU misst Überlappung, also ist größer besser. "
         "Die Intuition von Folie 2 'das Sliding Window ist feiner': Auf der EM-Aufgabe sind beide Fehlerraten bei U-Net niedriger, es ist also tatsächlich feiner, dank der Skip-Verbindungen. "
         "U-Net nutzt keine Vor- oder Nachbearbeitung, mittelt aber zur Testzeit über 7 gedrehte Versionen. Die Punktzahl von IDSIA reichte das Team von Ciresan unter anderen Bedingungen ein.")

# ---------- 9 caveats ----------
s = slide_base("Die Punktzahlen sind glaubwürdig, aber es fehlt die Evidenz dafür, warum es besser ist")
cav = [
    ("Sliding Window + Nachbearbeitung hat besseren Rand Error", "IDSIA-SCI 0,0189, DIVE-SCI 0,0305 gegen U-Net 0,0382; Tabelle 1 ist nach Warping Error sortiert"),
    ("Kein Ablationsexperiment", "Der Verdienst lässt sich nicht zwischen Architektur, elastischer Verformung und gewichtetem Verlust aufteilen; Padding und Kanalzahlen auch nicht verglichen"),
    ("„Schneller“ nicht unter gleichen Bedingungen gemessen", "Nur die eigene Geschwindigkeit von U-Net: 512×512 in unter 1 s, 10 h Training (Titan, 6 GB)"),
    ("Schmale Datenbasis", "Nur Mikroskopie, kein CT oder MRT; keine Fehlerbalken und kein statistischer Test"),
]
cw2, ch2 = 5.9, 2.4
for k, (h, b) in enumerate(cav):
    x = 0.6 + (k % 2) * (cw2 + 0.3)
    y = 1.6 + (k // 2) * (ch2 + 0.3)
    box(s, x, y, cw2, ch2, CORAL_LIGHT if k < 2 else PALE)
    badge(s, x + 0.3, y + 0.3, str(k + 1), fill=CORAL if k < 2 else GREY)
    text(s, x + 1.0, y + 0.3, cw2 - 1.3, ch2 - 0.5, [[(h, {"bold": True, "size": 17})], b], size=15, space=6)
source(s, "Quelle: Paper Tabelle 1, S. 6–8")
notes(s, "Glaubwürdig sind die Punktzahlen selbst: Die Veranstalter halten die Lösungen. Genau: U-Net ohne Nachbearbeitung schlägt das Sliding Window ohne Nachbearbeitung; "
         "das Sliding Window mit datensatzspezifischer Nachbearbeitung schlägt es beim Rand Error. Das Paper probiert U-Net nie mit derselben Nachbearbeitung aus.")

# ---------- 10 takeaway ----------
s = slide_base(None, dark=True)
text(s, 0.8, 0.6, 11.7, 1.5, ["Die Architektur ist direkt nutzbar; eine neue Aufgabe braucht eigene Experimente"], size=32, bold=True, head=True,
     color=WHITE, name="Title")
box(s, 0.8, 2.3, 5.7, 4.1, RGBColor(0x2B, 0x4C, 0x63), radius=0.06)
text(s, 1.1, 2.55, 5.1, 3.7, [
    [("In einem Satz", {"bold": True, "color": TEAL_LIGHT, "size": 18})],
    [("A ", {"bold": True, "color": TEAL_LIGHT}), ("die ganze U-Net-Methode (U-Form + elastische Verformung + Lückengewichtung)", {"color": WHITE})],
    [("B ", {"bold": True, "color": GRID}), ("das Sliding-Window-Netz (Ciresan et al.)", {"color": WHITE})],
    [("Bei Mikroskopie-Segmentierung mit 20–35 Trainingsbildern ist A ohne Nachbearbeitung besser", {"color": WHITE, "bold": True})],
], size=16, space=12)
text(s, 7.0, 2.3, 5.5, 0.5, ["Fragen zur Diskussion"], size=18, bold=True, color=TEAL_LIGHT)
qs = ["Welche Ablationen zuerst auf unseren Daten?", "Padding oder kein Padding?"]
for k, q in enumerate(qs):
    y = 3.0 + k * 1.6
    badge(s, 7.0, y + 0.2, str(k + 1), fill=CORAL, d=0.6, size=18)
    text(s, 7.85, y, 4.7, 1.0, [q], size=18, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
source(s, SRC, dark=True)
notes(s, "Mein Urteil: Für Segmentierung mit kleinen Datensätzen ist das Problem gelöst; die Punktzahlen stammen von den Veranstaltern und sind glaubwürdig; "
         "aber ohne Ablationen braucht die Übertragung auf andere Datensätze zusätzliche Experimente zur Anpassung von Architektur und Nachbearbeitung.")

out = OUT / "unet-group-meeting-de.pptx"
prs.save(out)
print(out)
