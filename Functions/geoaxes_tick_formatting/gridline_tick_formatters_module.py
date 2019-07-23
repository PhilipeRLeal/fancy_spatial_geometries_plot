# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:09:27 2019

@author: lealp
"""


from matplotlib import ticker

if '__main__' ==__name__:
    from locators_and_formatters_module import LongitudeFormatter, LatitudeFormatter
else:
    from .locators_and_formatters_module import LongitudeFormatter, LatitudeFormatter

def set_gridline_tick_axis_positions(gridliner , positions = dict(top=False, 
															   bottom=True, 
															   left=True, 
															   right=False)):
	 
	 gridliner.xlabels_top = positions['top']
	 gridliner.xlabels_bottom = positions['bottom']
	 
	 gridliner.ylabels_right = positions['right']
	 gridliner.ylabels_left = positions['left']
	 
	 

def set_number_of_ticks_in_Gridliner(nbins, gridliner):

	
    
    
    gridliner.ylocator = ticker.MaxNLocator(nbins)
    gridliner.xlocator = ticker.MaxNLocator(nbins)
    
    return gridliner

def change_gridline_tick_formating(gridliner, gridline_tick_formating='.2f', axis='yaxis', decimal_separator=',', geographical_symbol='°'):  
	 
	 def Format_p(x, counter):
		
		 return '{0:{1}}{2}'.format(x, gridline_tick_formating, geographical_symbol).replace('.', decimal_separator)
	 
	 if axis.lower() == 'both':
 
		 gridliner.xformatter = ticker.FuncFormatter(Format_p)
		 gridliner.yformatter = ticker.FuncFormatter(Format_p)
			 
	 else:
		 if axis.lower().startswith('x'):
			 gridliner.xformatter = ticker.FuncFormatter(Format_p)
		 else:
			 gridliner.yformatter = ticker.FuncFormatter(Format_p)
	
	
	 return gridliner


    
def add_custom_gridline(geo_axes, 
                    
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
                                               'fontsize':12},
                 
                        gridline_ylabel_style = {'color': 'black', 
                                           #'weight': 'bold', 
                                           'rotation':0,
                                           'fontsize':18},  
							
							
    
                    
						gridline_tick_axis_positions={'xlabels_top':False,
												 'ylabels_left':True,
												 'ylabels_right':False,
												 'xlabels_bottom':True}		,
                                
                        decimal_separator='.',										   
                        geographical_symbol='°'
                        ):

    """
        Function description:
			This inserts custom gridlines into a given axes.
			
			parameters:
				
				draw_labels(bool): whether to draw the labels in the gridline or not
					Default = True
				
				gridline_attr (dict): sets the linewidth, the linecolor, the alpha of the linecolor, linestyle

				n_coordinate_ticks (dict): sets the number of lines in the gridlines x coordinate (longitude) and y coordinate (latitude)
				
					Default = {'x_number':3,  'y_number':3}
		
				gridline_tick_formating (dict): contains parameters for setting the lines of the gridlines. 
				
					latitude_tick_formating: dictionary containing parameters for defining the ticklines of the y axis of the given axes:
						
						'number_format' (string or matplotlib formatter function based): sets the format of the coordinate number in the gridlines ticklabels
						
						'degree_symbol' (string): sets the symbol of the coordinates
							Default = '°'
						
						
						'north_hemisphere_str' (string): the string to be used for the north hemisphere.
							Default = 'N' 
						
						'south_hemisphere_str' (string): the string to be used for the south hemisphere
							Default = 'S' for south hemisphere
					
					
					longitude_tick_formating: the same thing as latitude_tick_formating for longitude data, except that it is relative to the xaxis of the given axes.
					
						
					gridline_xlabel_style (dict): sets xlabel style of the griline of the given axes. It accepts all parameters that ax.gridlines().xlabel_style accepts.
					
					gridline_ylabel_style (dict): sets xlabel style of the griline of the given axes. It accepts all parameters that ax.gridlines().ylabel_style accepts.
					
					gridline_tick_axis_positions: allows further customization of the ticklabels. It sets which axis the labels should be drawn in a given axes.

    """
 
    
    gl = geo_axes.gridlines(crs=geo_axes.projection, **gridline_attr) # axes projection here too
    
    		
    ## Better set to no standard labeling so to avoid possible overlay of custom and standard labels in geo_axes
    
    
       
    gl.xlabels_top = gridline_tick_axis_positions['xlabels_top']
    gl.ylabels_left = gridline_tick_axis_positions['ylabels_left']
    gl.ylabels_right= gridline_tick_axis_positions['ylabels_right']
    gl.xlabels_bottom = gridline_tick_axis_positions['xlabels_bottom']
    
    from matplotlib import ticker
    
    
    gl.ylocator = ticker.MaxNLocator(nbins=n_coordinate_ticks['y_number'])
    gl.xlocator = ticker.MaxNLocator(nbins=n_coordinate_ticks['x_number'])
    
    
    # Formater do gridline
    
    
    
    longitude_tick_formating = gridline_tick_formating['longitude_tick_formating']
    
    		
    
    number_format = longitude_tick_formating.get('number_format', '.2f')
    west_hemisphere_str = longitude_tick_formating.get('west_hemisphere_str', 'W')  
    east_hemisphere_str = longitude_tick_formating.get('east_hemisphere_str', 'E')  
    degree_symbol = longitude_tick_formating.get('degree_symbol', '')
    dateline_direction_label = longitude_tick_formating.get('dateline_direction_label', False)
    
    
    lon_formatter = LongitudeFormatter(number_format=number_format,
                                       degree_symbol=degree_symbol,
                                       west_hemisphere_str=west_hemisphere_str,
                                       east_hemisphere_str=east_hemisphere_str,
                                       dateline_direction_label=dateline_direction_label)
    
    
           
    latitude_tick_formating = gridline_tick_formating['latitude_tick_formating']
    
    number_format = latitude_tick_formating.get('number_format', '.2f')
    
    north_hemisphere_str = latitude_tick_formating.get('north_hemisphere_str', 'N')  
    south_hemisphere_str = latitude_tick_formating.get('south_hemisphere_str', 'S')  
    degree_symbol = latitude_tick_formating.get('degree_symbol', '')
    
    def Format_p(x, counter):
		
        return '{0:{1}}'.format(x, '.2f').replace('.', ',')
	 
	 
 
		 
    
    lat_formatter = LatitudeFormatter(number_format=number_format,
                                      degree_symbol=degree_symbol,
                                      north_hemisphere_str=north_hemisphere_str,
                                      south_hemisphere_str=south_hemisphere_str)
    
    
    gl.xformatter = lon_formatter
    gl.yformatter = lat_formatter
    
    
    gl.xlabel_style = gridline_xlabel_style
    gl.ylabel_style = gridline_ylabel_style
    
    
    change_gridline_tick_formating(gl,  
                                   gridline_tick_formating=longitude_tick_formating.get('number_format', '.2f'), 
                                   axis='x', decimal_separator=decimal_separator,
                                   geographical_symbol=geographical_symbol)
    
    change_gridline_tick_formating(gl,  
                                   gridline_tick_formating=latitude_tick_formating.get('number_format', '.2f'), 
                                   axis='y', decimal_separator=decimal_separator,
                                   geographical_symbol=geographical_symbol)
       
    
    
    
    return gl
        
        
     
    
    

if '__main__' ==__name__:
        
    
    
    import matplotlib.pyplot as plt
    
    import geopandas as gpd
    import cartopy.crs as ccrs
    
    
    SHP_path = r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp'
    
    SHP = gpd.read_file(SHP_path)
    
    SHP['CD_GEOCMU'] = SHP['CD_GEOCMU'].apply(int)
    
    
    projection = ccrs.PlateCarree() # projection.proj4_init
    
    Transform = ccrs.Geodetic(globe=ccrs.Globe(ellipse='GRS80'))
    
    
    
    fig, ax = plt.subplots(1, subplot_kw={'projection':projection})
    
    
    SHP.plot(ax=ax)
    
    Grider = ax.gridlines(draw_labels=True)
    
   
    
    change_gridline_tick_formating(Grider,  axis='both')
    
    
    
    set_gridline_tick_axis_positions(Grider, 
                                                             positions={'top': False, 
                                                                        'bottom': True, 
                                                                        'left': True, 
                                                                        'right': False})
    
   
    
    fig.subplots_adjust()
    
    fig.show()
    
    
    
    ##################################################################################################################
    
    ##################################################################################################################
    
    ##################################################################################################################
    
    ##################################################################################################################
    
    fig, ax = plt.subplots(1, subplot_kw={'projection':projection})
    
    
    SHP.plot(ax=ax)
    
    
    
    gl = add_custom_gridline(ax, 
                            
                            gridline_attr=dict(draw_labels=True,
                                               linewidth=1, 
                                            color='black', 
                                            alpha=0.35, 
                                            linestyle='--'),
                                               
                            n_coordinate_ticks={'x_number':12,  'y_number':4},
                            
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
    							
    							
            
                            
    							gridline_tick_axis_positions={'xlabels_top':False,
    												 'ylabels_left':True,
    												 'ylabels_right':False,
    												 'xlabels_bottom':True}												   
                            
                            )

   
                     
    
    fig.subplots_adjust()
    fig.draw(fig.canvas.get_renderer())
    fig.show()