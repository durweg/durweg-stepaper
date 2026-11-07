# How the example slides are built

All figures are self-made; no image comes from the U-Net paper.

1. `uv run --no-project --with matplotlib --with numpy --with scipy --with pillow python -I make_figures.py figures`
   draws the U-Net schematic (after the layer sizes in the paper's Fig. 1), synthetic touching cells with the weight map of the paper's Eq. 2, and elastic deformations as Section 3.1 describes.
2. `uv run --no-project --with python-pptx python -I build_en.py .. figures` (likewise `build_zh.py`, `build_de.py`) writes `../unet-slides-<lang>.pptx`.

The previews `../preview-<lang>.png` are the slides exported by Microsoft PowerPoint, ten per image.
