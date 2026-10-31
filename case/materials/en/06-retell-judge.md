[中文](../zh/06-retell-judge.md) · [English](../en/06-retell-judge.md) · [Deutsch](../de/06-retell-judge.md)

# Retell and judge

### Retelling (A vs B)

- **A**: U-Net (whole image in at once, U-shaped network + skip connections, with elastic-deformation augmentation and a weighted loss for the gaps between cells).
- **B**: the sliding-window network (Ciresan et al., deciding one small patch at a time).
- **Conclusion**: on segmentation tasks, U-Net works better.

### Judgement

**Did the paper solve its problem?** Yes, for segmentation tasks with small datasets.

**How strong is the evidence?** All metrics and rankings were given fairly by the challenge organizers, so the evidence is very credible.
Claude's addition (kept by the user): what is credible is the scores themselves. By Rand error, the sliding window with dataset-specific post-processing (IDSIA-SCI 0.0189, DIVE-SCI 0.0305) beats U-Net (0.0382), so more precisely: "without post-processing, U-Net is better".

**My reservation**: there is no ablation experiment, so the credit cannot be split between the network architecture, elastic deformation and the weighted loss. Moving the method to other datasets may therefore need more tuning (network architecture, post-processing) to get the best result.

**Did I reach my goal (understanding this paper)?** Yes. I understood the network design, and the training and results in the challenges; I also understood their "post-processing methods" (note: U-Net itself adds no post-processing; this means training methods such as data augmentation and the weighted loss). To reuse their method for my own task, many extra experiments are needed to adapt it.
