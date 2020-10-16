# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 11:11:00 2020

@author: Philipe_Leal
"""
import geopandas as gpd
import fancy_spatial_geometries_plot

dir_path = fancy_spatial_geometries_plot.__path__
import os



def get_standard_gdf():
    """ basic function for getting some geographical data in geopandas GeoDataFrame python's instance:
        An example data can be downloaded from Brazilian IBGE:
        ref: ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2017/Brasil/BR/br_municipios.zip    
    """
    gdf_path = os.path.join(dir_path, 'Data_example\MUNICIPIOS_PARA.shp')

    return gpd.read_file(gdf_path)
