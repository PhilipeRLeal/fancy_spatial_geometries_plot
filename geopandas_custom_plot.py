# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:53:33 2019

@author: lealp
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.patches as mpatches
import pandas as pd
pd.set_option("display.max_rows",10000)
pd.set_option('display.max_columns', 500)
import matplotlib


try:
    from .gridline_tick_formatters import LongitudeFormatter, LatitudeFormatter
    
except:
    from gridline_tick_formatters import LongitudeFormatter, LatitudeFormatter

class geopandas_custom_plot(object):
    """
    This is a class that contains several staticmethods for fancy plotting using cartopy.
    
    There is no instance or class method in it.
    
    Use it freely.
    
    """
   
        
    @ staticmethod
    
    
    def change_gridliner_tick_decimal_separator(Gridliner, gridline_tick_formating='.2f', axis='y'):  
        
        def get_t(text):
        
            new_t = "{0:{1}}".format(text,gridline_tick_formating).replace('.',',')
            
            return new_t 
        
        def transform_axis_ticks(axis_get_Ticks, axis_set_ticks):
        
            
            XTexts = [get_t(t) for t in axis_get_Ticks()]      
            
            axis_set_ticks(XTexts)
        
        if axis.lower()=='y':
            
            Yaxis_get_Ticks = getattr(Gridliner.axes, 'get_yticks')
            Yaxis_set_Ticks = getattr(Gridliner.axes, 'set_yticklabels')
            
            transform_axis_ticks(Yaxis_get_Ticks, Yaxis_set_Ticks)    
            
            
        elif axis.lower()=='x':    
            Xaxis_get_Ticks = getattr(Gridliner.axes, 'get_xticks')
            Xaxis_set_Ticks = getattr(Gridliner.axes, 'set_xticklabels')
            
            
            transform_axis_ticks(Xaxis_get_Ticks, Xaxis_set_Ticks)    
        

        else: # or axis.lower()=='both':
            
            transform_axis_ticks(Yaxis_get_Ticks, Yaxis_set_Ticks) 
            transform_axis_ticks(Xaxis_get_Ticks, Xaxis_set_Ticks)  
        
        
        return Gridliner

    
    
    
    @ staticmethod
    def add_colorbar_for_axes(geo_axes, gdf, 
                              column=None,
                              n_ticks_in_colorbar=4, 
                              shrink=0.95, pad=0.02,
                              round_float_value_colorbar_tickslabels=2, 
                              cmap='viridis',
                              alpha=1,
							  n_colors_in_cmap=None,
							  colorbar_tick_fontsize=7, decimal_separator=','):


        '''
		Parameters:
		
		
            geo_axes: the geo_axes into which space will be drawn for fixing the colorbar
			
			----------------------------------------------------------------------------------------------
            
			column: the dataframe (or geodataframe) column from which the colors will be derived for the colorbar
			
			----------------------------------------------------------------------------------------------
            
			n_ticks_in_colorbar: sets the number of ticks to be plotted in the colorbar
			
			----------------------------------------------------------------------------------------------
            
			round_float_value_colorbar_tickslabels: the resolution after the decimal separator to be applied
			
			----------------------------------------------------------------------------------------------
            
			cmap: the cmap name to be used in the colorbar. The function also accepts a matplotlib.colors.ListedColormap instance, instead of a cmap name.
			
			----------------------------------------------------------------------------------------------
            
			n_colors_in_cmap: number of colors (discrete intervals) to be used in the colorbar. Only applicable for cmap str instance 
			
				i.e.: cmap='viridis'
						n_colors_in_cmap = 4
						
			
			----------------------------------------------------------------------------------------------
            
			colorbar_tick_fontsize: the fontsize of the ticklabels of the colorbar
			
			----------------------------------------------------------------------------------------------
            
			
			
		Returns:
			colorbar instance
			
		
        '''
		
        if isinstance(cmap, str):
        
            cmap = plt.cm.get_cmap(cmap , n_colors_in_cmap)     

        elif isinstance(cmap, matplotlib.colors.ListedColormap):
            cmap = cmap
        
        else:
            cmap = getattr(mpl.cm, cmap)
        
        
        Vmin = gdf[column].min()
        Vmax = gdf[column].max()
        
        Ticks_list, step = np.linspace(Vmin, Vmax, num=n_ticks_in_colorbar, endpoint=True, retstep=True)
        Ticks_list = np.round(Ticks_list,round_float_value_colorbar_tickslabels)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=Vmin,vmax=Vmax))
    
        sm._A = []
        
        fig=geo_axes.get_figure()
        
         
        cbar = fig.colorbar(sm, ax=geo_axes, ticks=Ticks_list, shrink=shrink, pad=pad)   
        
        Ticks_list = [str(tick).replace('.', decimal_separator) for tick in Ticks_list]
        
        cbar.set_ticklabels(Ticks_list)
		
        cbar.ax.tick_params(labelsize=colorbar_tick_fontsize)
			

        return cbar
    
    
    
    #####################################################################
    
    
    @ staticmethod
    
    def fancy_plotting(gdf, 
                       
                       geo_axes, 
                       geo_axes_projection=ccrs.PlateCarree(central_longitude=0),
                 
                       gdf_plot_kw={'categorical':True,
                              'column':None,
                              'legend':None,
                              'facecolor':'white',
                              'alpha':0.5,
                              'linewidth':1,
                              
                              'legend_kwds':{'fontsize':12, 
                                             'loc':(1.05, 0.5),
                                             'bbox_to_anchor':(0.5, 0., 0.5, 0.5),
                                             'bbox_transform':None,
                                             'ncol':2,
                                             'frameon':True,
                                             'framealpha':0.5,
                                             'fancybox':True,
                                             'facecolor':'k',
                                             'edgecolor':'k',
                                             'title':'HAV',
                                             'title_fontsize':12,
                                             'borderpad':12,
                                             'borderaxespad':10
                                             },
                                             
                              'edgecolor':'k'},
                              
                         add_colorbar=False,
                         cmap='viridis',
                         n_colors_in_cmap=5, 
                         
                         
                                              
                         
                         
                         
                         
                         n_coordinate_ticks={'x_number':6,  'y_number':6},
                         
                         gridline_xlabel_style = {'color': 'black', 
                               #'weight': 'bold', 
                               'rotation':90,
                               'fontsize':12},
                         
                         gridline_ylabel_style = {'color': 'black', 
                               #'weight': 'bold', 
                               'rotation':0,
                               'fontsize':18},       
                                        
                         gridline_attr=dict(linewidth=1, 
                                            color='black', 
                                            alpha=0.35, 
                                            linestyle='--', 
                                            draw_labels=True),
                 
                         gridline_tick_formating=dict(latitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                                      'degree_symbol':'°', # u'\u00B0'
                                                                      'north_hemisphere_str': 'N',
                                                                      'south_hemisphere_str': 'S'} ,
                                                               
        
                                                      longitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                                       'degree_symbol':'°', # u'\u00B0'
                                                                       'dateline_direction_label':True, # ONLY APPLICABLE TO LONGITUDE DATA
                                                                       'west_hemisphere_str': 'O',
                                                                       'east_hemisphere_str': 'L'})          ):
        
        
        '''
           This is the fancy plotting function.
            
           It receives several parameters so to properly generate a given fancy cartopy plot.
		   
		   Returns: (dict)
		   
				{'axes':geo_axes, 'gridliner':gl}
           
           Paramters:
               
               
               ----------------------------------------------------------------------------------------------
                
               gdf: (geopandas geodataframe)
               
               ----------------------------------------------------------------------------------------------
                
               geo_axes: the geoaxes that will be used to fancy plot,
               
               ----------------------------------------------------------------------------------------------
                
               geo_axes_projection: the projection of the geo_axes
               
               
               ----------------------------------------------------------------------------------------------
                
               
               gdf_plot_kw = dictionary containing all parameters required for plotting the GDF in geo_axes.
                             It is a wrapper of the geopandas plot parameters
               
                   i.e.:
               
               
                       gdf_plot_kw={'categorical':True,
                                      'column':None,
                                      'legend':None,
                                      'facecolor':'white',
                                      'alpha':0.5,
                                      'linewidth':1,
                                      
                                      'legend_kwds':{'fontsize':12, 
                                                     'loc':(1.05, 0.5),
                                                     'bbox_to_anchor':(0.5, 0., 0.5, 0.5),
                                                     'bbox_transform':None,
                                                     'ncol':2,
                                                     'frameon':True,
                                                     'framealpha':0.5,
                                                     'fancybox':True,
                                                     'facecolor':'k',
                                                     'edgecolor':'k',
                                                     'title':'legend title',
                                                     'title_fontsize':12,
                                                     'borderpad':12,
                                                     'borderaxespad':10
                                                     },
                                                     
                                      'edgecolor':'k'},
               
                
                ----------------------------------------------------------------------------------------------
                
                
                add_colorbar: (boolean)  - standard is False
                
                
                ----------------------------------------------------------------------------------------------
                
                
                cmap= (str or matplotlib.colors.ListedColormap):
                    
                
                ----------------------------------------------------------------------------------------------
                
                n_colors_in_cmap=5. Applicable only with cmap as (str), 
                 
                
                ----------------------------------------------------------------------------------------------
                
                 
                n_coordinate_ticks= {'x_number': (int),  'y_number': (int)}:
                    
                    sets the number of ticks in geo_axes
                    
                    
                ----------------------------------------------------------------------------------------------
                
                gridline_xlabel_style = dictionary containing text parameters for styling the xlabels in geo_axes
                                
                    i.e.:
                        
                        gridline_xlabel_style = {'color': 'black', 
                                               #'weight': 'bold', 
                                               'rotation':0,
                                               'fontsize':18},        
                
                ----------------------------------------------------------------------------------------------
                
                
                
                gridline_ylabel_style = dictionary containing text parameters for styling the ylabels in geo_axes
                
                    i.e.:
                        
                        gridline_ylabel_style = {'color': 'black', 
                                               #'weight': 'bold', 
                                               'rotation':0,
                                               'fontsize':18},           
            
            
                
                ----------------------------------------------------------------------------------------------
                
                
                gridline_attr: (dictionary). Dictionary containing text parameters for the gridline styling, 
                    
                    i.e:
                                             
                    gridline_attr=dict(linewidth=1,                 # sets the width of the lines in the gridlines
                                                color='black',      # sets the color of the lines in the gridlines
                                                alpha=0.35,         # sets the alpha of the lines in the gridlines
                                                linestyle='--',     # sets the linestyle of the lines in the gridlines
                                                draw_labels=True),  # sets True for label drawing in the ticks of each gridline or not 
                     
                
                
                
                ----------------------------------------------------------------------------------------------
                
                gridline_tick_formating: (dictionary). Dictionary containing parameters for the tick formating of each of the axis in a geo_axes
                
                    i.e.:
                
                        gridline_tick_formating=dict( latitude_tick_formating={'number_format':'.2f', # two decimal coordinate approximation
                                                                                  'degree_symbol':'°', # u'\u00B0'
                                                                                  
                                                                                  'north_hemisphere_str': 'N',
                                                                                  'south_hemisphere_str': 'S'} ,
                                                                           
                    
                                                      longitude_tick_formating={'number_format':'.2f', # two decimal coordinate approximation
                                                                                   'degree_symbol':'°', # u'\u00B0'
                                                                                   'dateline_direction_label':True,
                                                                                   'west_hemisphere_str': 'O',
                                                                                   'east_hemisphere_str': 'L'})  
                
        '''
        
        
        
        # reprojetando dados para o CRS do mapa
        gdf = gdf.to_crs(geo_axes_projection.proj4_init)
        
        xmin, ymin, xmax, ymax = gdf.total_bounds
		
        geo_axes.set_extent((xmin, xmax, ymin, ymax), crs=geo_axes_projection)
        # pegando o sistema de cores desejado:
        
        
        if isinstance(cmap, str):
        
            cmapper = plt.cm.get_cmap(cmap,n_colors_in_cmap)     
        
        
        
        
        elif isinstance(cmap, matplotlib.colors.ListedColormap):
            cmapper = cmap
        
        
        else:
            
             cmapper = None
        
        
        # transform: always plot gdf in the projection of the map (better safe to be sorry!)
        
        
        gdf.plot(ax=geo_axes, 
                 cmap=cmapper,
                 
                 **gdf_plot_kw) 
        
       
        # getting extent
        
        geo_extent = geo_axes.get_extent() # x0, x1, y0, y1
        

        geo_axes.set_extent(geo_extent, crs=geo_axes_projection) # axes projection here too
        
        geo_axes.set_aspect('equal')
        
        
        fig = geo_axes.get_figure()
        
        if add_colorbar==True:
            
            artist = plt.gca().get_children()[0]
            
            cax = fig.add_axes([0.90,0.24,0.03,0.524]) 
            
            print("\n\n")
            fig.colorbar(mappable=artist, cax=cax)
            
            print("Colorbar is set")
        
        
        X = np.linspace(geo_extent[0], geo_extent[1], n_coordinate_ticks['x_number'], endpoint=True)
        
        geo_axes.set_xticks(X, crs=ccrs.PlateCarree())
        #gl.xlocator = mticker.FixedLocator(X)
        
        
        Y = np.linspace(geo_extent[2], geo_extent[3], n_coordinate_ticks['y_number'], endpoint=True)
        
        geo_axes.set_yticks(Y, crs=ccrs.PlateCarree())
        
        
        gl = geo_axes.gridlines(crs=geo_axes_projection, xlocs=X, 
								ylocs=Y, **gridline_attr) # axes projection here too
        
		
        ## Better set to no standard labeling so to avoid possible overlay of custom and standard labels in geo_axes
        
        
        tick_axis_positions={'xlabels_top':False,
                             'ylabels_left':False,
                             'ylabels_right':False,
                             'xlabels_bottom':False}
        
        

        gl.xlabels_top = tick_axis_positions['xlabels_top']
        gl.ylabels_left = tick_axis_positions['ylabels_left']
        gl.ylabels_right= tick_axis_positions['ylabels_right']
        gl.xlabels_bottom = tick_axis_positions['xlabels_bottom']
        
        
        #gl.ylocator = mticker.FixedLocator(Y)
        # Formater do gridline
        
        
        
        
        longitude_tick_formating = gridline_tick_formating['longitude_tick_formating']
        
 
        
        number_format = longitude_tick_formating.get('number_format', '.2f')
        west_hemisphere_str = longitude_tick_formating.get('west_hemisphere_str', 'O')  
        east_hemisphere_str = longitude_tick_formating.get('east_hemisphere_str', 'L')  
        degree_symbol = longitude_tick_formating.get('degree_symbol', '')
        dateline_direction_label = longitude_tick_formating.get('dateline_direction_label', False)
        
        
        lon_formatter = LongitudeFormatter(number_format=number_format,
                                           degree_symbol=degree_symbol,
                                           west_hemisphere_str=west_hemisphere_str,
                                           east_hemisphere_str=east_hemisphere_str,
                                           dateline_direction_label=dateline_direction_label)

        
        latitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                 'degree_symbol':'°',
                                 'north_hemisphere_str':'N'}
        
        latitude_tick_formating = gridline_tick_formating['latitude_tick_formating']
        
        number_format = latitude_tick_formating.get('number_format', '.2f')

        north_hemisphere_str = latitude_tick_formating.get('north_hemisphere_str', 'N')  
        south_hemisphere_str = latitude_tick_formating.get('south_hemisphere_str', 'S')  
        degree_symbol = latitude_tick_formating.get('degree_symbol', '')
        
        
        lat_formatter = LatitudeFormatter(number_format=number_format,
                                          degree_symbol=degree_symbol,
                                          north_hemisphere_str=north_hemisphere_str,
                                          south_hemisphere_str=south_hemisphere_str)
    
        geo_axes.xaxis.set_major_formatter(lon_formatter)
        geo_axes.yaxis.set_major_formatter(lat_formatter)
        
       
        gl.xlabel_style = gridline_xlabel_style
        gl.ylabel_style = gridline_ylabel_style
        
        
        
        
        geopandas_custom_plot._set_ticks(ax=geo_axes, 
                                        axis='x', 
                                        which='major', 
                                        labelpad=10, 
                                        labelrotation=90, 
                                        ticksize=2, 
                                        labelsize=8,
                                        labelcolor='k',
                                        tick_color='k',)
        
        
        geopandas_custom_plot._set_ticks(ax=geo_axes, axis='y', 
                                        which='major', 
                                        labelpad=10, 
                                        labelrotation=0, 
                                        ticksize=2, 
                                        labelsize=8,
                                        labelcolor='k',
                                        tick_color='k',)
        
        
        
        geopandas_custom_plot.change_gridliner_tick_decimal_separator(gl, gridline_tick_formating['latitude_tick_formating']['number_format'], axis='y')
        
        geopandas_custom_plot.change_gridliner_tick_decimal_separator(gl, gridline_tick_formating['longitude_tick_formating']['number_format'], axis='x')
        

        return {'axes':geo_axes, 'gridliner':gl}
    
    @ staticmethod
    
    def add_custom_gridline(geo_axes, 
                            
                            gridline_attr=dict(linewidth=1, 
                                            color='black', 
                                            alpha=0.35, 
                                            linestyle='--', 
                                            draw_labels=True),
                                               
                            n_coordinate_ticks={'x_number':3,  'y_number':3},
                            
                            gridline_tick_formating=dict(latitude_tick_formating={'number_format':'.1f', # com duas casas decimais
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
                                                       'fontsize':12},
                         
                            gridline_ylabel_style = {'color': 'black', 
                                                   #'weight': 'bold', 
                                                   'rotation':0,
                                                   'fontsize':18},       
                            
                            ):
        
        
        geo_extent = geo_axes.get_extent()
        
        X = np.linspace(geo_extent[0], geo_extent[1], n_coordinate_ticks['x_number'], endpoint=True)
        
        geo_axes.set_xticks(X, crs=ccrs.PlateCarree())
        #gl.xlocator = mticker.FixedLocator(X)
        
        
        Y = np.linspace(geo_extent[2], geo_extent[3], n_coordinate_ticks['y_number'], endpoint=True)
        
        geo_axes.set_yticks(Y, crs=ccrs.PlateCarree())
        
        
        gl = geo_axes.gridlines(crs=geo_axes.projection, xlocs=X, 
								ylocs=Y, **gridline_attr) # axes projection here too
        
		
        ## Better set to no standard labeling so to avoid possible overlay of custom and standard labels in geo_axes
        
        
        tick_axis_positions={'xlabels_top':False,
                             'ylabels_left':False,
                             'ylabels_right':False,
                             'xlabels_bottom':False}
        
        

        gl.xlabels_top = tick_axis_positions['xlabels_top']
        gl.ylabels_left = tick_axis_positions['ylabels_left']
        gl.ylabels_right= tick_axis_positions['ylabels_right']
        gl.xlabels_bottom = tick_axis_positions['xlabels_bottom']
        
        
        #gl.ylocator = mticker.FixedLocator(Y)
        # Formater do gridline
        
        
        
        
        longitude_tick_formating = gridline_tick_formating['longitude_tick_formating']
        
 
        
        number_format = longitude_tick_formating.get('number_format', '.2f')
        west_hemisphere_str = longitude_tick_formating.get('west_hemisphere_str', 'O')  
        east_hemisphere_str = longitude_tick_formating.get('east_hemisphere_str', 'L')  
        degree_symbol = longitude_tick_formating.get('degree_symbol', '')
        dateline_direction_label = longitude_tick_formating.get('dateline_direction_label', False)
        
        
        lon_formatter = LongitudeFormatter(number_format=number_format,
                                           degree_symbol=degree_symbol,
                                           west_hemisphere_str=west_hemisphere_str,
                                           east_hemisphere_str=east_hemisphere_str,
                                           dateline_direction_label=dateline_direction_label)

        
        latitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                 'degree_symbol':'°',
                                 'north_hemisphere_str':'N'}
        
        latitude_tick_formating = gridline_tick_formating['latitude_tick_formating']
        
        number_format = latitude_tick_formating.get('number_format', '.2f')

        north_hemisphere_str = latitude_tick_formating.get('north_hemisphere_str', 'N')  
        south_hemisphere_str = latitude_tick_formating.get('south_hemisphere_str', 'S')  
        degree_symbol = latitude_tick_formating.get('degree_symbol', '')
        
        
        lat_formatter = LatitudeFormatter(number_format=number_format,
                                          degree_symbol=degree_symbol,
                                          north_hemisphere_str=north_hemisphere_str,
                                          south_hemisphere_str=south_hemisphere_str)
    
        geo_axes.xaxis.set_major_formatter(lon_formatter)
        geo_axes.yaxis.set_major_formatter(lat_formatter)
        
       
        gl.xlabel_style = gridline_xlabel_style
        gl.ylabel_style = gridline_ylabel_style
        
        
        
        
        geopandas_custom_plot._set_ticks(ax=geo_axes, 
                                        axis='x', 
                                        which='major', 
                                        labelpad=5, 
                                        labelrotation=90, 
                                        ticksize=2, 
                                        labelsize=6,
                                        labelcolor='k',
                                        tick_color='k',)
        
        
        geopandas_custom_plot._set_ticks(ax=geo_axes, axis='y', 
                                        which='major', 
                                        labelpad=5, 
                                        labelrotation=0, 
                                        ticksize=2, 
                                        labelsize=6,
                                        labelcolor='k',
                                        tick_color='k',)
        
        
        return geo_axes, gl
    
    #####################################################################
    
    
    @ staticmethod
    def _set_ticks(ax, 
                  axis='both', 
                  which='major', 
                  labelpad=10, 
                  labelrotation=90, 
                  labelsize=12,
                  labelcolor='k',
                  ticksize=10,
                  length=1.0,
                  width=0.2,
                  tick_color='k',
                  bottom=True,
                  left=True,
                  right=False,
                  top=False,
                  direction='out',
                  grid_color='k',
                  grid_alpha=0.5,
                  grid_linewidth=0.2,
                  grid_linestyle='-'
                  ):
        
        
        '''
        
        standard matplotlib function for setting ticks in given Axes.
        
        Parameters:
        
            
            axis: ['x', 'y', 'both']
            which: ['major', 'minor', 'both'] - defines the tick that the function will be applied
            labelpad: pad of the label
            labelrotation: for standard it is 90
            labelsize: size of the labels
            ticksize: the size of the ticks
            
            ticksize: the size of the tick lines
            bottom, top, right, left: allows or denies the tick and ticklabel plotting for that given axis direction
            
            direction : ['in', 'out', 'inout']
                    Puts ticks inside the axes, outside the axes, or both
                    
            length : float
                Tick length in points
                
            width : float
                Tick width in points.
                
        Returns:
            
            axes
            
        '''
        
        ax.tick_params(axis=axis, 
                      which = which, 
                      pad = labelpad, 
                      
                      size = ticksize, 
                      color = tick_color,
                      length=length,
                      width=width,
                      labelrotation = labelrotation, 
                      labelsize = labelsize,
                      labelcolor = labelcolor,
                      
                      bottom = bottom,
                      left = left,
                      right = right,
                      top = top,
                      direction = direction,
                      grid_color = grid_color,
                      grid_alpha = grid_alpha,
                      grid_linewidth = grid_linewidth,
                      grid_linestyle = grid_linestyle)
        
        return ax
    
    
    
    #####################################################################
    
    
    @ staticmethod
    def set_axis_number_of_ticks(ax, axis='both', which='major', n_ticks=5):
        
        '''
        
        Internal function that sets the number of ticks in an axes (or geoaxes):
            
        Parameters:
            
            axis=['x', 'y', 'both']
                Standard is both
                
            which=['major', 'minor', 'both'] - Which ticks should be processed
            
            n_ticks= int (standard is 5): the number of ticks in the axis
        
        
        axis: ['x', 'y', 'both']
        
        '''
        
        if which=='major':
        
            if axis=='x':
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_major_locator(MaxNLocator(n_ticks))
            
            elif axis=='y':
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_major_locator(MaxNLocator(n_ticks))
                
            else:
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_major_locator(MaxNLocator(n_ticks))
                
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_major_locator(MaxNLocator(n_ticks))
            
        elif which=='minor':
        
            if axis=='x':
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_minor_locator(MaxNLocator(n_ticks))
            
            elif axis=='y':
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_minor_locator(MaxNLocator(n_ticks))
                
            else:
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_minor_locator(MaxNLocator(n_ticks))
                
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_minor_locator(MaxNLocator(n_ticks))
                
        else:
            
            if axis=='x':
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_major_locator(MaxNLocator(n_ticks))
            
            elif axis=='y':
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_major_locator(MaxNLocator(n_ticks))
                
            else:
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_major_locator(MaxNLocator(n_ticks))
                
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_major_locator(MaxNLocator(n_ticks))
            
            
            if axis=='x':
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_minor_locator(MaxNLocator(n_ticks))
            
            elif axis=='y':
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_minor_locator(MaxNLocator(n_ticks))
                
            else:
                yaxis = getattr(ax, 'yaxis')
                yaxis.set_minor_locator(MaxNLocator(n_ticks))
                
                xaxis = getattr(ax, 'xaxis')
                xaxis.set_minor_locator(MaxNLocator(n_ticks))
                
        return ax

    @ staticmethod
    def add_north_Arrow(geo_axes, 
                        x_tail = 0.892,
                        y_tail = 0.08,
                        x_head = 0.892,
                        y_head = 0.12,
                        width=0.05,
                        transform=None):
        
        """Function that adds north arrow plus a text over the arrows head
        
        parameters: 
            
            geo_axes a cartopy geoaxes instance
            
            x_tail = (float) 0.975   - the xbase of the arrow 
            y_tail = (float) 0.01    - the ybase of the arrow
            x_head = (float) 0.975   - the xtop of the arrow
            y_head = (float) 0.030,  - the ytop of the arrow
            width=0.05: the width of the arrows head
            transform: the transform that wil be used to set the position of the arrow in the figure/axes
            (standard): None == fig.transFigure
        

		Returns:
		
			geo_axes
            
        """
        
        
        
        dx = x_head - x_tail
        dy = y_head - y_tail


        fig = geo_axes.get_figure()
        
        if transform==None:
            transform=fig.transFigure
        
        arrow = mpatches.Arrow(x_tail, y_tail, dx, dy, width=width, transform=transform, color='k', figure=fig)

        fig.patches.extend([arrow])
    
        plt.text(x_head, 
				 y_head + 0.8*(y_head - y_tail) , 
				s='N', 
				size=11, 
				ha='center', 
				va='center',
				color='K', 
				transform=transform, 
				figure=fig)
    
        
        return geo_axes
    
    
    @ staticmethod
    def add_scale_bar(geo_axes, length=200, unit='km', location=(1.22, 0.001), linewidth=2.5):
        """
        Function that adds scale bar to an geoaxes
        
        length: float. For standard(km). 
            unit parameter sets the unit in the legth
        
        unit= (str or float) ['km', 'm', float]:
            
            if str:
                direction convertion to units in map
                
            if float:
                float value must be a relation to 1 kilometer.
                
            unit parameter sets the parameter legth value. 
        
        
        """
        
        
        
        #Get the limits of the axis in lat long
        llx0, llx1, lly0, lly1 = geo_axes.get_extent(ccrs.PlateCarree())
		#Make tmc horizontally centred on the middle of the map,
		#vertically at scale bar location
        sbllx = (llx1 + llx0) / 2
        sblly = lly0 + (lly1 - lly0) * location[1]
        
        
        tmc = ccrs.TransverseMercator(central_longitude=sbllx, 
                                      central_latitude=sblly)
        
        
		#Get the extent of the plotted area in coordinates in metres
        x0, x1, y0, y1 = geo_axes.get_extent(tmc)
		#Turn the specified scalebar location into coordinates in metres
        sbx = x0 + (x1 - x0) * location[0]
        sby = y0 + (y1 - y0) * location[1]

		#Calculate a scale bar length if none has been given
		#(Theres probably a more pythonic way of rounding the number but this works)
        if not length: 
            
            if unit == 'km':
            
                length = (x1 - x0) / 5000 #in km
            
            elif unit == 'm':
                length = (x1 - x0) / 5 # in meters
                
            elif unit =='miles':
                
                length = (x1 - x0) / (5000/1.60934)  #in miles
                
            else:
                
                length = (x1 - x0) / (5000/float(unit)) # assuming that the given value is a relation to kms.
                
            ndim = int(np.floor(np.log10(length))) #number of digits in number
            length = round(length, -ndim) #round to 1sf
			#Returns numbers starting with the list
            def scale_number(x):
                if str(x)[0] in ['1', '2', '5']: return int(x)		
                else: return scale_number(x - 10 ** ndim)
            
            length = scale_number(length) 

		#Generate the x coordinate for the ends of the scalebar
        bar_xs = [sbx - length * 500, sbx + length * 500]
		
		#Plot the scalebar
        geo_axes.plot(bar_xs, [sby, sby], 
				transform=tmc, 
				color='k',
				clip_on=False, 
				linewidth=linewidth,
				zorder=100)
		

		#Plot the scalebar label
        unit_text = ''
        
        if isinstance(unit, str):
            unit_text = unit
        

        
        Text = geo_axes.text(sbx, sby, str(length) + ' ' + unit_text, 
                      bbox=dict(facecolor='white', alpha=0.5, edgecolor='white'),
    				  clip_on=False,  
    				  transform=tmc,
    				  horizontalalignment='center', 
    				  verticalalignment='bottom',
    				  zorder=100)
        
        
        geo_axes.set_extent([llx0, llx1, lly0, lly1], crs=ccrs.PlateCarree())
    
        return [geo_axes, Text]
    #####################################################################
    


