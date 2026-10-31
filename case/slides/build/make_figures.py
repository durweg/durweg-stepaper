"""Self-made figures for the public decks: no pixel comes from the U-Net paper.

  uv run --no-project --with matplotlib --with numpy --with scipy --with pillow python -I make_figures.py <out-dir>

fig1-unet.png      U-Net schematic, redrawn from the layer sizes the paper gives (Fig. 1)
fig3-weights.png   synthetic touching cells: (a) image, (b) instances, (c) labels with gaps, (d) weight map by Eq. 2
cells-*.png        the synthetic image of (a) and three elastic deformations as Section 3.1 describes
Same aspect ratios as the crops used in the internal decks, so the slide scripts place them unchanged.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy import ndimage as ndi
from PIL import Image

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
BLUE, GREY, DARK = "#6f9fd8", "#9aa4ad", "#1f2d3a"

# ---------- U-Net schematic (aspect 1.5) ----------
fig = plt.figure(figsize=(15.6, 10.4), dpi=150); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 15.6); ax.set_ylim(0, 10.4); ax.axis("off")
levels = [(64, "568²"), (128, "280²"), (256, "136²"), (512, "64²")]
ys = [8.4, 6.6, 4.8, 3.0]
def block(x, y, ch, size, w=0.35, h=1.1, col=BLUE, label=True):
    ax.add_patch(Rectangle((x, y), w, h, color=col, ec="none"))
    if label:
        ax.text(x + w / 2, y + h + 0.08, str(ch), ha="center", va="bottom", fontsize=12, color=DARK)
        ax.text(x - 0.06, y, size, ha="right", va="bottom", fontsize=10, color="#57606a", rotation=90)
def arrow(x0, y0, x1, y1, col, lw=2.5, ms=14):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw))
lx = [0.9, 2.0, 3.1, 4.2]; rx = [12.6, 11.5, 10.4, 9.3]
for i, ((ch, size), y) in enumerate(zip(levels, ys)):
    x = lx[i]
    block(x, y, ch, size); block(x + 0.6, y, ch, "", label=False)
    arrow(x + 0.38, y + 0.55, x + 0.58, y + 0.55, "#1b3a8c")
    arrow(x + 1.0, y + 0.55, rx[i] - 0.65, y + 0.55, GREY, lw=4, ms=18)
    block(rx[i] - 0.6, y, ch, "", col="#dbe6f4", label=False); block(rx[i] - 0.25, y, ch, "", label=False)
    ax.text(rx[i] - 0.25 + 0.175, y + 1.18, f"{ch}", ha="center", fontsize=12, color=DARK)
    arrow(rx[i] + 0.12, y + 0.55, rx[i] + 0.4, y + 0.55, "#1b3a8c")
    block(rx[i] + 0.42, y, ch, "", label=False)
    if i < 3:
        arrow(x + 0.78, y - 0.02, lx[i + 1] - 0.08, ys[i + 1] + 0.75, "#8b1a1a")
        arrow(rx[i + 1] + 0.6, ys[i + 1] + 1.12, rx[i] + 0.0, y - 0.02, "#2e8b2e")
by = 1.2
block(5.6, by, 1024, "28²", w=0.35); block(6.3, by, 1024, "", label=False); block(7.0, by, 1024, "", label=False)
arrow(lx[3] + 0.78, ys[3] - 0.02, 5.52, by + 0.75, "#8b1a1a"); arrow(7.2, by + 1.12, rx[3] - 0.3, ys[3] - 0.02, "#2e8b2e")
arrow(5.97, by + 0.55, 6.28, by + 0.55, "#1b3a8c"); arrow(6.67, by + 0.55, 6.98, by + 0.55, "#1b3a8c")
ax.text(0.5, 10.05, "input 572×572", fontsize=14, color=DARK, ha="left")
ax.text(14.6, 10.05, "output 388×388 · 2 classes", fontsize=14, color=DARK, ha="right")
arrow(13.2, 8.95, 13.6, 8.95, "#0f8a8a"); ax.add_patch(Rectangle((13.62, 8.4), 0.12, 1.1, color="#0f8a8a"))
legend = [("#1b3a8c", "conv 3×3, ReLU"), (GREY, "copy and crop"), ("#8b1a1a", "max pool 2×2"), ("#2e8b2e", "up-conv 2×2"), ("#0f8a8a", "conv 1×1")]
for k, (c, t) in enumerate(legend):
    yy = 2.6 - k * 0.45
    arrow(11.0, yy, 11.5, yy, c, lw=3, ms=14); ax.text(11.65, yy, t, va="center", fontsize=13, color=c)
ax.text(0.5, 0.25, "Schematic redrawn after the layer sizes in Ronneberger et al. 2015, Fig. 1", fontsize=11, color="#57606a")
fig.savefig(OUT / "fig1-unet.png", facecolor="white"); plt.close(fig)

# ---------- synthetic touching cells ----------
rng = np.random.default_rng(3)
H = W = 240
seeds = np.array([[50, 60], [55, 150], [70, 215], [120, 40], [115, 110], [125, 180], [185, 70], [180, 150], [205, 215], [30, 105]])
yy, xx = np.mgrid[0:H, 0:W]
d = np.stack([np.hypot(yy - sy, xx - sx) for sy, sx in seeds])
inst = d.argmin(0) + 1
fg = ndi.gaussian_filter(rng.normal(size=(H, W)), 18) > -0.35        # where cells are
fg &= d.min(0) < 52
inst = np.where(fg, inst, 0)
# true borders between different cells
border = np.zeros_like(fg)
for sh in ((0, 1), (1, 0), (1, 1), (1, -1)):
    o = np.roll(inst, sh, axis=(0, 1)); border |= (inst != o) & (inst > 0) & (o > 0)
border = ndi.binary_dilation(border, iterations=1)
labels = fg & ~border
# raw-looking image: soft cells, darker rims, speckle
base = 105 + 12 * ndi.gaussian_filter(rng.normal(size=(H, W)), 2)
rim = ndi.gaussian_filter((ndi.binary_dilation(labels) ^ labels).astype(float) + border * 1.0, 1.2)
cellsoft = ndi.gaussian_filter(labels.astype(float), 3)
raw = base + 18 * cellsoft - 55 * rim + 6 * rng.normal(size=(H, W))
for _ in range(120):
    cy, cx = rng.integers(0, H), rng.integers(0, W)
    if labels[cy, cx]: raw[max(cy-1,0):cy+2, max(cx-1,0):cx+2] -= 40
raw = np.clip(raw, 0, 255).astype(np.uint8)
# Eq. 2 weight map: w = wc + w0 * exp(-(d1+d2)^2 / (2 sigma^2)), w0 = 10, sigma = 5
dist = []
for k in range(1, len(seeds) + 1):
    m = labels & (inst == k)
    dist.append(ndi.distance_transform_edt(~m) if m.any() else np.full((H, W), 1e3))
dist = np.sort(np.stack(dist), axis=0)
wmap = np.where(labels, 1.0, 1.0 + 10 * np.exp(-((dist[0] + dist[1]) ** 2) / (2 * 5.0 ** 2)))
cmap_inst = plt.get_cmap("tab10")
fig = plt.figure(figsize=(13, 3.0), dpi=150)
panels = [("a", raw, "gray", None), ("b", None, None, None), ("c", labels, "gray", None), ("d", wmap, "jet", None)]
for i, (lab, img, cm, _) in enumerate(panels):
    a = fig.add_axes([0.045 + i * 0.245, 0.04, 0.2, 0.2 * 13 / 3.0 * 0.92 if False else 0.92]); a.axis("off")
    if lab == "b":
        over = np.stack([raw / 255.0] * 3, -1)
        col = cmap_inst((inst - 1) % 10)[..., :3]
        over = np.where(labels[..., None], 0.55 * over + 0.45 * col, over)
        a.imshow(over)
    else:
        a.imshow(img, cmap=cm, vmin=None)
    fig.text(0.03 + i * 0.245, 0.9, lab, fontsize=20)
fig.savefig(OUT / "fig3-tmp.png", facecolor="white"); plt.close(fig)
im = Image.open(OUT / "fig3-tmp.png"); w, h = im.size
target_h = round(w * 279 / 1209)
im.crop((0, (h - target_h) // 2, w, (h - target_h) // 2 + target_h)).save(OUT / "fig3-weights.png"); (OUT / "fig3-tmp.png").unlink()

# ---------- augmentation examples (aspect 232:238) ----------
img = Image.fromarray(raw).resize((232, 238), Image.BICUBIC); img.save(OUT / "cells-original.png")
g = np.asarray(img, float); h, w = g.shape
yy, xx = np.mgrid[0:h, 0:w]
for k in range(3):
    s = 16 * h / 250
    dx = ndi.zoom(rng.normal(0, s, (3, 3)), (h / 3, w / 3), order=3)[:h, :w]
    dy = ndi.zoom(rng.normal(0, s, (3, 3)), (h / 3, w / 3), order=3)[:h, :w]
    out = ndi.map_coordinates(g, [yy + dy, xx + dx], order=3, mode="reflect")
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT / f"cells-elastic-{k + 1}.png")
print("done", sorted(p.name for p in OUT.iterdir()))
