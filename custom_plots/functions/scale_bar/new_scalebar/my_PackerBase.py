
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:48:35 2020

@author: lealp
"""


import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from glob import glob


import pandas as pd
pd.set_option('display.width', 50000)
pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 5000)


from matplotlib.offsetbox import PackerBase

from matplotlib.patches import (
    FancyBboxPatch, FancyArrowPatch, bbox_artist as mbbox_artist)
from matplotlib.text import _AnnotationBase
from matplotlib.transforms import Bbox, BboxBase, TransformedBbox


DEBUG = False


# for debugging use
def bbox_artist(*args, **kwargs):
    if DEBUG:
        mbbox_artist(*args, **kwargs)


def _get_aligned_offsets(hd_list, height, align="baseline"):
    """
    Given a list of (height, descent) of each boxes, align the boxes
    with *align* and calculate the y-offsets of each boxes.
    total width and the offset positions of each items according to
    *mode*. xdescent is analogous to the usual descent, but along the
    x-direction. xdescent values are currently ignored.

    *hd_list* : list of (width, xdescent) of boxes to be aligned.
    *sep* : spacing between boxes
    *height* : Intended total length. None if not used.
    *align* : align mode. 'baseline', 'top', 'bottom', or 'center'.
    """

    if height is None:
        height = max(h for h, d in hd_list)

    if align == "baseline":
        height_descent = max(h - d for h, d in hd_list)
        descent = max(d for h, d in hd_list)
        height = height_descent + descent
        offsets = [0. for h, d in hd_list]
    elif align in ["left", "top"]:
        descent = 0.
        offsets = [d for h, d in hd_list]
    elif align in ["right", "bottom"]:
        descent = 0.
        offsets = [height - h + d for h, d in hd_list]
    elif align == "center":
        descent = 0.
        offsets = [(height - h) * .5 + d for h, d in hd_list]
    else:
        raise ValueError("Unknown Align mode : %s" % (align,))

    return height, descent, offsets


def _get_packed_offsets(wd_list, total, sep, mode="fixed"):
    """
    Given a list of (width, xdescent) of each boxes, calculate the
    total width and the x-offset positions of each items according to
    *mode*. xdescent is analogous to the usual descent, but along the
    x-direction. xdescent values are currently ignored.

    *wd_list* : list of (width, xdescent) of boxes to be packed.
    *sep* : spacing between boxes
    *total* : Intended total length. None if not used.
    *mode* : packing mode. 'fixed', 'expand', or 'equal'.
    """

    w_list, d_list = zip(*wd_list)
    # d_list is currently not used.

    if mode == "fixed":
        offsets_ = np.cumsum([0] + [w + sep for w in w_list])
        offsets = offsets_[:-1]
        if total is None:
            total = offsets_[-1] - sep
        return total, offsets

    elif mode == "expand":
        # This is a bit of a hack to avoid a TypeError when *total*
        # is None and used in conjugation with tight layout.
        if total is None:
            total = 1
        if len(w_list) > 1:
            sep = (total - sum(w_list)) / (len(w_list) - 1)
        else:
            sep = 0
        offsets_ = np.cumsum([0] + [w + sep for w in w_list])
        offsets = offsets_[:-1]
        return total, offsets

    elif mode == "equal":
        maxh = max(w_list)
        if total is None:
            total = (maxh + sep) * len(w_list)
        else:
            sep = total / len(w_list) - maxh
        offsets = (maxh + sep) * np.arange(len(w_list))
        return total, offsets

    else:
        raise ValueError("Unknown mode : %s" % (mode,))


class my_PackerBase(PackerBase):
    
    
    def draw(self, renderer):
        """
        Update the location of children if necessary and draw them
        to the given *renderer*.
        """
        width, height, xdescent, ydescent, offsets = self.get_extent_offsets(
                                                        renderer)

        px, py = self.get_offset(width, height, xdescent, ydescent, renderer)

        for c, (ox, oy) in zip(self.get_visible_children(), offsets):
            c.set_offset((px, py))
            c.draw(renderer)

        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
        
    def get_extent_offsets(self, renderer):
        # docstring inherited
        dpicor = renderer.points_to_pixels(1.)
        pad = self.pad * dpicor
        sep = self.sep * dpicor

        if self.width is not None:
            for c in self.get_visible_children():
                if isinstance(c, PackerBase) and c.mode == "expand":
                    c.set_width(self.width)

        whd_list = [c.get_extent(renderer)
                    for c in self.get_visible_children()]
        whd_list = [(w, h, xd, (h - yd)) for w, h, xd, yd in whd_list]

        wd_list = [(w, xd) for w, h, xd, yd in whd_list]
        width, xdescent, xoffsets = _get_aligned_offsets(wd_list,
                                                         self.width,
                                                         self.align)

        pack_list = [(h, yd) for w, h, xd, yd in whd_list]
        height, yoffsets_ = _get_packed_offsets(pack_list, self.height,
                                                sep, self.mode)

        yoffsets = yoffsets_ + [yd for w, h, xd, yd in whd_list]
        ydescent = height - yoffsets[0]
        yoffsets = height - yoffsets

        yoffsets = yoffsets - ydescent

        return (width + 2 * pad, height + 2 * pad,
                xdescent + pad, ydescent + pad,
                list(zip(xoffsets, yoffsets)))


