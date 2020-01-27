
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText

import matplotlib.collections as mcollections
from cartopy.mpl.geoaxes import GeoAxesSubplot





class UpdatablePatchCollection(mcollections.PatchCollection):
    def __init__(self, patches, *args, **kwargs):
        self.patches = patches
        mcollections.PatchCollection.__init__(self, patches, *args, **kwargs)

    def get_paths(self):
        self.set_paths(self.patches)
        return self._paths


plt.ion()



class zebra_ticks():
    
    
    def __init__(self, ax=None, 
             drawlicense=False,
             pad=2):
        
        if not isinstance(ax, GeoAxesSubplot):
            
            projection = ccrs.PlateCarree()
            self.fig = plt.figure(figsize=(9,7))
            self.ax = plt.axes(projection=projection)
            
        else:
            self.ax = ax
        
        
        self.main(drawlicense=drawlicense, pad=pad)
    
    def main(self, drawlicense, pad=2):
        self.ax.stock_img()
    
        # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
        states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
    
        SOURCE = 'Natural Earth'
        LICENSE = 'public domain'
    
        self.ax.add_feature(cfeature.LAND)
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(states_provinces, edgecolor='gray')
    
        # Add a text annotation for the license information to the
        # the bottom right corner.
        
        if drawlicense:
            
            text = AnchoredText(r'$\mathcircled{{c}}$ {}; license: {}'
                                ''.format(SOURCE, LICENSE),
                                loc='right',
                                bbox_transform=self.ax.transAxes,
                                bbox_to_anchor=(1.01, -0.11), 
                                prop={'size': 8}, 
                                frameon=False)
            
            self.ax.add_artist(text)
            
        self.gridliner = self.ax.gridlines(draw_labels=True)
        self.pad = pad
        self.zebras = self.add_zebra()
        
        
        plt.show()
        
        self.ax.callbacks.connect('xlim_changed', lambda x: self.update_zebra)
        self.ax.callbacks.connect('ylim_changed', lambda x: self.update_zebra)

    
    
    def add_zebra(self):
        '''
        Description:
            
            This function add a zebra line border around a cartopy's geoaxes.
            
            It uses the coordinates tick position to evaluate the zebra blocks.
        
        
        returns (dict): {'horizontal:'horizontal_zebras, 'vertical':vertical_zebras}
        
        '''
        
        
        self.fig.canvas.draw()   
        
        lon0, lon1, lat0, lat1 = self.ax.get_extent(crs=self.ax.projection)
        
        ysegs = self.gridliner.yline_artists[0].get_segments()
        yticks = [yseg[0,1] for yseg in ysegs]
        
        xsegs = self.gridliner.xline_artists[0].get_segments()
        xticks = [xseg[0,0] for xseg in xsegs]
        xticks.append(lon1)
        
        i = 0
        
        colors_wk = ['white', 'black']
        
            
        horizontal_zebras={'north':[],
                           'south':[]}
        
        
        vertical_zebras={'east':[],
                           'west':[]}
        
        
        for lon, position in zip([lon0, lon1 - self.pad], ['east', 'west']):
            y0 = xticks[0]
            for enum, y in enumerate(yticks[1:]):
                
                color = colors_wk[i]
                
                delta_coor = (y - y0)
                
                vertical_rect = mpatches.Rectangle( (lon, y0), self.pad , delta_coor, 
                                          transform=self.ax.transData,
                                          facecolor=color, zorder=1000)
                
                vertical_zebras[position].append(vertical_rect)
                
                i = 1 - i
                y0 = y
                
                self.ax.add_patch(vertical_rect)
    
        
        
        
        for lat, position in zip([lat0, lat1 - self.pad], ['south', 'north']):
            x0 = xticks[0]
            
            for x in xticks[1:]:
                
                color = colors_wk[i]
                
                delta_coor = (x - x0)
                
                
                horizontal_rect = mpatches.Rectangle( (x0, lat), delta_coor, self.pad ,
                                          transform=self.ax.transData,
                                          facecolor=color, zorder=1000)
                
                
                horizontal_zebras[position].append(horizontal_rect)
        
                
                x0 = x
                
                i = 1 - i
                
                self.ax.add_patch(horizontal_rect)
