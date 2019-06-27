# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:49:21 2019

@author: lealp
"""


from matplotlib import ticker


class axes_tick_formatter(object):
    
    def format_axis_ticks_to_scientific_notation(ax, axis='both', decimal_separator='.'):
         
         ##################################     
         def value_to_scientific(x):
             return '{:2.2e}'.format(x)
        

         def axis_fmt(x, y, decimal_separator=decimal_separator):
        
             v1, v2 = value_to_scientific(x).split('e')
            
             v1 = v1.replace('.', decimal_separator)
        
             return r'${0} \times 10^{{{1}}}$'.format(v1, v2) if x !=0 else '0'
    
    
         ###################################
     
       
         
         if axis.lower() == 'both':
             
             axis = ['xaxis', 'yaxis']
            
             for i_axis in axis:
                 Axis = getattr(ax, i_axis)
                 Axis.set_major_formatter(ticker.FuncFormatter(axis_fmt))
            
         else:
            
             Axis = getattr(ax, axis)
             Axis.set_major_formatter(ticker.FuncFormatter(axis_fmt))
    

    def set_number_of_ticks_for_given_axis(axes, n_ticks, axis='both'):
        
         if axis.lower() == 'both':
             axes.xaxis.set_major_locator(ticker.MaxNLocator(n_ticks))
        
             axes.yaxis.set_major_locator(ticker.MaxNLocator((n_ticks)))
            
         elif axis.lower() == 'x':
             axes.xaxis.set_major_locator(ticker.MaxNLocator((n_ticks)))
        
         elif axis.lower()=='y':
             axes.yaxis.set_major_locator(ticker.MaxNLocator((n_ticks)))
            
         elif axis.lower() == 'z':
             if hasattr(axes, 'zaxis'):
                 axes.zaxis.set_major_locator(ticker.MaxNLocator((n_ticks)))
                
         else:
             None
             

    def change_axes_tick_decimal_separator(ax, gridline_tick_formating='.2f', axis='both', decimal_separator=','):  
         
         def Format_p(x, counter):
            
             return '{0:{1}}'.format(x, gridline_tick_formating).replace('.', decimal_separator)
         
         if axis.lower() == 'both':
     
             axis = ['xaxis', 'yaxis']
    
             for i_axis in axis:
                 Axis = getattr(ax, i_axis)
                 Axis.set_major_formatter(ticker.FuncFormatter(Format_p))
                 
         else:
            
             Axis = getattr(ax, axis)
             Axis.set_major_formatter(ticker.FuncFormatter(Format_p))
        
        
         return ax
    

    def set_ticks_in_axes(ax, 
                  axis='both', 
                  which='major', 
                  labelpad=10, 
                  labelrotation=90, 
                  labelsize=12,
                  labelcolor='k',
                  ticksize=10,
                  length=1.0,
                  width=0.2,
                  tick_color='k',
                  bottom=True,
                  left=True,
                  right=False,
                  top=False,
                  direction='out',
                  grid_color='k',
                  grid_alpha=0.5,
                  grid_linewidth=0.2,
                  grid_linestyle='-'
                  ):
        
        
         '''
        
         standard matplotlib function for setting ticks in given Axes.
        
         Parameters:
        
            
             axis: ['x', 'y', 'both']
             which: ['major', 'minor', 'both'] - defines the tick that the function will be applied
             labelpad: pad of the label
             labelrotation: for standard it is 90
             labelsize: size of the labels
             ticksize: the size of the ticks
             
             ticksize: the size of the tick lines
             bottom, top, right, left: allows or denies the tick and ticklabel plotting for that given axis direction
             
             direction : ['in', 'out', 'inout']
                     Puts ticks inside the axes, outside the axes, or both
                    
             length : float
                 Tick length in points
                
             width : float
                 Tick width in points.
                
         Returns:
            
             axes
            
         '''
        
         ax.tick_params(axis=axis, 
                      which = which, 
                      pad = labelpad, 
                      rotation=labelrotation,
                      size = ticksize, 
                      color = tick_color,
                      length=length,
                      width=width,
                      labelsize = labelsize,
                      labelcolor = labelcolor,
                      
                      bottom = bottom,
                      left = left,
                      right = right,
                      top = top,
                      direction = direction,
                      grid_color = grid_color,
                      grid_alpha = grid_alpha,
                      grid_linewidth = grid_linewidth,
                      grid_linestyle = grid_linestyle)
        
         return ax
    
    