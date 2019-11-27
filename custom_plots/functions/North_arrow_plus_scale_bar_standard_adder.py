
from .north_arrow import add_north_arrow_to_fig

from .scale_bar import scale_bar_class



def add_standard_north_arrow_with_scale_bar(ax, distance=300, units='km'):
    
    box = scale_bar_class.get_scalebar_with_rounded_kilometer_distance_based(ax=ax, 
                                                                             distance_in_km=distance, 
                                                                             length_unit=units,
                                                                             rounding_value_for_xsize=0,
                                                                             pad=0.5,sep=2, borderpad=5, 
                                                                             background_facecolor=(1,1,1,0.5),
                                                                             background_edgecolor ='k',
                                                                             background_facealpha=1,
                                                                             x0=0.952,
                                                                             y0=0.05,
                                                                             x1=0.95,
                                                                             y1=0.085)
    
    xmean = scale_bar_class.get_central_x_point_from_scalebar_in_fig_coordinates(box)  
    
    add_north_arrow_to_fig(fig=ax.get_figure(), 
                           x_tail=xmean,
                            y_tail=0.11,
                            x_head=xmean,
                            y_head=0.14,)
    
    
    