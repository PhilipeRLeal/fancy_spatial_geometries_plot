# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:49:20 2019

@author: lealp
"""






def get_distance(ax, x_size_in_data_units, rounding_value_for_xsize=0, length_unit='Km', unit_transformation_function=None):
    """
    
    Function description:
        This function receives the distance in degrees (using PlateCarree CRS) and returns in planar units the required distance.
        
    Parameters:
    
        ax is the axes to draw the scalebar on.
        x_size_in_data_units: it is size of the scalebar in Data transform coordinates.
        
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
    
    Returns: 
        distance value (float or int)
    
    """
        
    try:
        from to_Transverse_Mercator_projection import get_local_TransVerse_Mercator_Projection_for_given_geoaxes
    except:
        from . to_Transverse_Mercator_projection import get_local_TransVerse_Mercator_Projection_for_given_geoaxes

    import numpy as np
    
    tmc, relative_ax_size = get_local_TransVerse_Mercator_Projection_for_given_geoaxes(ax, x_size_in_data_units)
    
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
