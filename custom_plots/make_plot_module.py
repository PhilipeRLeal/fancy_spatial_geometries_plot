# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:56:32 2019

@author: lealp
"""

import pandas as pd


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import matplotlib

import sys
import os

sys.path.insert(0,r'C:\Users\lealp\Dropbox\Profissao\Python\OSGEO\OGR_Vetor\Geopandas\custom_plots\custom_plots')

from functions import colorbars, north_arrow, scale_bar, North_arrow_plus_scale_bar_standard_adder

from functions.geoaxes_tick_formatting.gridline_tick_formatters_module import add_custom_gridline

from functions.zebra_axis_tick import add_zebra


custom_cbar = colorbars.custom_colorbars



def make_cbars(ax, vmin, vmax, colorbar_ax_yticks_format='%.0f'):
    
    cbar = custom_cbar.add_colorbar_for_axes(axes=ax, vmax=vmax, vmin=vmin, colorbar_ax_yticks_format=colorbar_ax_yticks_format)
    
    return cbar


def make_fig():
    
    Projection = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(3,4, sharex=True, sharey=True, subplot_kw={'projection':Projection}, figsize=(12,6.5))
    
    return fig, ax

def add_background(ax):
    
    import cartopy.feature as cfeature
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

    ax.add_feature(states_provinces, edgecolor='gray')
    


def add_north_arrow(fig, xmean, y_tail=0.11, y_head=0.14,):
    north_arrow.add_north_arrow_to_fig(fig=fig, 
                                   x_tail=xmean,
                                    y_tail=y_tail,
                                    x_head=xmean,
                                    y_head=y_head)

def add_gridlines(ax,
                  
                  decimal_separator='.',
                  
                  gridline_tick_formating=dict(latitude_tick_formating={'number_format':'.1f', # com duas casas decimais
                                                                      'degree_symbol':'°', # u'\u00B0'
                                                                      'north_hemisphere_str': 'N',
                                                                      'south_hemisphere_str': 'S'} ,
                                                               
        
                                                      longitude_tick_formating={'number_format':'.1f', # com duas casas decimais
                                                                       'degree_symbol':'°', # u'\u00B0'
                                                                       'dateline_direction_label':True, # ONLY APPLICABLE TO LONGITUDE DATA
                                                                       'west_hemisphere_str': 'W',
                                                                       'east_hemisphere_str': 'E'}
                                                                       
                                                        ) ,
                                           
                  n_coordinate_ticks={'x_number':4,  'y_number':3},                      
                                                                                
                  gridline_xlabel_style={'color': 'black', 'rotation': 90, 'fontsize': 7},
                  
                  gridline_ylabel_style={'color': 'black', 'rotation': 0, 'fontsize': 7},
                  
                  gridline_attr=dict(draw_labels=True,
                                               linewidth=1, 
                                            color='black', 
                                            alpha=0.35, 
                                            linestyle='--'),
                                     
                  gridline_tick_axis_positions={'xlabels_top':False,
    												 'ylabels_left':True,
    												 'ylabels_right':False,
    												 'xlabels_bottom':True}		,
                  
                  
                  ):
    
    
    gridline = add_custom_gridline(ax,
                                   gridline_attr= gridline_attr,
                                   n_coordinate_ticks=n_coordinate_ticks,
                                   gridline_tick_axis_positions=gridline_tick_axis_positions,
                                   gridline_tick_formating=gridline_tick_formating,
                                   gridline_xlabel_style= gridline_xlabel_style,
                                   gridline_ylabel_style=gridline_ylabel_style)
    zebra_gridlines={'add':True,
                                   'pad':2}
    if zebra_gridlines['add']:
        add_zebra(gridline, pad=zebra_gridlines['pad'])                      

    return gridline
 




###########
  

class make_plot():
    """
    Description:
        This class creates a custom multiplot of 12 geoaxes (3 rows and 4 columns).
        
        Axes[10] = Temporal Mean of the data (aggregation over time using the mean function)
        
        Axes[11] = Temporal Sum of the data (aggregation over time using the sum function)
        
        Each geoaxes has its ticks formatted according to a predetermined formatting function
        
    Requirements:
        
        This class requires that the geodataframe possess a datetime attribute so to aggregate data over that dimension.
        
    
    How to use it:
       
        
        This class can be thought as a plotting formatting function, which can be called once at least 1 instance 
        of it has been created. 
        
        
        Once its instance is created, the instance can be called as a normal function so to plot other spatio-temporal data
        
    """
    
    
    
    def __init__(self, gdf, vmin, vmax, column, datetime_column_name='Datetime',
                 temporal_aggregation_attribute_name='COD_MUNIC_6',
                 gdf_TIME_Aggregated_1=None,
                 gdf_TIME_Aggregated_2=None,
                 colorbar_formatting_string='%.2f', temporal_aggregators=['mean', 'sum']):
        
        self.gdf = gdf
        self.vmin = vmin
        self.vmax = vmax
        self.column = column
        self.datetime_column_name = datetime_column_name
        self.temporal_aggregation_attribute_name =  temporal_aggregation_attribute_name
        self.title_fontsize = 8
        self.colorbar_formatting_string = colorbar_formatting_string
        
        self.temporal_aggregators = temporal_aggregators
       
        if not hasattr(self, 'gdf_TIME_Aggregated_1'):
            self.gdf_TIME_Aggregated_1 = self.gdf.dissolve(by=self.temporal_aggregation_attribute_name,
                                                          aggfunc=temporal_aggregators[0])  
            
        if not hasattr(self, 'gdf_TIME_Aggregated_2'):
            self.gdf_TIME_Aggregated_2 = self.gdf.dissolve(by=self.temporal_aggregation_attribute_name,
                                                         aggfunc=temporal_aggregators[1])
        
        self.fig, self.gridline, self.cbars = self._make_plot()
        
        

    def __call__(self, gdf, vmin, vmax, column, 
                 temporal_aggregators=['mean', 'sum'],
                 colorbar_formatting_string='%.2f'):
        
        self.__init__(gdf, vmin, vmax, column, gdf_TIME_Aggregated_1=self.gdf_TIME_Aggregated_1,
                      gdf_TIME_Aggregated_2=self.gdf_TIME_Aggregated_2, 
                      colorbar_formatting_string=colorbar_formatting_string,
                      temporal_aggregators=temporal_aggregators)
        
        return self
    
    def _make_plot (self):
        '''
        Function description:
            
            This function plots the spatial-temporal data and returns a fig, a gridline and colorbar instances
        
        '''
          # equidistant
        Projection = ccrs.PlateCarree()

        fig, ax = make_fig()

        ax = ax.ravel()


        Anos = np.unique(self.gdf[self.datetime_column_name].dt.year)

        cbars = []
        
        cmap = matplotlib.cm.get_cmap('viridis')
        
        for enum, ano in enumerate(Anos):

            ax[enum].set_title(str(ano), fontsize= self.title_fontsize)
            add_background(ax[enum])
            gdf_anual = self.gdf[self.gdf[self.datetime_column_name].dt.year==ano]

            gdf_anual.plot(ax=ax[enum], transform=Projection,  vmin=self.vmin, 
                           vmax=self.vmax, facecolor=cmap(0), column=self.column, 
                           cmap='viridis')

            cbars.append(make_cbars(ax[enum], 
                                    vmin=self.vmin, 
                                    vmax=self.vmax, 
                                    colorbar_ax_yticks_format=self.colorbar_formatting_string))

            gridline = add_gridlines(ax[enum])
            

        print("Definindo o total temporal")   

        ax[-2].set_title(r'Temporal {0}'.format(self.temporal_aggregators[0]),
                                                fontsize= self.title_fontsize)

        self.gdf_TIME_Aggregated_1.plot(ax=ax[-2],  
                                        transform=Projection, 
                                        column=self.column, 
                                        cmap='viridis')
        add_background(ax[-2])
        gridline = add_gridlines(ax[-2])


        cbars.append(make_cbars(ax[-2], vmin=self.gdf_TIME_Aggregated_1[self.column].min(), 
                   vmax=self.gdf_TIME_Aggregated_1[self.column].max(),
                    colorbar_ax_yticks_format=self.colorbar_formatting_string))


        ax[-1].set_title(r'Temporal {0}'.format(self.temporal_aggregators[1]), 
                         fontsize=self.title_fontsize)

        add_background(ax[-1])
        gridline = add_gridlines(ax[-1])


        self.gdf_TIME_Aggregated_2.plot(ax=ax[-1], transform=Projection, 
                                      column=self.column, cmap='viridis')

        cbars.append(make_cbars(ax[-1], 
                   vmin=self.gdf_TIME_Aggregated_2[self.column].min(), 
                   vmax=self.gdf_TIME_Aggregated_2[self.column].max()))

        North_arrow_plus_scale_bar_standard_adder.add_standard_north_arrow_with_scale_bar(ax[0], 
                                                                                          distance=300, 
                                                                                          units='km')
        fig.subplots_adjust(top=0.913,
                            bottom=0.08,
                            left=0.055,
                            right=0.898,
                            hspace=0.352,
                            wspace=0.025)

        fig.show()

        return fig, gridline, cbars
    