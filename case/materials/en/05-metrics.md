[中文](../zh/05-metrics.md) · [English](../en/05-metrics.md) · [Deutsch](../de/05-metrics.md)

# Metrics guide

**Overview**

| Metric | Where in the paper | Better when | Human / best value in the paper | U-Net |
|---|---|---|---|---|
| Warping error | EM task, Table 1 | lower | human 0.000005 | 0.000353 (rank 1) |
| Rand error | EM task, Table 1 | lower | human 0.0021 | 0.0382 |
| Pixel error | EM task, Table 1 | lower | human 0.0010 | 0.0611 |
| IOU | cell tasks, Table 2 | higher (max 1) | — | 0.92 (PhC-U373), 0.78 (DIC-HeLa) |

### Pixel error

- **What it is for**: the simplest check — how many pixels got the wrong label (cell vs membrane).
- **How to read it**: the share of wrong pixels, from 0 (all right) to 1 (all wrong); lower is better. U-Net's 0.0611 means about 6 % of pixels are wrong.
- **Watch out**: it counts every pixel equally, so a one-pixel break in a thin membrane, which merges two cells, hardly changes it. That is why the EM challenge also uses the next two metrics.

### Rand error

- **What it is for**: checks whether the image is cut into the right **objects** (cells), not just whether pixels are right.
- **How to read it**: take pairs of pixels and ask "same cell or different cells?"; the Rand error is the share of pairs where the answer differs from the ground truth. From 0 to 1; lower is better. U-Net 0.0382 ≈ 4 % of pairs judged wrong.
- **Watch out**: a small gap in a membrane that merges two cells makes many pairs wrong, so this metric punishes merges and splits that pixel error barely sees.

### Warping error

- **What it is for**: counts only **topological** mistakes — cells wrongly merged, split, or with holes — and forgives small shifts of the borders.
- **How to read it**: the result is first allowed to bend slightly towards the ground truth wherever that does not change the topology; the pixels still wrong afterwards are the warping error. Lower is better; the numbers are tiny (U-Net 0.000353 vs human 0.000005), so compare them with each other, not with pixel error.
- **Why it matters here**: Table 1 is sorted by this metric, and it is the one on which U-Net ranks first.

The three EM metrics are computed by the challenge organizers on their secret test answers; they threshold the predicted membrane map at 10 levels and report the result (p. 6).

### IOU (intersection over union)

- **What it is for**: how well the predicted cell area overlaps the true cell area.
- **How to read it**: overlap ÷ the area covered by either of them; 1 = perfect match, 0 = no overlap; higher is better. U-Net 0.92 on PhC-U373 vs 0.83 for the second best; 0.78 on DIC-HeLa vs 0.46.
- **Watch out**: it is an average over the dataset, given without error bars, so the paper's "significantly better" is not backed by a statistical test.

### In one sentence each (to retell)

- **Pixel error**: share of wrong pixels — lower is better.
- **Rand error**: share of pixel pairs put in the wrong "same / different cell" group — lower is better; punishes merged or split cells.
- **Warping error**: only the mistakes that change the shape of the cell layout (merges, splits, holes) — lower is better; U-Net ranks first on it.
- **IOU**: overlap ÷ union of predicted and true area — higher is better, 1 is perfect.