if '__main__' ==__name__:
        
    
    
    SHP_path = r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp'
    
    SHP = gpd.read_file(SHP_path)
    
    SHP['CD_GEOCMU'] = SHP['CD_GEOCMU'].apply(int)
    
    
    projection = ccrs.PlateCarree() # projection.proj4_init
    
    Transform = ccrs.Geodetic(globe=ccrs.Globe(ellipse='GRS80'))
    
    fig, ax = plt.subplots(1, subplot_kw={'projection':projection})
    
    
    
    
    
    Result = geopandas_custom_plot.fancy_plotting(geo_axes=ax, 
                 gdf=SHP,
                 add_colorbar=False,
                 cmap='viridis',
                 n_colors_in_cmap=144, 
                 geo_axes_projection=projection,
                 gdf_plot_kw={'categorical':True,
                              'column':'NM_MUNICIP',
                              'legend':False,
                              'facecolor':'white',
                              'alpha':0.5,
                              'linewidth':1,
                              'legend_kwds':{'fontsize':2.5},
                              'edgecolor':'k'},
                              
                              
                 gridline_tick_formating=dict(latitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                                       'degree_symbol':'°'} ,
                                                               
        
                                             longitude_tick_formating={'number_format':'.2f', # com duas casas decimais
                                                                       'degree_symbol':'°',
                                                                       'dateline_direction_label':False,
                                                                       'west_hemisphere_str': 'O',
                                                                       'east_hemisphere_str': 'L'}),
                                                                       
                gridline_xlabel_style = {'color': 'black', 
                       #'weight': 'bold', 
                       'rotation':90,
                       'fontsize':10},
                 
                 gridline_ylabel_style = {'color': 'black', 
                       #'weight': 'bold', 
                       'rotation':0,
                       'fontsize':10},     
                n_coordinate_ticks={'x_number':9,  'y_number':5},
                )
                 
                 
    ax, Text = geopandas_custom_plot.add_scale_bar(geo_axes=ax)
    
    ax = geopandas_custom_plot.add_north_Arrow(geo_axes=ax, transform=fig.transFigure)
    geopandas_custom_plot.add_colorbar_for_axes(ax, SHP, column='CD_GEOCMU', n_ticks_in_colorbar=10)
    
    
    fig.subplots_adjust(top=0.88,
                        bottom=0.18,
                        left=0.11,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)
                            
    fig.show()
    