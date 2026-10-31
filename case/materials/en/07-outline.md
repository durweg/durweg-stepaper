[中文](../zh/07-outline.md) · [English](../en/07-outline.md) · [Deutsch](../de/07-outline.md)

# Slide outline

10 slides (the default is 8; "method" is split into 3 slides so each covers one thing). Each slide: title = its one-sentence conclusion; below, what goes on it.

| # | Question it answers | Title (one-sentence conclusion) | Content |
|---|---|---|---|
| 1 | What problem does the paper solve? | A few dozen annotated images are enough to train a precise segmentation network | Title, authors, venue; the core claim in one sentence |
| 2 | What was wrong with the earlier method? | The sliding window decides patch by patch: slow, and "seeing wide" and "locating precisely" pull against each other | Own sketch: a patch moving across the image step by step; one line per drawback |
| 3 | Method 1: what does the network look like? | U-Net = encoder–decoder + a skip connection at every level, whole image out at once | Paper Fig. 1; mark shrinking left side, enlarging right side, copied detail across |
| 4 | Method 2: what if there are too few images? | Elastic deformation turns existing images into new ones, without new annotation | Original vs three deformed versions; why tissue suits elastic deformation |
| 5 | Method 3: how are touching cells separated? | Weight the narrow gaps between cells so the network learns to separate them | Paper Fig. 3 (c segmentation map, d weight map) |
| 6 | What does each part solve? | Each part answers one of the original problems | Three rows: U shape → trade-off and speed; augmentation → few data; weighting → merged cells |
| 7 | How was it tested? | Three public challenges, the answers held by the organizers | Table: dataset, image type, training images (30 / 35 / 20), metric |
| 8 | What are the results (A vs B)? | Without post-processing, U-Net already beats the sliding window | Table 1 excerpt: U-Net vs IDSIA (warping 0.000353 vs 0.000420, Rand 0.0382 vs 0.0504); Table 2: IOU 0.92 vs 0.83, 0.78 vs 0.46 |
| 9 | How reliable is the conclusion? | The scores are credible, but there is no evidence for why it is better | Four reservations: sliding window with post-processing has better Rand error (0.0189, 0.0305); no ablation; "faster" not measured under equal conditions; microscopy only |
| 10 | What do we take away? | The architecture can be used directly; a new task needs its own experiments | A-vs-B retelling in one sentence; discussion: ① which ablations first on our data? ② padding or no padding? |
