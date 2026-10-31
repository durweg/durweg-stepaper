[中文](../zh/03-core-claim.md) · [English](../en/03-core-claim.md) · [Deutsch](../de/03-core-claim.md)

# Core claim

**The concrete problem**: in medical images, every **single pixel** has to get a class label (segmentation), but often only a few dozen annotated training images exist. Deep networks at the time usually needed thousands of annotated images.

The best method before (Ciresan et al., sliding window): cut a small patch around one pixel and decide which class that pixel belongs to. The paper names two drawbacks (introduction):
1. Slow: the network runs separately for every patch; neighbouring patches overlap heavily, so much is computed twice.
2. A trade-off: a large patch sees more context but localizes coarsely; a small patch localizes well but sees little context.

**Core claim**: a U-shaped network (first shrink the image to capture the whole, then enlarge it back to localize, passing the details from the shrinking side straight across), combined with heavy data augmentation (above all elastic deformations), **can be trained from very few annotated images and segments more accurately and faster than the sliding-window method**.

**Evidence the paper gives (abstract)**:
- Neuronal structures in electron microscopy (ISBI 2012): better than the previous best sliding-window method.
- Cell segmentation in light microscopy (ISBI cell tracking challenge 2015): won by a large margin on the two hardest datasets.
- Speed: a 512×512 image takes less than a second on a GPU.
