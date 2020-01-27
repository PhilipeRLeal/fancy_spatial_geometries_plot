# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:59:05 2020

@author: lealp
"""

import pandas as pd
pd.set_option('display.width', 50000)
pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 5000)


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText

def main(projection = ccrs.PlateCarree(), drawlicense=True):
    
    fig = plt.figure(figsize=(9,7))
    ax = plt.axes(projection=projection)
    

    # Put a background image on for nice sea rendering.
    ax.stock_img()

    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    SOURCE = 'Natural Earth'
    LICENSE = 'public domain'

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(states_provinces, edgecolor='gray')

    # Add a text annotation for the license information to the
    # the bottom right corner.
    
    if drawlicense:
        
        text = AnchoredText(r'$\mathcircled{{c}}$ {}; license: {}'
                            ''.format(SOURCE, LICENSE),
                            loc='right',
                            bbox_transform=ax.transAxes,
                            bbox_to_anchor=(1.01, -0.11), 
                            prop={'size': 8}, 
                            frameon=False)
        
        ax.add_artist(text)

    plt.show()

    return ax


ax = main()
fig = ax.get_figure()
gridliner = ax.gridlines(draw_labels=True)


def add_zebra(gridliner, pad=1):
    
    
    ax = gridliner.axes
    fig = ax.get_figure()
    
    
    fig.canvas.draw()   
    
    lon0, lon1, lat0, lat1 = ax.get_extent(crs=ax.projection)
    
    ysegs = gridliner.yline_artists[0].get_segments()
    yticks = [yseg[0,1] for yseg in ysegs]
    
    xsegs = gridliner.xline_artists[0].get_segments()
    xticks = [xseg[0,0] for xseg in xsegs]
    xticks.append(lon1)
    
    i = 0
    
    colors_wk = ['white', 'black']
    
    for lon in (lon0, lon1 - pad):
        y0 = xticks[0]
        for enum, y in enumerate(yticks[1:]):
            
            color = colors_wk[i]
            
            delta_coor = (y - y0)
            
            rect = mpatches.Rectangle( (lon, y0), pad , delta_coor, 
                                      transform=ax.transData,
                                      facecolor=color, zorder=1000)
            
            i = 1 - i
            y0 = y
            
            ax.add_patch(rect)
    
    
    
    for lat in (lat0, lat1 - pad):
        x0 = xticks[0]
        for x in xticks[1:]:
            
            color = colors_wk[i]
            
            delta_coor = (x - x0)
            
            
            rect = mpatches.Rectangle( (x0, lat), delta_coor, pad ,
                                      transform=ax.transData,
                                      facecolor=color, zorder=1000)
            
            x0 = x
            
            i = 1 - i
            
            ax.add_patch(rect)
    
    
    
    
    if ax.projection.proj4_params.get('units', 'None') == 'None':
    
        if not (lon0 <=-180 or lon1 >= 180 or lat0>=90 or lat0<=-90):
    
            ax.set_extent(lon0-pad, lon1+pad, lat0-pad, lat1+pad)

add_zebra(gridliner, pad=2)

fig.show()









