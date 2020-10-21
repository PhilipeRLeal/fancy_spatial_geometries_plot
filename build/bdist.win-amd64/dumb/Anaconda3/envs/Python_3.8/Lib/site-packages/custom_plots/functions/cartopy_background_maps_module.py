
import cartopy.feature as cfeature



Coastline = cfeature.NaturalEarthFeature(
        category='physical',
        name='Coastline',
        scale='10m',
        facecolor='none')

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

def add_background(ax):

    ax.add_feature(states_provinces, edgecolor='gray')
    ax.add_feature(Coastline, edgecolor='gray')