#                
#                
#        collection = UpdatablePatchCollection( (vertical_zebras['east'] + 
#                                                vertical_zebras['west'] +
#                                                horizontal_zebras['south'] +
#                                                horizontal_zebras['north']
#                                               ), transform=self.ax.transData
#                                             )
#        
#        self.ax.add_artist(collection)

        
        if self.ax.projection.proj4_params.get('units', 'None') == 'None':
        
            if not (lon0 <=-180 or lon1 >= 180 or lat0>=90 or lat0<=-90):
        
                self.ax.set_extent((lon0-self.pad, 
                                    lon1+self.pad, 
                                    lat0-self.pad, 
                                    lat1+self.pad))
                
        return {'horizontal':horizontal_zebras, 
                'vertical':vertical_zebras}
    
    
    def update_zebra(self, event):
        axes = event.axes
        # trigger the outline and background patches to be re-clipped
        axes.outline_patch.reclip = True
        axes.background_patch.reclip = True
        
        lon0, lon1, lat0, lat1 = self.ax.get_extent(crs=self.ax.projection)
        
        ysegs = self.gridliner.yline_artists[0].get_segments()
        yticks = [yseg[0,1] for yseg in ysegs]
        
        xsegs = self.gridliner.xline_artists[0].get_segments()
        xticks = [xseg[0,0] for xseg in xsegs]
        xticks.append(lon1)
            
        for Vzebras in self.zebras['vertical']:
            for zebra in Vzebras:
                
                for lon, position in zip([lon0, lon1 - self.pad], ['east', 'west']):
                    y0 = xticks[0]
                    for enum, y in enumerate(yticks[1:]):
                        
                        delta_coor = (y - y0)
                        
                        zebra.set_bounds( lon, y0, self.pad , delta_coor)
                        
                        y0 = y
                        
        
        for Hzebras in self.zebras['vertical']:
            for zebra in Hzebras:
                
                for lat, position in zip([lat0, lat1 - self.pad], ['south', 'north']):
                    x0 = xticks[0]
                    
                    for x in xticks[1:]:
                        
                        delta_coor = (x - x0)
                        
                        
                        zebra.set_bounds( x0, lat, 
                                         delta_coor, 
                                         self.pad )
                        
                        
                        x0 = y
                        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()




def add_zebra(gridliner, pad=2):
    '''
    Description:
        
        This function add a zebra line border around a cartopy's geoaxes.
        
        It uses the coordinates tick position to evaluate the zebra blocks.
    
    
    returns (dict): {'horizontal:'horizontal_zebras, 'vertical':vertical_zebras}
    
    '''
    
    
    fig = gridliner.axes.get_figure()
    ax = gridliner.axes
    fig.canvas.draw()   
    
    lon0, lon1, lat0, lat1 = ax.get_extent(crs=ax.projection)
    
    ysegs = gridliner.yline_artists[0].get_segments()
    yticks = [yseg[0,1] for yseg in ysegs]
    
    xsegs = gridliner.xline_artists[0].get_segments()
    xticks = [xseg[0,0] for xseg in xsegs]
    xticks.append(lon1)
    
    i = 0
    
    colors_wk = ['white', 'black']
    
        
    horizontal_zebras={'north':[],
                       'south':[]}
    
    
    vertical_zebras={'east':[],
                       'west':[]}
    
    
    for lon, position in zip([lon0, lon1 - pad], ['east', 'west']):
        y0 = xticks[0]
        for enum, y in enumerate(yticks[1:]):
            
            color = colors_wk[i]
            
            delta_coor = (y - y0)
            
            vertical_rect = mpatches.Rectangle( (lon, y0), pad , delta_coor, 
                                      transform=ax.transData,edgecolor='k',
                                      facecolor=color, zorder=1000)
            
            vertical_zebras[position].append(vertical_rect)
            
            i = 1 - i
            y0 = y
            
            ax.add_patch(vertical_rect)

    
    
    
    for lat, position in zip([lat0, lat1 - pad], ['south', 'north']):
        x0 = xticks[0]
        
        for x in xticks[1:]:
            
            color = colors_wk[i]
            
            delta_coor = (x - x0)
            
            
            horizontal_rect = mpatches.Rectangle( (x0, lat), delta_coor, pad ,
                                      transform=ax.transData,
                                      edgecolor='k',
                                      facecolor=color, zorder=1000)
            
            
            horizontal_zebras[position].append(horizontal_rect)
    
            
            x0 = x
            
            i = 1 - i
            
            ax.add_patch(horizontal_rect)
#                
#                
#        collection = UpdatablePatchCollection( (vertical_zebras['east'] + 
#                                                vertical_zebras['west'] +
#                                                horizontal_zebras['south'] +
#                                                horizontal_zebras['north']
#                                               ), transform=ax.transData
#                                             )
#        
#        ax.add_artist(collection)

    
    if ax.projection.proj4_params.get('units', 'None') == 'None':
    
        if not (lon0 <=-180 or lon1 >= 180 or lat0>=90 or lat0<=-90):
    
            ax.set_extent((lon0-pad, 
                                lon1+pad, 
                                lat0-pad, 
                                lat1+pad))
            
    return {'horizontal':horizontal_zebras, 
            'vertical':vertical_zebras}

if '__main__' == __name__:

    Z = zebra_ticks()
    









