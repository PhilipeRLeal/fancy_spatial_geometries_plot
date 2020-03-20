
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

import matplotlib.transforms as transforms
pd.set_option('display.width', 50000)
pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 5000)
from matplotlib.offsetbox import PackerBase
from matplotlib import docstring, transforms
from matplotlib.offsetbox import (AuxTransformBox,AnchoredOffsetbox,
                                  DrawingArea, TextArea, VPacker, HPacker)

#from my_OffsetBox import AnchoredOffsetbox

from matplotlib.patches import (Rectangle, Ellipse, ArrowStyle,
                                FancyArrowPatch, PathPatch)
from matplotlib.text import TextPath
                                  

from my_PackerBase import my_PackerBase
                                
class AnchoredSizeBar(AnchoredOffsetbox):
    
    def __init__(self, transform, size, label, loc='right',
                 pad=0.1, borderpad=0.1, sep=0,
                 frameon=True, size_vertical=0.1, color='black',
                 nbars = 3,
                 bbox_to_anchor = (0.985, 0.952),
                 label_top=False, fontproperties=None, fill_bar=True,
                 **kwargs):
        """
        Draw a horizontal scale bar with a center-aligned label underneath.

        Parameters
        ----------
        transform : `matplotlib.transforms.Transform`
            The transformation object for the coordinate system in use, i.e.,
            :attr:`matplotlib.axes.Axes.transData`.

        size : int or float
            Horizontal length of the size bar, given in coordinates of
            *transform*.

        label : str
            Label to display.

        loc : int
            Location of this size bar. Valid location codes are::

                'upper right'  : 1,
                'upper left'   : 2,
                'lower left'   : 3,
                'lower right'  : 4,
                'right'        : 5,
                'center left'  : 6,
                'center right' : 7,
                'lower center' : 8,
                'upper center' : 9,
                'center'       : 10

        pad : int or float, optional
            Padding around the label and size bar, in fraction of the font
            size. Defaults to 0.1.

        borderpad : int or float, optional
            Border padding, in fraction of the font size.
            Defaults to 0.1.

        sep : int or float, optional
            Separation between the label and the size bar, in points.
            Defaults to 2.

        frameon : bool, optional
            If True, draw a box around the horizontal bar and label.
            Defaults to True.

        size_vertical : int or float, optional
            Vertical length of the size bar, given in coordinates of
            *transform*. Defaults to 0.

        color : str, optional
            Color for the size bar and label.
            Defaults to black.

        label_top : bool, optional
            If True, the label will be over the size bar.
            Defaults to False.

        fontproperties : `matplotlib.font_manager.FontProperties`, optional
            Font properties for the label text.

        fill_bar : bool, optional
            If True and if size_vertical is nonzero, the size bar will
            be filled in with the color specified by the size bar.
            Defaults to True if `size_vertical` is greater than
            zero and False otherwise.

        **kwargs
            Keyworded arguments to pass to
            :class:`matplotlib.offsetbox.AnchoredOffsetbox`.

        Attributes
        ----------
        size_bar : `matplotlib.offsetbox.AuxTransformBox`
            Container for the size bar.

        txt_label : `matplotlib.offsetbox.TextArea`
            Container for the label of the size bar.

        Notes
        -----
        If *prop* is passed as a keyworded argument, but *fontproperties* is
        not, then *prop* is be assumed to be the intended *fontproperties*.
        Using both *prop* and *fontproperties* is not supported.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> from mpl_toolkits.axes_grid1.anchored_artists import (
        ...     AnchoredSizeBar)
        >>> fig, ax = plt.subplots()
        >>> ax.imshow(np.random.random((10,10)))
        >>> bar = AnchoredSizeBar(ax.transData, 3, '3 data units', 4)
        >>> ax.add_artist(bar)
        >>> fig.show()

        Using all the optional parameters

        >>> import matplotlib.font_manager as fm
        >>> fontprops = fm.FontProperties(size=14, family='monospace')
        >>> bar = AnchoredSizeBar(ax.transData, 3, '3 units', 4, pad=0.5,
        ...                       sep=5, borderpad=0.5, frameon=False,
        ...                       size_vertical=0.5, color='white',
        ...                       fontproperties=fontprops)
        """
        
        
        
        if fontproperties is None and 'prop' in kwargs:
            fontproperties = kwargs.pop('prop')

        if fontproperties is None:
            textprops = {'color': color}
        else:
            textprops = {'color': color, 'fontproperties': fontproperties}
            
        
        trans = transforms.blended_transform_factory(
                transform, plt.gcf().transFigure)
            
        
        if fill_bar is None:
            fill_bar = size_vertical > 0


        self.size_bar = AuxTransformBox(transform)
        
        
        self.boxes = []
        ax = plt.gca()
        
        
        for enum, i in enumerate(reversed(range(1,nbars+1))):
            print(i, end='')
    
            if i % 2 == 0:
                facecolor='k'
    
            else:
                facecolor='white'
                
            print('\t {0}'.format(facecolor), end='')
    
        
            label = '{0}'.format(size*(1+enum))
            
            if (1+enum) == nbars:
                label = '{0} units'.format(size*(1+enum))
            
            print('\t {0}'.format(label))



            ###########  

            
            Xsize = size * i
            
            bar = Rectangle((0, 0), 
                            Xsize, 
                            size_vertical,
                            fill=fill_bar, 
                            facecolor=facecolor,
                            transform = trans,
                            edgecolor='k',
                            zorder=10-i
                            )    
            
            
            self.size_bar.add_artist(bar)
    
    
            self.txt_label = TextArea(
                                        label,
                                        minimumdescent=False,
                                        textprops=textprops)
            
            
            
            if label_top:
                _box_children = [self.txt_label, self.size_bar]
            else:
                _box_children = [self.size_bar, self.txt_label]
        
            
            self._box = VPacker(children=_box_children,
                                align="right",
                                pad=pad, sep=sep)
            
            
            self.boxes.append(self._box)
            

        
        for box in self.boxes[:1]:
            
            AnchoredOffsetbox.__init__(self, loc, 
                                       pad=pad, 
                                       borderpad=borderpad,
                                       bbox_to_anchor = bbox_to_anchor,
                                       bbox_transform=plt.gca().transAxes,
                                       child= self._box, 
                                       prop=fontproperties,
                                       frameon=True, **kwargs)
        
        
        self.patch.set_boxstyle("square", pad=0.3)
            



                                
