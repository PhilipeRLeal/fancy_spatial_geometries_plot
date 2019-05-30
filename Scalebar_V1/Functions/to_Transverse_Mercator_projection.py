# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:49:20 2019

@author: lealp
"""


def get_local_TransVerse_Mercator_Projection_for_given_geoaxes(ax, x_size_in_data_units):
    """
    ax is the axes to draw the scalebar on.
    length is the length of the scalebar in km.
    location is center of the scalebar in axis coordinates.
    (ie. 0.5 is the middle of the plot)
    linewidth is the thickness of the scalebar.
    """
    import cartopy.crs as ccrs
    
    location=(0.5, 0.05)
    #Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ax.projection)
    #Make tmc horizontally centred on the middle of the map,
    #vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    
    relative_ax_size = x_size_in_data_units/abs(llx1 - llx0)
    
    return tmc, relative_ax_size