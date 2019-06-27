# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:42:09 2019

@author: lealp
"""

import pandas as pd
pd.set_option('display.width', 50000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

import matplotlib.pyplot as plt


import matplotlib as mpl
        
from matplotlib import ticker


class custom_colorbars():    
    
     @ staticmethod
     def add_colorbar_for_axes(axes, vmax, 
                              vmin,
                              n_ticks_in_colorbar=4, 
                              shrink=0.95, pad=0.02,
                              cmap='viridis',
                              matplotlib_colors_normalize=None,
							  n_colors_in_cmap=None,
							  colorbar_tick_fontsize=7,
                              colorbar_ax_yticks_format='%.2f',
                              **fbar_kwds):


         '''
		 Parameters:
		
		
             axes: the axes into which space will be drawn for fixing the colorbar
			
			
	      	----------------------------------------------------------------------------------------------
            
	 		 n_ticks_in_colorbar: sets the number of ticks to be plotted in the colorbar
			
	 		----------------------------------------------------------------------------------------------
            
	 		cmap: the cmap name to be used in the colorbar. The function also accepts a matplotlib.colors.ListedColormap instance, instead of a cmap name.
			
			----------------------------------------------------------------------------------------------

             matplotlib_colors_normalize: A matplotlib.colors.Normalize instace. The normalizing object which scales data, typically into the
                 interval ``[0, 1]``.
                                         
                 If *None*, *norm* defaults to a *colors.Normalize* object which
                 initializes its scaling based on the first data processed.
                
                
             ----------------------------------------------------------------------------------------------
            
            
	 		n_colors_in_cmap: number of colors (discrete intervals) to be used in the colorbar. Only applicable for cmap str instance 
			
	 			i.e.: cmap='viridis'
	 					n_colors_in_cmap = 4
						
			
	 		----------------------------------------------------------------------------------------------
            
	 		colorbar_tick_fontsize: the fontsize of the ticklabels of the colorbar
			
	 		----------------------------------------------------------------------------------------------
            
            
             colorbar_ax_yticks_format (string or a matplotlib.ticker.Formatter): 
                 standard = {0:.2f} a float number with 2 decimal cases
                
                 Alternative options (with comma as decimal separator):
                    
                    
                    
                     colorbar with scientific formatting:
                        
                         """
                        
                        
                         from matplotlib import ticker
                        
                         def wrapped_func (x, y, decimal_separator=','):
                            
                             return geopandas_custom_plot._y_fmt(x, y, decimal_separator=decimal_separator)
                        
                         formatter = ticker.FuncFormatter( wrapped_func)
                    
                    
                    
                         geopandas_custom_plot.add_colorbar_for_axes(geo_axes, 
                                                                    vmax, 
                                                                    vmin,
                                                                    colorbar_ax_yticks_format=formatter)
                        
                         """
                        
                        
			
			
		 Returns:
		  	colorbar instance
			
		
         '''
		
         
        
         if isinstance(cmap, str):
        
             cmap = plt.cm.get_cmap(cmap , n_colors_in_cmap)     

         elif isinstance(cmap, mpl.colors.ListedColormap):
             cmap = cmap
    
         else:
             cmap = getattr(mpl.cm, cmap)
    
    

        
         if matplotlib_colors_normalize == None:
             matplotlib_colors_normalize = plt.Normalize
        
         sm = plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib_colors_normalize(vmin=vmin,vmax=vmax))
    
         sm._A = []
    
         fig = axes.get_figure()
    
     
         cbar = fig.colorbar(sm, ax=axes, shrink=shrink, pad=pad, 
                            format=colorbar_ax_yticks_format, **fbar_kwds)   
        
         from matplotlib import ticker
        
         def null_ticks(x,y):
             return ''
         
            
         # xaxis   
            
         cbar.ax.xaxis.set_major_formatter(ticker.FuncFormatter(null_ticks))
        
         cbar.ax.xaxis.set_ticks([])
         
         # yaxis
         
         cbar.ax.yaxis.set_major_formatter(ticker.MaxNLocator(n_ticks_in_colorbar))
        
         cbar.ax.tick_params(labelsize=colorbar_tick_fontsize)
    
         
        
         return cbar


    
     @ staticmethod
     def add_colorbar_for_fig (fig, 
                              vmin,
                              vmax, 
                              n_ticks_in_colorbar=4,
                              Bounding_box=[0.8, 0.17, 0.02, 0.65],
                              cmap='viridis',
							  n_colors_in_cmap=None,
                              colorbar_ax_yticks_format='{0:.2f}',
							  colorbar_tick_fontsize=7, 
                              **fig_colorbar_kwds):


         '''
		 Parameters:
		
		
            fig: the fig into which space will be drawn for fixing the colorbar
			
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
            
            
            colorbar_ax_yticks_format (string or a matplotlib.ticker.Formatter): 
                standard = {0:.2f} a float number with 2 decimal cases
                
                Alternative options (with comma as decimal separator):
                    
                    
                    
                    colorbar with scientific formatting:
                        
                        """
                        
                        
                        from matplotlib import ticker
                        
                        def wrapped_func (x, y, decimal_separator=','):
                            
                            return geopandas_custom_plot._y_fmt(x, y, decimal_separator=decimal_separator)
                        
                        formatter = ticker.FuncFormatter( wrapped_func)
                    
                    
                    
                        geopandas_custom_plot.add_colorbar_for_axes(geo_axes, 
                                                                    vmax, 
                                                                    vmin,
                                                                    colorbar_ax_yticks_format=formatter)
                        
                        """
                        
                        
			
		 Returns:
		 	 colorbar instance
			
		
         '''
         
		
         if isinstance(cmap, str):
        
             cmap = plt.cm.get_cmap(cmap , n_colors_in_cmap)     

         elif isinstance(cmap, mpl.colors.ListedColormap):
             cmap = cmap
        
         else:
             cmap = getattr(mpl.cm, cmap)
     
        
         sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin,vmax=vmax))
    
         sm._A = []
        
         fig=fig
        
        
         cax = fig.add_axes(Bounding_box)
        
        
         cbar = fig.colorbar(sm, cax=cax, format=colorbar_ax_yticks_format, **fig_colorbar_kwds)
        
         cbar.ax.yaxis.set_major_formatter(ticker.MaxNLocator(n_ticks_in_colorbar))
        

        
         def null_ticks(x,y):
             return ''
        
         cbar.ax.xaxis.set_major_formatter(ticker.FuncFormatter(null_ticks))
        
        
        
         cbar.ax.xaxis.set_ticks([])
         cbar.ax.tick_params(labelsize=colorbar_tick_fontsize)
         cbar.ax.xaxis.set_ticks([])

         return cbar
    
    
     @ staticmethod
     def format_cbar_ticks_to_scientific_notation(cbar, axis='both', decimal_separator='.'):
         
          ##################################     
          def value_to_scientific(x):
              return '{:2.2e}'.format(x)
        

          def axis_fmt(x, y, decimal_separator=decimal_separator):
        
              v1, v2 = value_to_scientific(x).split('e')
            
              v1 = v1.replace('.', decimal_separator)
         
              return r'${0} \times 10^{{{1}}}$'.format(v1, v2) if x !=0 else '0'
    
    
          ###################################
     
          ax = cbar.ax
         
          if axis.lower() == 'both':
             
              axis = ['xaxis', 'yaxis']
            
              for i_axis in axis:
                  Axis = getattr(ax, i_axis)
                  Axis.set_major_formatter(ticker.FuncFormatter(axis_fmt))
            
          else:
            
              Axis = getattr(ax, axis)
              Axis.set_major_formatter(ticker.FuncFormatter(axis_fmt))
              
          return cbar
      
        
        
        
if "__main__" == __name__:
    import geopandas as gpd
    import cartopy.crs as ccrs
    
    SHP_path = r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp'
    
    SHP = gpd.read_file(SHP_path)
    
    SHP['CD_GEOCMU'] = SHP['CD_GEOCMU'].apply(float)
    
    vmin = SHP['CD_GEOCMU'].min()
    
    vmax = SHP['CD_GEOCMU'].max()
    
    
    projection = ccrs.PlateCarree() # projection.proj4_init

    fig, ax = plt.subplots(1, subplot_kw={'projection':projection})
    
    
    SHP.plot(ax=ax, column='CD_GEOCMU')
    
    cbar = custom_colorbars.add_colorbar_for_fig(fig=fig, vmin=vmin, vmax=vmax)
    
    custom_colorbars.format_cbar_ticks_to_scientific_notation(cbar, decimal_separator=',')
    
    fig.subplots_adjust(top=0.88,
                        bottom=0.18,
                        left=0.11,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)
                            
    fig.show()
    