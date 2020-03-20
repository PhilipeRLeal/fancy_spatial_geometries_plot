import matplotlib.pyplot as plt
import cartopy.crs as ccrs   
import geopandas as gpd


from matplotlib.offsetbox import (AnchoredOffsetbox, HPacker)

from my_AnchoredSizeBar import AnchoredSizeBar2

from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar


from matplotlib.offsetbox import PaddedBox
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, VPacker
if "__main__" == __name__:
    shp_path = r'F:\Philipe\Doutorado\BD\IBGE\IBGE_Estruturas_cartograficas_Brasil\2017\Unidades_Censitarias\Municipios\MUNICIPIOS_PARA.shp'

    PA = gpd.read_file(shp_path)

    Projection = ccrs.PlateCarree()

    fig, ax = plt.subplots(1, figsize=(6,6), subplot_kw={'projection':Projection})


    PA.plot(ax=ax, transform=Projection)


    Gridliner = ax.gridlines(crs=Projection, draw_labels=True)

    Gridliner.xlabels_top = False
    Gridliner.ylabels_right = False


    

    size = 2
    nbars = 4
    bars = []

    
    size = 1

    bars = []

    for enum, i in enumerate(range(1,5)[::-1]):
        print(i, end='')
    
        if i % 2 == 0:
            color='k'

        else:
            color='white'
            
        print('\t {0}'.format(color), end='')

    
        label = '{0}'.format(size*(1+enum))
        
        if (1+enum) == nbars:
            label = '{0} units'.format(size*(1+enum))
        
        print('\t {0}'.format(label))

            
        
        bar = AnchoredSizeBar2(ax.transData, size*i, # here is the size multiplier

                              '{0:.0f} data units'.format(size*i), # respective legend
                              label_top=True,
                              frameon=False,
                              borderpad=0.5, 
                              fill_bar=True,
                              color=color,
                              pad=0,
                              sep=1, 
                              loc='upper left',
                              size_vertical=0.45,
                          )



        bars.append(bar)

    box = HPacker(children=bars,
                  align="center",
                  pad=0, sep=0, mode='expand')


    anchored_box = AnchoredOffsetbox(loc='lower left',
                                     child=box, pad=0.,
                                     frameon=True,
                                     bbox_to_anchor=(0.5, 1.52),
                                     bbox_transform=ax.transAxes,
                                     borderpad=0.,
                                     )

    ax.add_artist(anchored_box)

    fig.show()