class AnchoredSizeBar2(AnchoredOffsetbox):
    
    def __init__(self, transform, size, label, loc='right',
                 pad=0.1, borderpad=0.1, sep=0,
                 frameon=True, size_vertical=0.1, color='black',
                 nbars = 3,
                 bbox_to_anchor = (0.985, 0.952),
                 label_top=False, fontproperties=None, fill_bar=True,
                 **kwargs):
        """
        Draw a horizontal scale bar with a center-aligned label underneath.

        Parameters
        ----------
        transform : `matplotlib.transforms.Transform`
            The transformation object for the coordinate system in use, i.e.,
            :attr:`matplotlib.axes.Axes.transData`.

        size : int or float
            Horizontal length of the size bar, given in coordinates of
            *transform*.

        label : str
            Label to display.

        loc : int
            Location of this size bar. Valid location codes are::

                'upper right'  : 1,
                'upper left'   : 2,
                'lower left'   : 3,
                'lower right'  : 4,
                'right'        : 5,
                'center left'  : 6,
                'center right' : 7,
                'lower center' : 8,
                'upper center' : 9,
                'center'       : 10

        pad : int or float, optional
            Padding around the label and size bar, in fraction of the font
            size. Defaults to 0.1.

        borderpad : int or float, optional
            Border padding, in fraction of the font size.
            Defaults to 0.1.

        sep : int or float, optional
            Separation between the label and the size bar, in points.
            Defaults to 2.

        frameon : bool, optional
            If True, draw a box around the horizontal bar and label.
            Defaults to True.

        size_vertical : int or float, optional
            Vertical length of the size bar, given in coordinates of
            *transform*. Defaults to 0.

        color : str, optional
            Color for the size bar and label.
            Defaults to black.

        label_top : bool, optional
            If True, the label will be over the size bar.
            Defaults to False.

        fontproperties : `matplotlib.font_manager.FontProperties`, optional
            Font properties for the label text.

        fill_bar : bool, optional
            If True and if size_vertical is nonzero, the size bar will
            be filled in with the color specified by the size bar.
            Defaults to True if `size_vertical` is greater than
            zero and False otherwise.

        **kwargs
            Keyworded arguments to pass to
            :class:`matplotlib.offsetbox.AnchoredOffsetbox`.

        Attributes
        ----------
        size_bar : `matplotlib.offsetbox.AuxTransformBox`
            Container for the size bar.

        txt_label : `matplotlib.offsetbox.TextArea`
            Container for the label of the size bar.

        Notes
        -----
        If *prop* is passed as a keyworded argument, but *fontproperties* is
        not, then *prop* is be assumed to be the intended *fontproperties*.
        Using both *prop* and *fontproperties* is not supported.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> from mpl_toolkits.axes_grid1.anchored_artists import (
        ...     AnchoredSizeBar)
        >>> fig, ax = plt.subplots()
        >>> ax.imshow(np.random.random((10,10)))
        >>> bar = AnchoredSizeBar(ax.transData, 3, '3 data units', 4)
        >>> ax.add_artist(bar)
        >>> fig.show()

        Using all the optional parameters

        >>> import matplotlib.font_manager as fm
        >>> fontprops = fm.FontProperties(size=14, family='monospace')
        >>> bar = AnchoredSizeBar(ax.transData, 3, '3 units', 4, pad=0.5,
        ...                       sep=5, borderpad=0.5, frameon=False,
        ...                       size_vertical=0.5, color='white',
        ...                       fontproperties=fontprops)
        """
        
        
        
        if fontproperties is None and 'prop' in kwargs:
            fontproperties = kwargs.pop('prop')

        if fontproperties is None:
            textprops = {'color': color}
        else:
            textprops = {'color': color, 'fontproperties': fontproperties}
            
        
        trans = transforms.blended_transform_factory(
                transform, plt.gcf().transFigure)
            
        
        if fill_bar is None:
            fill_bar = size_vertical > 0


        self.size_bar = AuxTransformBox(transform)
        

        ###########  

        
        
        bar = Rectangle((0, 0), 
                        size, 
                        size_vertical,
                        fill=fill_bar, 
                        facecolor=color,
                        transform = trans,
                        edgecolor='k',
                        )    
        
        
        self.size_bar.add_artist(bar)


        self.txt_label = TextArea(
                                    label,
                                    minimumdescent=False,
                                    textprops=textprops)
        
        
        
        if label_top:
            _box_children = [self.txt_label, self.size_bar]
        else:
            _box_children = [self.size_bar, self.txt_label]
    
        
        self._box = VPacker(children=_box_children,
                            align="right",
                            pad=pad, sep=sep)
        
        

        AnchoredOffsetbox.__init__(self, loc, 
                                   pad=pad, 
                                   borderpad=borderpad,
                                   bbox_to_anchor = bbox_to_anchor,
                                   bbox_transform=plt.gca().transAxes,
                                   child= self._box, 
                                   prop=fontproperties,
                                   frameon=frameon, **kwargs)
    
        
        #self.patch.set_boxstyle("square", pad=0.3)
            
                        