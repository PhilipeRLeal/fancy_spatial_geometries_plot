# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:34:54 2019

@author: lealp
"""



def add_background(ax, x0, x1, y0, y1, 
                        facecolor='k', 
                        face_alpha=1,
                        edgecolor='k',
                        edgealpha=1,
                        linewidth=2,
                        transform=None, 
                        background_xpadding=0.5, 
                        background_ypadding=0.2):
    
    from matplotlib.patches import Rectangle
    
    width = (x1 - x0 ) 
    height = (y1 - y0)
    
    Tuple_positioning = (x0  , y0)
    
    rect = Rectangle( Tuple_positioning, -width*background_xpadding, height*background_ypadding, 
                      facecolor=facecolor, 
                      alpha=face_alpha,
                      edgecolor=edgecolor,
                      linewidth=linewidth,
                      transform=transform, zorder=1)
    
    rect2 = Rectangle(Tuple_positioning, -width*background_xpadding, height*background_ypadding, 
                      facecolor=facecolor, 
                      fill=False,
                      alpha=edgealpha,
                      edgecolor=edgecolor,
                      linewidth=linewidth,
                      transform=transform, zorder=1)
    
    ax.figure.patches.extend([rect, rect2])
    
    print("Background bbox x0, y0 setted at: ", Tuple_positioning)
    
    print("Background added to figure")
    
