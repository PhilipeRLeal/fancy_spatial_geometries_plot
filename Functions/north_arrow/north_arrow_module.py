# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:53:33 2019

@author: lealp
"""


import matplotlib.patches as mpatches

import pandas as pd
pd.set_option('display.width', 50000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def add_north_arrow_to_fig(fig, 
                    x_tail = 0.892,
                    y_tail = 0.08,
                    x_head = 0.892,
                    y_head = 0.12,
                    width=0.05,
						label_pad=0.012,
                    transform=None):
    
    """Function that adds north arrow plus a text over the arrows head
    
    parameters: 
        
        geo_axes a cartopy geoaxes instance
        
        x_tail = (float) 0.975   - the xbase of the arrow 
        y_tail = (float) 0.01    - the ybase of the arrow
        x_head = (float) 0.975   - the xtop of the arrow
        y_head = (float) 0.030,  - the ytop of the arrow
        width=0.05: the width of the arrows head
			label_pad: the distance in figure units from the label to the arrow.
        transform: the transform that wil be used to set the position of the arrow in the figure/axes
        (standard): None == fig.transFigure
    

		Returns:
		
			geo_axes
        
    """
    
    
    
    dx = x_head - x_tail
    dy = y_head - y_tail


    
    if transform==None:
        transform=fig.transFigure
    
    arrow = mpatches.Arrow(x_tail, y_tail, dx, dy, width=width, transform=transform, color='k', figure=fig)

    fig.patches.extend([arrow])

    fig.text(x_head, 
				 y_head + label_pad , 
				s='N', 
				size=11, 
				ha='center', 
				va='center',
				color='K', 
				transform=transform, 
				figure=fig)

    
    return fig
    
    
   

if '__main__' ==__name__:
        
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    SHP_path = r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp'
    
    SHP = gpd.read_file(SHP_path)
    
    SHP['CD_GEOCMU'] = SHP['CD_GEOCMU'].apply(int)
    
    
    projection = ccrs.PlateCarree() # projection.proj4_init
    
    Transform = ccrs.Geodetic(globe=ccrs.Globe(ellipse='GRS80'))
    
    
    
    fig, ax = plt.subplots(1, subplot_kw={'projection':projection})
    
    SHP.plot(ax=ax, column= 'CD_GEOCMU', legend=True)
     
    ax = add_north_arrow_to_fig(fig=fig, transform=fig.transFigure, x_tail=0.1, x_head=0.1)
 
    
    fig.subplots_adjust(top=0.88,
                        bottom=0.18,
                        left=0.11,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)
                            
    fig.show()
    