# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:38:58 2020

@author: Philipe_Leal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
import glob

from fancy_spatial_geometries_plot import custom_plots

gdf = custom_plots.get_standard_gdf()


def wraper_plotting(ax):
    custom_plots.add_background(ax)
    
    
    scale_kwds = dict(location=(1.1, 0.1), 
                        length=200,
                          
                        metres_per_unit=1000, 
                        unit_name='km',
                        tol=0.01, 
                        angle=0,
                        dy = 0.05,
                        max_stripes=3,
                        ytick_label_margins = 0.25,
                        fontsize= 8,
                        font_weight='bold',
                        rotation = 45,
                        zorder=999,
                        paddings = {'xmin':0.1,
                                    'xmax':0.1,
                                    'ymin':0.3,
                                    'ymax':0.3},
           
                        bbox_kwargs = {'facecolor':'w',
                                       'edgecolor':'k',
                                       'alpha':0.7},
                                       
                        add_numeric_scale_bar=True,
                        
                        numeric_scale_bar_kwgs={'x_text_offset':0,
                                                
                                         'y_text_offset':-30,
                                         'box_x_coord':0.5,
                                         'box_y_coord':0.01}
                 )
    
    custom_plots.add_north_arrow_to_fig(ax.get_figure(),
                                        x_tail = 0.892,
                                        y_tail = 0.8,
                                        x_head = 0.892,
                                        y_head = 0.85,
                                        width=0.05,
                    						label_pad=0.012,
                                            transform=ax.transAxes)
    custom_plots.fancy_scalebar(ax, **scale_kwds)
    


    gl = custom_plots.add_custom_gridline(geo_axes=ax, 
                    
                        gridline_attr=dict(draw_labels=True,
                                       linewidth=1, 
                                    color='black', 
                                    alpha=0.35, 
                                    linestyle='--'),
                                       
                        n_coordinate_ticks={'x_number':3,  'y_number':3},
                    
                        gridline_tick_formating=dict(latitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                              'degree_symbol':'°', # u'\u00B0'
                                                              'north_hemisphere_str': 'N',
                                                              'south_hemisphere_str': 'S'} ,
                                                       

                        longitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                               'degree_symbol':'°', # u'\u00B0'
                                                               'dateline_direction_label':True, # ONLY APPLICABLE TO LONGITUDE DATA
                                                               'west_hemisphere_str': 'O',
                                                               'east_hemisphere_str': 'L'}) ,
                    
						gridline_xlabel_style = {'color': 'black', 
                                               #'weight': 'bold', 
                                               'rotation':90,
                                               'fontsize':10},
                 
                        gridline_ylabel_style = {'color': 'black', 
                                           #'weight': 'bold', 
                                           'rotation':0,
                                           'fontsize':10},  
							
							
    
                    
						gridline_tick_axis_positions={'xlabels_top':False,
												 'ylabels_left':True,
												 'ylabels_right':False,
												 'xlabels_bottom':True}		,
                                
                        decimal_separator='.',										   
                        geographical_symbol='°'
                        )
    
    plt.draw()
    
#########################################3
    
    
projection = ccrs.PlateCarree()

cm = 1/2.54  # centimeters in inches
height = 21 # in cm
width = 29.7 # in cm
fig, ax = plt.subplots(figsize=(height*cm, width*cm), subplot_kw={'projection':projection})
gdf.plot(ax=ax)
wraper_plotting(ax)

fig.subplots_adjust(top=0.97,
bottom=0.111,
left=0.113,
right=0.672,
hspace=0.2,
wspace=0.2)

fig.show()
