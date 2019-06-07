# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:09:00 2019

@author: lealp
"""


import matplotlib.pyplot as plt

import numpy as np
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import (AnchoredOffsetbox, HPacker)
from matplotlib import transforms
from matplotlib.transforms import Bbox
import matplotlib


class scale_bar_class(object):
    
	
    @ staticmethod
	
		
    def get_central_x_point_from_scalebar_in_fig_coordinates(scalebar):
        """
		Function description:
			The function receives a scale_bar_class.scalebar object and returns its central x position in figure coordinates
		
        """
	
        fig = scalebar.get_figure()
        x1, dx1, ty, dty = fig.transFigure.inverted().transform(scalebar.get_bbox_to_anchor()).ravel()
		
        x1 = x1 + dx1
		
        x2 = ty - x1
		
        y1 = ty - dty
		
        y2 = dty

        mean = (x1 + x2)/2
		
        return mean

	
    @ staticmethod
    def get_local_TransVerse_Mercator_Projection_for_given_geoaxes(ax, x_size_in_degrees):
        """
        ax is the axes to draw the scalebar on.
        length is the length of the scalebar in km.
        location is center of the scalebar in axis coordinates.
        (ie. 0.5 is the middle of the plot)
        linewidth is the thickness of the scalebar.
        """

        location=(0.5, 0.05)
        #Get the limits of the axis in lat long
        llx0, llx1, lly0, lly1 = ax.get_extent(ax.projection)
        #Make tmc horizontally centred on the middle of the map,
        #vertically at scale bar location
        sbllx = (llx1 + llx0) / 2
        sblly = lly0 + (lly1 - lly0) * location[1]
        tmc = ccrs.TransverseMercator(sbllx, sblly)

        relative_ax_size = x_size_in_degrees/abs(llx1 - llx0)

        return tmc, relative_ax_size


    @ staticmethod
    def calculate_distance_based_on_Transverse_mercator_projection(ax, x_size_in_degrees, 
                                                                   rounding_value_for_xsize=0, 
                                                                   length_unit='Km', 
                                                                   unit_transformation_function=None):
        """
        ax is the axes to draw the scalebar on.
        x_size_in_degrees: it is size of the scalebar in Data transform coordinates (in degrees).

        rounding_value_for_xsize: it is the rounding value (number of decimal cases) to be used in the transformed \
                                  scalebar size and legend

        length_unit (string): The distance unit measurement that will be used in the scalebar. Available options: ['m', 'Km']
                If other distance unit measurement is provided (ex: miles), one must add a transformation function from meters \
                to the required unit in the attr: "unit_transformation_function"

                Standard: 'Km'

        unit_transformation_function: the function to convert the scale unit into the desired distance measurement unit, 
            in case that measurement unit is not "km" or 'm'. This passed function must convert meters to the desired unit, 
            and return the converted value in the desired unit.

            Example of converting a meter to mile: unit_transformation_function = lambda x: x*0,00062137

            Standard: None (so that no transformation is applied)

        """

        tmc, relative_ax_size = scale_bar_class.get_local_TransVerse_Mercator_Projection_for_given_geoaxes(ax, x_size_in_degrees)

        # Get the extent (x0, x1, y0, y1) of the map in the given coordinate system.
        # If no crs is given, the returned extents' coordinate system will be
        # the CRS of this Axes.

        # use Projection TransverseMercator (whose unit is in meters) for converting the measurement in meters
        x0, x1, y0, y1 = ax.get_extent(tmc)
        #Turn the specified scalebar location into coordinates in metres



        sbx = (x1 - x0) * relative_ax_size 

        if (unit_transformation_function is not None) and (length_unit.lower() !='km') and (length_unit.lower() !='m'):
            sbx = unit_transformation_function(sbx)

        print("sbx", sbx)

        if length_unit.lower()=='km':

            sbx = sbx /1000.0 # meters for Km

        sbx = np.round(sbx, rounding_value_for_xsize)

        if rounding_value_for_xsize == 0:

            sbx = np.int(sbx)

        return sbx    
    
    
    @ staticmethod
    
    def distance_from_degrees_using_geopy(ax, longitudinal_distance_in_degrees, 
                                          ellipsoid='WGS-84', 
                                          distance_method='vincenty', 
                                          length_unit='Km',
                                          rounding_value_for_xsize=2):
        """
        Function that returns the distance between Point_latLon_1, Point_latLon_2 
        based on Ellipsoid distance using geodesic points. 
        
        Alternative distance measuring algorithms:
             geodesic distance : Standard method
             great_circle distance: alternative method
        
        Standard Ellipsoid is wgs-84.
            Alternative Ellipsoids (geopy.distance.ELLIPSOIDS):
            
                {'WGS-84': (6378.137, 6356.7523142, 0.0033528106647474805),
                 'GRS-80': (6378.137, 6356.7523141, 0.003352810681182319),
                 'Airy (1830)': (6377.563396, 6356.256909, 0.0033408506414970775),
                 'Intl 1924': (6378.388, 6356.911946, 0.003367003367003367),
                 'Clarke (1880)': (6378.249145, 6356.51486955, 0.003407561378699334),
                 'GRS-67': (6378.16, 6356.774719, 0.003352891869237217)}
            
            If ellipsoid is not present in the dictionary, one may give a 3d-tuple indicating the ellipsoid in the following format:
                (semimajor_axis, semiminor_axis, flattening_alpha)
                
                semimajor_axis, semiminor_axis, 
                
                flattening_alpha = (semimajor_axis - semiminor_axis)/semimajor_axis
                
                i.e.:
                    semimajor_axis = 6377
                    semiminor_axis = 6356
                    flattening_alpha = 1/297
                    
        Returns:
            Distance in km
        
        """
        
        
        
        x0, x1, y0, y1 = ax.get_extent()

        Point_latLon_1 = ( np.mean([y0, y1]), np.mean([x0, x1]) )
        
        Point_latLon_2 = (np.mean([y0, y1]), np.mean([x0, x1]) + longitudinal_distance_in_degrees) 
        
       
        from geopy import distance
        if distance_method=='geodesic':
            
            Value = getattr(distance.distance(Point_latLon_1, Point_latLon_2, ellipsoid=ellipsoid), length_unit)
        
            if rounding_value_for_xsize == 0:

            
                return int(round(Value, rounding_value_for_xsize))
            
            else:
                return round(Value, rounding_value_for_xsize)
            
        
       
            
        else: # great_circle
            
            Value = getattr(distance.great_circle(Point_latLon_1, Point_latLon_2, ellipsoid=ellipsoid), length_unit)
            if rounding_value_for_xsize == 0:

            
                return int(round(Value, rounding_value_for_xsize))
            
            else:
                return round(Value, rounding_value_for_xsize)
            
    @ staticmethod
    
    def add_anchored_size_bar(ax,
						      transform, 
                              loc='center',
                              color='k',
							  horizontal_size=3,
                              label= None,
                              label_top=True,
                              pad=0.3, 
                              fontproperties=None,
                              borderpad=0.1, 
                              sep=0.2, 
                              bar_height=0.015,
							  frameon=True, 
                              fill_bar=True,
                              bbox_to_anchor = (0.5, 0.02, 1, 0.08), # (x0, y0, x1, y1),
                              bbox_transform='figure'):
            
            if bbox_transform == 'figure':
                bbox_transform = ax.figure.transFigure
            
            bar = AnchoredSizeBar(transform=transform, 
                                  loc=loc,
                                  color=color,
                                  size=horizontal_size,
                                  size_vertical=bar_height,
                                  label= label,
                                  label_top=label_top,
                                  pad=pad, 
                                  fontproperties=fontproperties,
                                  borderpad=borderpad, 
                                  sep=sep, 
                                  frameon=frameon, 
                                  fill_bar=fill_bar,
                                  bbox_to_anchor = Bbox.from_extents(bbox_to_anchor),
                                  bbox_transform=bbox_transform)



            ax.add_artist(bar)

            #window_extent = bar.get_window_extent(ax.figure.canvas.get_renderer())

            #figure_window_extent = ax.figure.transFigure.inverted().transform(window_extent)

            #x0, y0, x1, x1 = figure_window_extent.ravel()
            return bar
    
    
    
    @ staticmethod

    def scalebar_based_on_degree_distance(ax, 
                                          distance_measuring_method='geopy',
                                          ellipsoid='WGS-84', 
                                          distance_method='geodesic',
                                          x_size_in_degrees=1, 
                                          rounding_value_for_xsize = 0,
                                          decimal_separator=',',
                                          bar_height=0.015, 
                                          fill_bar=True, 
                                          fill_bar_color='k', 
                                          fontproperties = None,
                                          label_top=True,
                                          loc='center', 
                                          pad=0.3, 
                                          borderpad=0,
                                          background_facecolor = 'white',
                                          face_alpha=1,
                                          length_unit= 'km',
                                          unit_transformation_function=None,
                                          background_edgecolor = 'k',
                                          background_linewidth =1,
                                          background_edgealpha = 1,
                                          background_facealpha =1,
                                          sep=0, 
                                          x0=0.91,
                                          y0=0.02,
                                          x1=1,
                                          y1=0.08,
                                          K_times=3,
                                          over_write_distance_metric=False):
        
        """
            Function description:
                This function adds a sizebar in the axes. 
                This sizebar is an artist of matplotlib. 
                This artist x_size automatically dilates or contracts acoording to the zooming (in/out) \
                of its parent axes.

            --------------------------------------------------------------------------------------------------------------    

            Parameters:

                ax: the parent axes that will be used to measure the distance for the sizebar
                
                --------------------------------------------------------------------------------------------------------------    

                distance_measuring_method (string): sets the type of distance measuring system over geodetic (degree) distances
                    Available options: ['geopy', 'Transverse_mercator_projection']
                    
                        Geopy option requires extra parameters for its evaluation which are set by the ellipsoid and distance_method parameters
                        
                
                    Standard: 'geopy'
                --------------------------------------------------------------------------------------------------------------    

                ellipsoid (string or (3d-tuple)): sets the ellipsoid that will be used for the distance measuring system. WGS-84 garantees standard error distance for all the globe. 
                                                  Better precision can be acchieved by local specific Ellipsoid
                
                    Standard: 'WGS-84'
                    
                    Observation: this parameter is only applicable for distance_measuring_method == 'geopy'
                --------------------------------------------------------------------------------------------------------------    

                distance_method (string): sets the type of distance measuring system that will be applied over the scalebar. It will convert
                                          degree distance into planar distance.
                                          
                    
                    Available options: ['vincety': most precise
                                        'geodetic/geodesic': will converge always
                                        'great_circle': commonly used in the literature
                                        ]
                                        
                    Standard: 'vincenty'
                
                    Observation: this parameter is only applicable for distance_measuring_method == 'geopy'
                --------------------------------------------------------------------------------------------------------------    

                x_size_in_degrees (float): the longitudinal size to create the scalebar. Units in longitudinal data coordinates transform.
                     Standard = 0.2

                --------------------------------------------------------------------------------------------------------------    

                rounding_value_for_xsize: the rounding decimal cases to be used in the scalebar label.

                --------------------------------------------------------------------------------------------------------------    

                bar_height (float): the relative height of the scalebar in figure units
                    Standard = 0.015

                --------------------------------------------------------------------------------------------------------------    

                fill_bar (bool): this sets whether to fill or not the bar. The filling color is setted by the color attribute
                    Standard = True

                --------------------------------------------------------------------------------------------------------------    

                fill_bar_color ('string' or Tuple): sets the color to be used in the filling process of the scalebar

                --------------------------------------------------------------------------------------------------------------    

                fontproperties (matplotlib.font_manager.FontProperties): sets the fontproperties to be used in the label of the scalebar

                    Example:

                        from matplotlib.font_manager import FontProperties

                        fontproperties = FontProperties(family='calibri', weight='light', style='normal', size=10)

                --------------------------------------------------------------------------------------------------------------    

                label_top (Bool): sets the label vertical position relative to the scalebar. For standard, the legend is above the scalebar
                    Standard = True

                --------------------------------------------------------------------------------------------------------------    

                loc (string): this attribute sets the label position relative to the bounding box
                    Standard = 'upper right'
                    Options available: [upper right, upper left, 
                                        lower left, lower right,
                                        right, center left,
                                        center right, lower center,
                                        upper center, center]

                --------------------------------------------------------------------------------------------------------------    

                pad (float): sets the vertical distance from the scalebar and its background Bbox in fraction of the font \
                             size
                    Standard = 0.1

                --------------------------------------------------------------------------------------------------------------    

                background_facecolor = sets the color to the background color'k'

                --------------------------------------------------------------------------------------------------------------    

                face_alpha (string): sets the color to the background alpha
                    Standard = 'grey'

                --------------------------------------------------------------------------------------------------------------    

                length_unit (string): The distance unit measurement that will be used in the scalebar. Available options: ['m', 'Km']
                    If other distance unit measurements are required, add a transformation function from meters to the required unit 
                    in the attr: "unit_transformation_function"

                    Standard: 'Km'
                
                
                --------------------------------------------------------------------------------------------------------------    

                
                unit_transformation_function: the function to convert the scale unit into the desired distance measurement unit, 
                    in case that measurement unit is not "km" or 'm'. This passed function must convert meters to the desired unit, 
                    and return the converted value in the desired unit.

                    Example of converting a meter to mile: unit_transformation_function = lambda x: x*0,00062137

                    Standard: None (so that no transformation is applied)
                    
                    Observation: this parameter is only applicable for distance_measuring_method == 'Transverse_mercator_projection'
                --------------------------------------------------------------------------------------------------------------    


                background_padding=100,

                --------------------------------------------------------------------------------------------------------------    

                background_edgecolor (string; or tuple(RGB); or tuple(RGBA) ): sets the color to be used in the edgecolor of the bbox 
                    Standard = 'k'

                --------------------------------------------------------------------------------------------------------------    

                background_linewidth (float): the width of the line surrounding the Bbox
                    Standard = 1

                --------------------------------------------------------------------------------------------------------------    

                sep (int): Separation between the label and the size bar, in points
                    Standard = 5
                --------------------------------------------------------------------------------------------------------------    

                x0 (float): the relative longitudinal position to be placed the scalebar in figure units.
                    Standard = 0.8

                --------------------------------------------------------------------------------------------------------------    

                y0 (float): the relative latitudinal position to be placed the scalebar in figure units.
                    Standard = 0.1


                --------------------------------------------------------------------------------------------------------------    
                --------------------------------------------------------------------------------------------------------------    


            Returns:
                box that encompasses the scalebar

        """

        if ax.projection != ccrs.PlateCarree():
            raise ("The axes projection must be the ccrs.PlateCarree() projection in order for this algorithm to work.")





        # the x coords of this transformation are data, and the
        # y coord are axes
        trans = transforms.blended_transform_factory(
            ax.transData, ax.figure.transFigure)


        if not isinstance(fontproperties, matplotlib.font_manager.FontProperties):

            fontproperties = FontProperties(family='calibri', weight='light', style='normal', size=10)


        
        if distance_measuring_method =='geopy':
            
            get_distancer = getattr(scale_bar_class, 'distance_from_degrees_using_geopy')
            
            Distance = get_distancer(ax = ax, 
                                      longitudinal_distance_in_degrees = x_size_in_degrees, 
                                      ellipsoid=ellipsoid, 
                                      distance_method=distance_method, 
                                      length_unit=length_unit,
                                      rounding_value_for_xsize = rounding_value_for_xsize)
            
            if rounding_value_for_xsize == 0:
                converted_string = int(Distance)
        
            else:
            
                converted_string = str(Distance).replace('.', decimal_separator)
        
            Formatted_Label = '{0} {1}'.format(converted_string, length_unit)
            

        else:
            
            if (length_unit.lower() not in ['km', 'm', 'meter', 'kilometer']) and unit_transformation_function == None:
                raise Exception("""If length_unit is not Km or meter unit, a transformation function must be supplied for the attribute \
                                unit_transformation_function """)
            
            get_distancer = getattr(scale_bar_class, 'calculate_distance_based_on_Transverse_mercator_projection')
            
            
            
            Distance = get_distancer(ax = ax, 
                                      x_size_in_degrees = x_size_in_degrees, 
                                      rounding_value_for_xsize = rounding_value_for_xsize,
                                      length_unit = length_unit, 
                                      unit_transformation_function = unit_transformation_function)
            
            
            
            if rounding_value_for_xsize == 0:
                converted_string = int(Distance)
        
            else:
            
                converted_string = str(Distance).replace('.', decimal_separator)
        
            Formatted_Label = '{0} {1}'.format(converted_string, length_unit)


        if over_write_distance_metric is not False:
            Formatted_Label = '{0} {1}'.format(over_write_distance_metric, length_unit)
            
            print(Formatted_Label)
        
            
            
        from functools import partial
        
        P_scale_bar_c = partial(scale_bar_class.add_anchored_size_bar, ax=ax,
														  transform=trans, 
														  loc=loc,
														  color='k',
														  horizontal_size=x_size_in_degrees,
														  label= Formatted_Label,
														  label_top=label_top,
														  pad=pad,
														  bar_height=bar_height,
														  fontproperties=fontproperties,
														  borderpad=borderpad, 
														  sep=sep, 
														  frameon=True, 
														  bbox_to_anchor=(x0,y0,x1, y1),
														  bbox_transform=ax.figure.transFigure)
        

        Bbox_bar = P_scale_bar_c(fill_bar=True)
            

        child = HPacker(pad=0.2, sep=0.2, width=0.2, height=0.2, align='baseline', 
                        mode='fixed', children=[Bbox_bar])
       
         
        
        box = AnchoredOffsetbox(loc='center',
                                pad=pad,
                                borderpad=0.5,
                                child=child,
                                frameon=False, bbox_to_anchor=(x0, y0, x1,y1),
                                bbox_transform=ax.figure.transFigure)
        
        
        box.patch.set_color(background_facecolor)
        box.patch.set_alpha(background_facealpha)
        box.patch.set_edgecolor(background_edgecolor)

        
        box.axes = ax
        box.set_figure(ax.get_figure())
        
        return box
    
    
    @ staticmethod
    
    def scalebar_based_on_planar_distance(ax,
                                          x_planar_size=1, 
                                          rounding_value_for_xsize = 0,
                                          bar_height=0.015, 
                                          decimal_separator=',',
                                          fill_bar=True, 
                                          fill_bar_color='k', 
                                          fontproperties = None,
                                          label_top=True,
                                          loc='center', 
                                          pad=0, 
                                          borderpad=0,
                                          background_facecolor = 'k',
                                          face_alpha=1,
                                          length_unit= 'm',
                                          unit_transformation_function=None,
                                          background_edgecolor = 'k',
                                          background_linewidth =1,
                                          background_edgealpha = 1,
                                          background_facealpha =1,
                                          sep=0, 
                                          x0=0.91,
                                          y0=0.02,
                                          x1=1,
                                          y1=0.08,):
        
        """
            Function description:
                This function adds a sizebar in the axes. 
                This sizebar is an artist of matplotlib. 
                This artist x_size automatically dilates or contracts acoording to the zooming (in/out) \
                of its parent axes.

            --------------------------------------------------------------------------------------------------------------    

            Parameters:

                ax: the parent axes that will be used to measure the distance for the sizebar
                

                --------------------------------------------------------------------------------------------------------------    

                x_planar_size (float): the planar longitudinal size to create the scalebar. Units in data coordinates transform.
                     Standard = 200 (units)

                --------------------------------------------------------------------------------------------------------------    

                rounding_value_for_xsize: the rounding decimal cases to be used in the scalebar label.

                --------------------------------------------------------------------------------------------------------------    

                bar_height (float): the relative height of the scalebar in figure units
                    Standard = 0.015

                --------------------------------------------------------------------------------------------------------------    

                fill_bar (bool): this sets whether to fill or not the bar. The filling color is setted by the color attribute
                    Standard = True

                --------------------------------------------------------------------------------------------------------------    

                fill_bar_color ('string' or Tuple): sets the color to be used in the filling process of the scalebar

                --------------------------------------------------------------------------------------------------------------    

                fontproperties (matplotlib.font_manager.FontProperties): sets the fontproperties to be used in the label of the scalebar

                    Example:

                        from matplotlib.font_manager import FontProperties

                        fontproperties = FontProperties(family='calibri', weight='light', style='normal', size=10)

                --------------------------------------------------------------------------------------------------------------    

                label_top (Bool): sets the label vertical position relative to the scalebar. For standard, the legend is above the scalebar
                    Standard = True

                --------------------------------------------------------------------------------------------------------------    

                loc (string): this attribute sets the label position relative to the bounding box
                    Standard = 'upper right'
                    Options available: [upper right, upper left, 
                                        lower left, lower right,
                                        right, center left,
                                        center right, lower center,
                                        upper center, center]

                --------------------------------------------------------------------------------------------------------------    

                pad (float): sets the vertical distance from the scalebar and its background Bbox in fraction of the font \
                             size
                    Standard = 0.1

                --------------------------------------------------------------------------------------------------------------    

                background_facecolor = sets the color to the background color'k'

                --------------------------------------------------------------------------------------------------------------    

                face_alpha (string): sets the color to the background alpha
                    Standard = 'grey'

                --------------------------------------------------------------------------------------------------------------    

                length_unit (string): The distance unit measurement that will be used in the scalebar. Available options: ['m', 'Km']
                    If other distance unit measurements are required, add a transformation function from meters to the required unit 
                    in the attr: "unit_transformation_function"

                    Standard: 'Km'
                
                
                --------------------------------------------------------------------------------------------------------------    

                
                unit_transformation_function: the function to convert the scale unit into the desired distance measurement unit.
                    If unit_transformation_function is provided, the returned value will be the transformation of the planar distance by this given function

                    Example of converting a meter to mile: unit_transformation_function = lambda x: x*0,00062137

                    Standard: None (so that no transformation is applied)
                    
                --------------------------------------------------------------------------------------------------------------    

                background_padding=100

                --------------------------------------------------------------------------------------------------------------    

                background_edgecolor (string; or tuple(RGB); or tuple(RGBA) ): sets the color to be used in the edgecolor of the bbox 
                    Standard = 'k'

                --------------------------------------------------------------------------------------------------------------    

                background_linewidth (float): the width of the line surrounding the Bbox
                    Standard = 1

                --------------------------------------------------------------------------------------------------------------    

                sep (int): Separation between the label and the size bar, in points
                    Standard = 5
                --------------------------------------------------------------------------------------------------------------    

                x0 (float): the relative longitudinal position to be placed the scalebar in figure units.
                    Standard = 0.8

                --------------------------------------------------------------------------------------------------------------    

                y0 (float): the relative latitudinal position to be placed the scalebar in figure units.
                    Standard = 0.1


                --------------------------------------------------------------------------------------------------------------    
                --------------------------------------------------------------------------------------------------------------    


            Returns (tuple):
                1) The extent of the colorbar in rendered window units

                2) The extent of the colorbar in figure window units

        """

    

        # the x coords of this transformation are data, and the
        # y coord are axes
        trans = transforms.blended_transform_factory(
            ax.transData, ax.figure.transFigure)


        if not isinstance(fontproperties, matplotlib.font_manager.FontProperties):

            fontproperties = FontProperties(family='calibri', weight='light', style='normal', size=10)

        if unit_transformation_function !=None:
            converted_string = round(unit_transformation_function(x_planar_size),rounding_value_for_xsize)
        
        else:
            converted_string = round(unit_transformation_function(x_planar_size),rounding_value_for_xsize)
            
        
        if rounding_value_for_xsize == 0:
            converted_string = int(converted_string)
        
        else:
            
            converted_string = str(converted_string).replace('.', decimal_separator)
        
        Formatted_Label = '{0} {1}'.format(converted_string, length_unit)
            
            
        
        Bbox_bar = scale_bar_class.add_anchored_size_bar(ax=ax,
														 transform=trans, 
														 loc=loc,
														 color='k',
														 horizontal_size=x_planar_size,
														 label= Formatted_Label,
														 label_top=label_top,
														 pad=pad, 
														 bar_height=bar_height,
														 fontproperties=fontproperties,
														 borderpad=borderpad, 
														 sep=sep, 
														 frameon=True, 
														 fill_bar=fill_bar,
														 bbox_to_anchor=(x0,y0,x1, y1),
														 bbox_transform=ax.figure.transFigure)
        
               
       
        child = HPacker(pad=0.2, sep=0.2, width=0.2, height=0.2, align='baseline', 
                        mode='fixed', children=[Bbox_bar])

        box = AnchoredOffsetbox(loc='center',
                                pad=pad,
                                borderpad=0.5,
                                child=child,
                                frameon=False, bbox_to_anchor=(x0, y0, x1, y1),
                                bbox_transform=ax.figure.transFigure)
        
        box.patch.set_color(background_facecolor)
        box.patch.set_alpha(background_facealpha)
        box.patch.set_edgecolor(background_edgecolor)
        
        
        box.axes = ax
        box.set_figure(ax.get_figure())
        
        return box
    
    
    
    @ staticmethod
    
    def get_scalebar_with_rounded_kilometer_distance_based(ax, 
                                                           decimal_separator=',',
                                                           distance_in_km=100,
                                                           distance_measuring_method='geopy',
                                                           ellipsoid='WGS-84', 
                                                           distance_method='geodesic', 
                                                           length_unit= 'km',
                                                           unit_transformation_function=None,
                                                           rounding_value_for_xsize = 0,
                                                           bar_height=0.015, 
                                                           fill_bar=True, 
                                                           fill_bar_color='k', 
                                                           fontproperties = None,
                                                           label_top=True,
                                                           loc='center', 
                                                           
                                                           pad=0.1, 
                                                           borderpad=0.1,
                                                           
                                                           background_facecolor = (1,1,1,0.5),
                                                           face_alpha=1,
                                                           
                                                           background_edgecolor = 'k',
                                                           background_linewidth =1,
                                                           background_edgealpha = 1,
                                                           background_facealpha =1,
                                                           
                                                           sep=0.1, 
                                                           x0=0.7,
                                                           y0=0.02,
                                                           x1=0.8,
                                                           y1=0.08):
        """
        Parameters:
            gdf: the geodataframe from which the distance will be evaluated
            
            distance_in_km: the distance that will be used for the scalebar in km units.
        
        """
        
        
        from geopy import distance
    
        import geopy
    
        axis_x0, axis_x1, axis_y0, axis_y1 = ax.get_extent()
        New_Point = distance.geodesic(kilometers=distance_in_km).destination(geopy.Point(longitude=np.mean([axis_x0, axis_x1]), latitude=np.mean([axis_y0, axis_y1]))  ,  90)
        
        longitudinal_degree = New_Point.longitude
        
        dx = abs(np.mean([axis_x0, axis_x1]) - longitudinal_degree)
        
        print('dx: ', dx)
        
       
        
        Box = scale_bar_class.scalebar_based_on_degree_distance( ax=ax,
                                                                 x_size_in_degrees= dx, 
                                                                 distance_measuring_method=distance_measuring_method,
                                                                 ellipsoid=ellipsoid, 
                                                                 distance_method=distance_method,
                                                                
                                                                 rounding_value_for_xsize = rounding_value_for_xsize,
                                                                 decimal_separator=decimal_separator,
                                                                 bar_height=bar_height, 
                                                         
                                                         fontproperties = fontproperties,
                                                         label_top=label_top,
                                                         loc=loc, 
                                                         pad=pad, 
                                                         borderpad=borderpad, 
                                                         background_facecolor = background_facecolor,
                                                         face_alpha=face_alpha,
                                                         length_unit= length_unit,
                                                         unit_transformation_function=unit_transformation_function,
                                                         background_edgecolor = background_edgecolor,
                                                         background_linewidth =background_linewidth,
                                                         sep=sep, 
                                                         x0=x0, 
                                                         y0=y0,
                                                         x1=x1, 
                                                         y1=y1,
                                                         over_write_distance_metric=distance_in_km)
        
        print('criação do Box OK', Box)
        
        return Box

        
    

    
if "__main__" == __name__:
    
    try:
        plt.close('all')
    except:
        None
    
    
    import geopandas as gpd
    
    SHP = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\BRMUE250GC_SIR.shp')
    
    
    RGS = SHP.loc[SHP.UF_ID=='51']
    
    PA = SHP.loc[SHP.UF_ID=='15']
    
     # sirgas 200 polyconic
    
    
    PA.to_crs(epsg=5880, inplace=True)
    
    fig, ax = plt.subplots(1, figsize=(7,6), subplot_kw={'aspect':'equal'})
    
    
    PA.plot(ax=ax)
    
    ax.grid(linewidth=1)
    
    
    
    box = scale_bar_class.scalebar_based_on_planar_distance(ax=ax, x_planar_size=300_000, length_unit='km',
                                                            rounding_value_for_xsize=0,
                                                            unit_transformation_function=lambda x: x/1000,
                                                            pad=0.5,sep=2, borderpad=5, 
                                                            background_edgecolor='purple',
                                                            background_facecolor='orange',
                                                            background_facealpha=1,
                                                            x0=0.4,
                                                             y0=0.02,
                                                             x1=1,
                                                             y1=0.08)
    
    
    
    fig.show()
    
    
    # plotando em graus:
    
    SHP = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\BRMUE250GC_SIR.shp')
    
    
    RGS = SHP.loc[SHP.UF_ID=='51']
    
    PA = SHP.loc[SHP.UF_ID=='15']
    
    Projection = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
    
    
    RGS.plot(ax=ax, transform=Projection)
    
    box = scale_bar_class.scalebar_based_on_degree_distance(ax=ax, x_size_in_degrees=3, 
                                                            pad=0.5,sep=2, borderpad=5, 
                                                            length_unit='km',
                                                            background_facecolor=(1,1,1,0.5),
                                                            background_edgecolor ='purple',
                                                            background_facealpha=1,
                                                            x0=0.4,
                                                             y0=0.02,
                                                             x1=1,
                                                             y1=0.08)
    
    
    Gridliner = ax.gridlines(crs=Projection, draw_labels=True)
    
    Gridliner.xlabels_top = False
    Gridliner.ylabels_right = False
    
    
    fig.show()
    
    
    # plotando em graus:
    
    SHP = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\BRMUE250GC_SIR.shp')
    
    
    RGS = SHP.loc[SHP.UF_ID=='51']
    
    PA = SHP.loc[SHP.UF_ID=='15']
    
    Projection = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
    
    
    PA.plot(ax=ax, transform=Projection)
    
    box = scale_bar_class.scalebar_based_on_degree_distance(ax=ax, x_size_in_degrees=3, 
                                                            pad=0.5,sep=2, borderpad=5, 
                                                            length_unit='km',
                                                            background_facecolor='orange',
                                                            background_edgecolor ='purple',
                                                            background_facealpha=1,
                                                            x0=0.4,
                                                             y0=0.02,
                                                             x1=1,
                                                             y1=0.08)
    
    
    Gridliner = ax.gridlines(crs=Projection, draw_labels=True)
    
    Gridliner.xlabels_top = False
    Gridliner.ylabels_right = False
    
    
    fig.show()
    
    
    
    # plotando em graus em função de uma distância conhecida em km:
    
    SHP = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\BRMUE250GC_SIR.shp')
    
    
    RGS = SHP.loc[SHP.UF_ID=='51']
    
    PA = SHP.loc[SHP.UF_ID=='15']
    
    Projection = ccrs.PlateCarree()
    
    fig, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
    
    
    RGS.plot(ax=ax, transform=Projection)
    
    box = scale_bar_class.get_scalebar_with_rounded_kilometer_distance_based(ax=ax, 
                                                                             distance_in_km=300, 
                                                                             length_unit='km',
                                                                             rounding_value_for_xsize=0,
                                                                             pad=0.5,sep=2, borderpad=5, 
                                                                             background_facecolor=(1,1,1,0.5),
                                                                             background_edgecolor ='purple',
                                                                             background_facealpha=1,
                                                                             x0=0.4,
                                                                             y0=0.02,
                                                                             x1=0.9,
                                                                             y1=0.08)
        
    
    Gridliner = ax.gridlines(crs=Projection, draw_labels=True)
    
    Gridliner.xlabels_top = False
    Gridliner.ylabels_right = False
    
    
    
    fig.show()
    
    
    
    