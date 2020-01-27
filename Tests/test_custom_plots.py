
from unittest import TestCase

import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os
import glob
from custom_plots import (scale_bar_class, format_axis_ticks_to_scientific_notation,
                          add_north_arrow_to_fig, zebra_ticks,
                          custom_colorbars,
                          add_gridlines)
                       
add_colorbar_for_axes = custom_colorbars.add_colorbar_for_axes
format_cbar_ticks_to_scientific_notation = custom_colorbars.format_cbar_ticks_to_scientific_notation



def get_shp_example():
    
    cpath = '/'.join([os.path.dirname(__file__), 'Data_example'])
    path_file = glob.glob(cpath + '/*.shp' )
    

    return  gpd.read_file(path_file[0])



class Tester_custom_plots(TestCase):

    def test_gridline(self):
        try:
            gdf = get_shp_example()
             
            Projection = ccrs.PlateCarree()
            
            fig1, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
            
            gdf.plot(ax=ax, transform=Projection)
            add_gridlines(ax)
            
            self.assertTrue(True) 
            
        except:
            self.assertTrue(False) 
            
    def test_zebra_ticks(self):
        try:
            Z = zebra_ticks()
            self.assertTrue(True) 
            
        except:
            self.assertTrue(False) 
    def test_scale_bar(self):
        try:
            gdf = get_shp_example()
             
            Projection = ccrs.PlateCarree()
            
            fig1, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
            
         
            gdf.plot(ax=ax, transform=Projection)
            
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
            
            
            fig1.show()
        
            self.assertTrue(True) 
        except:
            self.assertTrue(False) 
       
    def test_north_arrow(self):
        try:
            gdf = get_shp_example()
                
            Projection = ccrs.PlateCarree()
            
            fig2, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})
            
         
            gdf.plot(ax=ax, transform=Projection)
            
            
            add_north_arrow_to_fig(fig=fig2, transform=fig2.transFigure, x_tail=0.1, x_head=0.1)
 
            
            
            Gridliner = ax.gridlines(crs=Projection, draw_labels=True)
            
            Gridliner.xlabels_top = False
            Gridliner.ylabels_right = False
            
            
            fig2.show()
        
            self.assertTrue(True) 
        except:
            self.assertTrue(False) 
        
        
    def test_add_colorbar_for_axes(self):
        try:
            SHP = get_shp_example()

            SHP['CD_GEOCMU'] = SHP['CD_GEOCMU'].apply(float)
            
            vmin = SHP['CD_GEOCMU'].min()
            
            vmax = SHP['CD_GEOCMU'].max()
            
            
            projection = ccrs.PlateCarree() # projection.proj4_init

            fig3, ax = plt.subplots(1, subplot_kw={'projection':projection})
            
            
            SHP.plot(ax=ax, column='CD_GEOCMU')
            
            
            add_north_arrow_to_fig(fig=fig3,
                                   transform=fig3.transFigure, x_tail=0.05, x_head=0.05)
            
            
            cbar = add_colorbar_for_axes(axes=ax, 
                                         vmin=vmin, 
                                         vmax=vmax, 
                                         n_ticks_in_colorbar=5)
            
            format_cbar_ticks_to_scientific_notation(cbar, decimal_separator='.')
            
            Gridliner = ax.gridlines(draw_labels=True)
            
            Gridliner.xlabels_top = False
            Gridliner.ylabels_right = False
            
            box = scale_bar_class.scalebar_based_on_degree_distance(ax=ax, x_size_in_degrees=3, 
                                                                    pad=0.5,sep=2, borderpad=5, 
                                                                    length_unit='km',
                                                                    background_facecolor=(1,1,1,0.5),
                                                                    background_edgecolor ='purple',
                                                                    background_facealpha=1,
                                                                    x0=0.8,
                                                                    y0=0.02,
                                                                    x1=1,
                                                                    y1=0.08)

            fig3.show()    
            self.assertTrue(True) 
        except:
            self.assertTrue(False)