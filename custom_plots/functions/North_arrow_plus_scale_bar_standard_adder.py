
from .north_arrow import add_north_arrow_to_fig

from .scale_bar import scale_bar_class
import numpy as np


def add_standard_north_arrow_with_scale_bar(ax, 
                                            distance=300, 
                                            units='km',
                                            x0=0.85,
                                            y0=0.05,
                                            x1=0.85,
                                            y1=0.085, 
                                            arrow_xshift=0.1,
                                            arrow_yshift=0.1):
    
    box = scale_bar_class.get_scalebar_with_rounded_kilometer_distance_based(ax=ax, 
                                                                             distance_in_km=distance, 
                                                                             length_unit=units,
                                                                             rounding_value_for_xsize=0,
                                                                             pad=0.5,sep=2, borderpad=5, 
                                                                             background_facecolor=(1,1,1,0.5),
                                                                             background_edgecolor ='k',
                                                                             background_facealpha=1,
                                                                             x0=x0,
                                                                             y0=y0,
                                                                             x1=x1,
                                                                             y1=y1)
    
    xmean = np.mean([x0, x1]) + arrow_xshift
    
    y0 += arrow_yshift
    
    y1 += arrow_yshift
    
    add_north_arrow_to_fig(fig=ax.get_figure(), 
                           x_tail=xmean,
                            y_tail=y0,
                            x_head=xmean,
                            y_head=y1)
    
    
    