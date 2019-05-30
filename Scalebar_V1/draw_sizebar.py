# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:36:26 2019

@author: lealp
"""





def draw_sizebar(ax, 
                 x_size_in_data_units=3, 
                 rounding_value_for_xsize = 0,
                 bar_height=0.015, 
                 fill_bar=True, 
                 fill_bar_color='k', 
                 fontproperties = None,
                 label_top=True,
                 loc='center left', 
                 pad=5, 
                 borderpad=0, 
                 add_background_to_scalebar=True,
                 background_facecolor = 'k',
                 face_alpha=0.1,
                 length_unit= 'Km',
                 unit_transformation_function=None,
                 background_xpadding=0.25,
                 background_ypadding = 0.2,
                 background_edgecolor = 'k',
                 background_linewidth =1,
                 background_edgealpha = 1,
                 sep=2, 
                 x0=0.82, 
                 y0=0.2,
                 x1=1, 
                 y1=0.5):
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
        
        x_size_in_data_units (float): the longitudinal size to create the scalebar. Units in longitudinal data coordinates transform.
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
        
        pad (float): sets the vertical distance from the sizebar and its label in fraction of the font \
                     size
            Standard = 0.1
            
        --------------------------------------------------------------------------------------------------------------    
        
        background_xpadding (float): sets the longitudinal padding distance from the sizebar and its background Bbox in fraction of 
                                     the figure transform
            Standard = 0.5
        
        -------------------------------------------------------------------------------------------------------------    
        
        
        background_ypadding (float): sets the latitudinal  padding distance from the sizebar and its background Bbox \
                                     in fraction of the figure transform
            Standard = 0.2
        
       
        --------------------------------------------------------------------------------------------------------------    
        
        add_background_to_scalebar (bool): whether to add a background to the colorbar or not
            Standard=False
        
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
        
        unit_transformation_function: the function to convert the scale unit into the desired distance measurement unit, 
            in case that measurement unit is not "km" or 'm'. This passed function must convert meters to the desired unit, 
            and return the converted value in the desired unit.
            
            Example of converting a meter to mile: unit_transformation_function = lambda x: x*0,00062137
            
            Standard: None (so that no transformation is applied)
        
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
        
        
    Returns (tuple):
        1) The extent of the colorbar in rendered window units
        
        2) The extent of the colorbar in figure window units
    
    """
    
    
    
    try:
        from Functions.get_geo_axes_extent import get_distance
    except:
        from . Functions.get_geo_axes_extent import get_distance
    
    try:
        from Functions.add_background_to_scalebar import add_background
    except:
        from . Functions.add_background_to_scalebar import add_background

    
    
    import cartopy.crs as ccrs
    
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    
    from matplotlib import transforms
    
    from matplotlib.transforms import Bbox
    
    import matplotlib
    
    
    if ax.projection != ccrs.PlateCarree():
        raise ("The axes projection must be the ccrs.PlateCarree() projection in order for this algorithm to work.")
    
    
    
    
    
    # the x coords of this transformation are data, and the
    # y coord are axes
    trans = transforms.blended_transform_factory(
        ax.transData, ax.figure.transFigure)
    
    
    if not isinstance(fontproperties, matplotlib.font_manager.FontProperties):
    
        from matplotlib.font_manager import FontProperties


        fontproperties = FontProperties(family='calibri', weight='light', style='normal', size=10)
    
    if (length_unit.lower() not in ['km', 'm', 'meter', 'kilometer']) and unit_transformation_function == None:
        raise Exception("""If length_unit is not Km or meter unit, a transformation function must be supplied for the attribute \
                            unit_transformation_function """)
        
    
    
    bar = AnchoredSizeBar(transform=trans, 
                          loc=loc,
                          color=fill_bar_color,
                          size=x_size_in_data_units,
                          size_vertical=bar_height,
                          label='{0} {1}'.format(get_distance(ax = ax, 
                                                              x_size_in_data_units = x_size_in_data_units, 
                                                              rounding_value_for_xsize = rounding_value_for_xsize,
                                                              length_unit = length_unit, 
                                                              unit_transformation_function = unit_transformation_function), 
                                                 length_unit),
                          label_top=label_top,
                          pad=pad, 
                          fontproperties=fontproperties,
                          borderpad=borderpad, 
                          sep=sep, 
                          frameon=False, 
                          fill_bar=fill_bar,
                          bbox_to_anchor = Bbox.from_extents(x0, y0, x0, y0),
                          bbox_transform=ax.figure.transFigure)
    
   
    
    ax.add_artist(bar)
    
    window_extent = bar.get_window_extent(ax.figure.canvas.get_renderer())
    
    figure_window_extent = ax.figure.transFigure.inverted().transform(window_extent)
    
    x0, y0, x1, x1 = figure_window_extent.ravel()
    
    if add_background_to_scalebar == True:
        
        add_background(ax, x0, x1, y0, y1, 
                            facecolor=background_facecolor, 
                            face_alpha=face_alpha, 
                            linewidth =background_linewidth,
                            transform=ax.figure.transFigure, 
                            background_xpadding=background_xpadding,
                            background_ypadding=background_ypadding,
                            edgecolor = background_edgecolor,
                            edgealpha=background_edgealpha)
        
    return window_extent, figure_window_extent





if "__main__" == __name__:

    import geopandas as gpd
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    Para = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp')

    
    Projection = ccrs.PlateCarree()

    fig, ax = plt.subplots(1, subplot_kw={'projection':Projection})

    
    Para.plot(ax=ax, transform=Projection)

    draw_sizebar(ax, x0=0.82, y0=0.2, x1=1, y1=0.5, sep=2, pad=.5, 
                                     borderpad=0, x_size_in_data_units=3, 
                                     loc='center left',
                                     background_xpadding=0.25,
                                     background_ypadding=0.2,
                                     add_background_to_scalebar=True,
                                     fill_bar_color='k',
                                     face_alpha=0.1,
                                     background_edgecolor = 'k',
                                     background_linewidth=1,
                                     length_unit='km',
                                     unit_transformation_function=None)

    Gridliner = ax.gridlines(crs=Projection, draw_labels=True)

    Gridliner.xlabels_top = False
    Gridliner.ylabels_right = False


    fig.show()