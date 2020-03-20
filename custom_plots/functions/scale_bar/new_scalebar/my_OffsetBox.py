from matplotlib.offsetbox import OffsetBox
from matplotlib.transforms import Bbox, BboxBase, TransformedBbox

from matplotlib import cbook, docstring, rcParams
import matplotlib.artist as martist
import matplotlib.path as mpath
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties
from matplotlib.image import BboxImage
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, bbox_artist as mbbox_artist)
from matplotlib.text import _AnnotationBase


class AnchoredOffsetbox(OffsetBox):
    """
    An offset box placed according to the legend location
    loc. AnchoredOffsetbox has a single child. When multiple children
    is needed, use other OffsetBox class to enclose them.  By default,
    the offset box is anchored against its parent axes. You may
    explicitly specify the bbox_to_anchor.
    """
    zorder = 5  # zorder of the legend

    # Location codes
    codes = {'upper right': 1,
             'upper left': 2,
             'lower left': 3,
             'lower right': 4,
             'right': 5,
             'center left': 6,
             'center right': 7,
             'lower center': 8,
             'upper center': 9,
             'center': 10,
             }

    def __init__(self, loc,
                 pad=0.4, borderpad=0.5,
                 child=None, prop=None, frameon=True,
                 bbox_to_anchor=None,
                 bbox_transform=None,
                 **kwargs):
        """
        loc is a string or an integer specifying the legend location.
        The valid location codes are::

        'upper right'  : 1,
        'upper left'   : 2,
        'lower left'   : 3,
        'lower right'  : 4,
        'right'        : 5, (same as 'center right', for back-compatibility)
        'center left'  : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center'       : 10,

        pad : pad around the child for drawing a frame. given in
          fraction of fontsize.

        borderpad : pad between offsetbox frame and the bbox_to_anchor,

        child : OffsetBox instance that will be anchored.

        prop : font property. This is only used as a reference for paddings.

        frameon : draw a frame box if True.

        bbox_to_anchor : bbox to anchor. Use self.axes.bbox if None.

        bbox_transform : with which the bbox_to_anchor will be transformed.

        """
        super().__init__(**kwargs)

        self.set_bbox_to_anchor(bbox_to_anchor, bbox_transform)
        self.set_child(child)

        if isinstance(loc, str):
            try:
                loc = self.codes[loc]
            except KeyError:
                raise ValueError('Unrecognized location "%s". Valid '
                                 'locations are\n\t%s\n'
                                 % (loc, '\n\t'.join(self.codes)))

        self.loc = loc
        self.borderpad = borderpad
        self.pad = pad

        if prop is None:
            self.prop = FontProperties(size=rcParams["legend.fontsize"])
        elif isinstance(prop, dict):
            self.prop = FontProperties(**prop)
            if "size" not in prop:
                self.prop.set_size(rcParams["legend.fontsize"])
        else:
            self.prop = prop

        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True
            )
        self.patch.set_boxstyle("square", pad=1)
        self._drawFrame = frameon

    def set_child(self, child):
        "set the child to be anchored"
        self._child = child
        if child is not None:
            child.axes = self.axes
        self.stale = True


    def get_child(self):
        "return the child"
        return self._child


    def get_children(self):
        "return the list of children"
        return [self._child]


    def get_extent(self, renderer):
        """
        return the extent of the artist. The extent of the child
        added with the pad is returned
        """
        w, h, xd, yd = self.get_child().get_extent(renderer)
        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        pad = self.pad * fontsize

        return w + 2 * pad, h + 2 * pad, xd + pad, yd + pad


    def get_bbox_to_anchor(self):
        """
        return the bbox that the legend will be anchored
        """
        if self._bbox_to_anchor is None:
            return self.axes.bbox
        else:
            transform = self._bbox_to_anchor_transform
            if transform is None:
                return self._bbox_to_anchor
            else:
                return TransformedBbox(self._bbox_to_anchor,
                                       transform)


    def set_bbox_to_anchor(self, bbox, transform=None):
        """
        set the bbox that the child will be anchored.

        *bbox* can be a Bbox instance, a list of [left, bottom, width,
        height], or a list of [left, bottom] where the width and
        height will be assumed to be zero. The bbox will be
        transformed to display coordinate by the given transform.
        """
        if bbox is None or isinstance(bbox, BboxBase):
            self._bbox_to_anchor = bbox
        else:
            try:
                l = len(bbox)
            except TypeError:
                raise ValueError("Invalid argument for bbox : %s" % str(bbox))

            if l == 2:
                bbox = [bbox[0], bbox[1], 0, 0]

            self._bbox_to_anchor = Bbox.from_bounds(*bbox)

        self._bbox_to_anchor_transform = transform
        self.stale = True


    def get_window_extent(self, renderer):
        '''
        get the bounding box in display space.
        '''
        self._update_offset_func(renderer)
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset(w, h, xd, yd, renderer)
        return Bbox.from_bounds(ox - xd, oy - yd, w, h)


    def _update_offset_func(self, renderer, fontsize=None):
        """
        Update the offset func which depends on the dpi of the
        renderer (because of the padding).
        """
        if fontsize is None:
            fontsize = renderer.points_to_pixels(
                            self.prop.get_size_in_points())

        def _offset(w, h, xd, yd, renderer, fontsize=fontsize, self=self):
            bbox = Bbox.from_bounds(0, 0, w, h)
            borderpad = self.borderpad * fontsize
            bbox_to_anchor = self.get_bbox_to_anchor()

            x0, y0 = self._get_anchored_bbox(self.loc,
                                             bbox,
                                             bbox_to_anchor,
                                             borderpad)
            return x0 + xd, y0 + yd

        self.set_offset(_offset)

    def update_frame(self, bbox, fontsize=None):
        self.patch.set_bounds(bbox.x0, bbox.y0,
                              bbox.width, bbox.height)

        if fontsize:
            self.patch.set_mutation_scale(fontsize)


    def draw(self, renderer):
        "draw the artist"

        if not self.get_visible():
            return

        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        self._update_offset_func(renderer, fontsize)

        if self._drawFrame:
            # update the location and size of the legend
            bbox = self.get_window_extent(renderer)
            self.update_frame(bbox, fontsize)
            self.patch.draw(renderer)

        width, height, xdescent, ydescent = self.get_extent(renderer)

        px, py = self.get_offset(width, height, xdescent, ydescent, renderer)

        self.get_child().set_offset((px, py))
        self.get_child().draw(renderer)
        self.stale = False


    def _get_anchored_bbox(self, loc, bbox, parentbbox, borderpad):
        """
        return the position of the bbox anchored at the parentbbox
        with the loc code, with the borderpad.
        """
        assert loc in range(1, 11)  # called only internally

        BEST, UR, UL, LL, LR, R, CL, CR, LC, UC, C = range(11)

        anchor_coefs = {UR: "NE",
                        UL: "NW",
                        LL: "SW",
                        LR: "SE",
                        R: "E",
                        CL: "W",
                        CR: "E",
                        LC: "S",
                        UC: "N",
                        C: "C"}

        c = anchor_coefs[loc]

        container = parentbbox.padded(-borderpad)
        anchored_box = bbox.anchored(c, container=container)
        return anchored_box.x0, anchored_box.y0
