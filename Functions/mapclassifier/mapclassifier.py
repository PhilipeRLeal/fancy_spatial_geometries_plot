# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:47:39 2019

@author: lealp
"""




class matplotlib_custom_schemer(object):
    
    @ staticmethod
    
    def get_bins_for_transformed_data(series, transformation='log', 
                               mc_classifier='Fisher_Jenks_Sampled' , 
                               k=5, **kwd_for_mc_classifier):
        
        if not callable(transformation):
            import numpy as np
            if hasattr(np, transformation):
                transformation = getattr(np, transformation)
            else:
                print("User must supply a transformation function or a numpy function for it to work")
                
        series = transformation(series)
        
        import mapclassify as mc
        classifier = getattr(mc, mc_classifier)
        
        e = classifier(y=series, k=k, **kwd_for_mc_classifier)
    
        return e
    





if __name__ == "__main__" :
    
    import geopandas as gpd
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import pandas as pd
    import sys
    from matplotlib import ticker
    
    import numpy as np
    
    sys.path.insert(0,r'C:\Users\lealp\Dropbox\Profissao\Python\OSGEO\OGR_Vetor\Geopandas\custom_plots')
    
    from geopandas_custom_plot import geopandas_custom_plot
    
    
    
            
    def wrapped_func (x, y, decimal_separator='.'):

        return geopandas_custom_plot._y_fmt(x, y, decimal_separator=decimal_separator)

    formatter = ticker.FuncFormatter( wrapped_func)

    
    
    
    
    
    
    
    Municipios = gpd.read_file(r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\Todos_Anos\Municipios_por_Ano_2007_a_2017.shp')
    
    Municipios['Datetime'] = Municipios['Datetime'].apply(pd.to_datetime)
    
    Municipios['COD_MUNIC_'] = Municipios['COD_MUNIC_'].astype(int)
    
    Municipios['log_COD_MUNIC_'] = Municipios['COD_MUNIC_'].apply(np.log)
    
    Projection = ccrs.PlateCarree()
    
    width, height = (14,7)
    
    for i in ['custom_colorbar', 'standard_legend_notation']:
        
        
        fig, ax = plt.subplots(3,4, figsize=(width, height), sharex=False, sharey=False, subplot_kw={'projection':Projection})
        
        ax = ax.ravel()
        
        
        minx, miny, maxx, maxy = Municipios.total_bounds
        
        column = 'COD_MUNIC_'
        column_log =  'log_COD_MUNIC_'
        
        for a in ax:
            
            a.set_extent((minx,  maxx, miny, maxy))
            
        for enum, ano in enumerate(Municipios.Datetime.dt.year.unique()):
        
            print(str(ano))
            
            Temp = Municipios.loc[Municipios.Datetime.dt.year == ano]
            
            
            e = matplotlib_custom_schemer.get_bins_for_transformed_data(Temp[column].values, k=6)
            
            ei = e.bins.tolist()
            
            if i.startswith('custom'):
                Legend=False
            else:
                Legend = True
            
            Temp.plot(ax=ax[enum], 
                      column=column_log, 
                      legend=Legend, 
                      markersize = 0.01,
                      legend_kwds={'loc': (1.05, 0.25), 
                                   'bbox_transform':ax[enum].transAxes,
                                  'frameon': True , 
                                  'markerscale':0.4,
                                   'markersize':10,
                                  'handletextpad':0.2,
                                  'handlelength':0.15,
                                  'labelspacing':0.2,
                                  'fontsize':7.5},
                      
                      categorical=False,
                      scheme='user_defined',
                      classification_kwds={'bins':ei},
                      linewidth=0.02,
                      edgecolor='k',
                     facecolor='white')
            
            ax[enum].set_title(str(ano), fontsize=10)
            ax[enum].set_extent((minx,  maxx, miny, maxy))
            
        
        
            if i.startswith('custom'):
                geopandas_custom_plot.add_colorbar_for_axes(axes=ax[enum], vmin=Temp[column].min(), vmax=Temp[column].max(), 
                                                            cmap='viridis', colorbar_ax_yticks_format=formatter )
            
        
        geopandas_custom_plot.add_north_Arrow(ax[enum], x_tail=0.96,
                                                        x_head=0.96, y_tail=0.11, y_head=0.15)
        
        geopandas_custom_plot.get_scalebar_with_rounded_kilometer_distance_based(ax=ax[enum],
                                                                                fill_bar_color='k',
                                                                                background_facecolor='white',
                                                                                decimal_separator=',',
                                                                                distance_in_km=900,
                                                                                distance_measuring_method='geopy',
                                                                                ellipsoid='WGS-84',
                                                                                x0=0.88,
                                                                                y0=0.9,
                                                                                x1=1,
                                                                                y1=0.93,
                                                                                pad=0.2,
                                                                                borderpad=0.01,)
        
        fig.suptitle('Births per year per Municipality in log scale  with user  defined scheme')
        
        fig.subplots_adjust(top=0.88,
        bottom=0.01,
        left=0.01,
        right=0.95,
        hspace=0.25,
        wspace=0.25)
        
        fig.show()
