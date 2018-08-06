#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:05:59 2018
This class creates maps of earthquakes and seismic stations from SQL database. 

@author: mostafamousavi
"""
import sqlite3
import plotly.plotly as py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.cm as cm
from pylab import rcParams
rcParams['figure.figsize'] = (8,6)



class eq_mapper():
     ''' This class generates maps of earthquakes and stations from a 
     sql database'''
     
     def __init__(self, fname):
         self.read_data(fname)
         self.make_map()
         
     def read_data(self, fname): 
        def read_large_file(file_object):
            while True:
                data = file_object.readline()
                if not data:
                    break
                yield data 
                
        def get_marker_color(depth):
            # Returns green for small earthquakes, yellow for moderate
            #  earthquakes, and red for significant earthquakes.
            if depth <= 10.0:
                return ('deeppink')
            elif 10 < depth and depth <= 50.0:
                return ('m')
            elif 50 < depth and depth <= 100.0:
                return ('orchid')
            elif 100 < depth and depth <= 300.0:
                return ('orangered')
            elif 300 < depth:
                return ('orange')            
                
        conn = sqlite3.connect(fname)
        cur = conn.cursor()
        outT = pd.read_sql_query("SELECT station_lat,station_lon,event_lat,\
                                 event_lon,event_depth,magnitude FROM "+fname+" ", conn)
        outT.to_csv('./temp_csv')
        del outT
        
        # Create empty lists for the data we are interested in.
        self.slats, self.slons = [], []
        self.evlats, self.evlons = [], []
        self.color = []
        self.msize = []
        
        # Store the latitudes and longitudes in the appropriate lists.
        f = open('./temp_csv') 
        for rowcat in read_large_file(f):
            rowcat = rowcat.split(',')   
            if rowcat[1] != 'station_lat':
                self.slats.append(float(rowcat[1]))
                self.slons.append(float(rowcat[2]))
                self.evlats.append(float(rowcat[3]))
                self.evlons.append(float(rowcat[4]))
                self.color.append(get_marker_color(float(rowcat[5])))
                s = (float(rowcat[6])/10) * 400
                self.msize.append(s)
                
     def make_map(self):        
        # --- Build Map ---
#        m = Basemap(llcrnrlon=-180,llcrnrlat=-60,urcrnrlon=180.,urcrnrlat=80.,
#                     resolution='c', projection='merc', lat_0 = 0., lon_0 = 0.)        
        # parallels = np.arange(-80., 90, 30)
        # meridians = np.arange(0., 360., 30)
        # lw = 1
        # dashes = [5,7] # 5 dots, 7 spaces... repeat
        # graticules_color = 'grey'
        # =============================================================================
        
        m = Basemap(llcrnrlon=min(self.evlons)-5,llcrnrlat=min(self.evlats)-5,
        urcrnrlon=max(self.evlons)+5, urcrnrlat=max(self.evlats)+5,
        resolution='c', projection='merc', lat_0 = 0, lon_0 = 0)  
        
        fig1 = plt.figure(figsize=(10,12))
        fig1.patch.set_facecolor('#e6e8ec')
        ax = fig1.add_axes([0.1,0.1,0.8,0.8])
        
# =============================================================================
#         m.drawmapboundary(color='white', 
#                           linewidth=0.0, 
#                           fill_color='white')
#         #m.drawparallels(parallels, 
#         #                linewidth=lw, 
#         #                dashes=dashes, 
#         #                color=graticules_color)
#         #m.drawmeridians(meridians, 
#         #                linewidth=lw, 
#         #                dashes=dashes, 
#         #                color=graticules_color)
#         m.drawcoastlines(linewidth=0.5,
#                          linestyle='solid', 
#                          color='black')
#         m.fillcontinents('gainsboro', 
#                          lake_color='white')
#         m.drawcountries(linewidth=0.5, 
#                         linestyle='solid', 
#                         color='black', 
#                         zorder=30)
#         m.readshapefile('./tectonicplates-master/PB2002_plates', 
#                         name='tectonic_plates', 
#                         drawbounds=True, 
#                         color='r')      
# =============================================================================        
        m.drawcoastlines()
        m.shadedrelief()
        m.readshapefile('st99_d00', name='states', drawbounds=True)

        title = plt.title('Earthquake Map '+str(len(self.evlons)), 
                          fontsize=20) 
        title.set_y(1.03) # Move the title a bit for niceness
        
        x1, y1 = m(self.evlons, self.evlats) # Convert coords to projected place in figure
        
        m.scatter(x1, y1, s=self.msize, c= self.color, marker = 'o', cmap=cm.cool, alpha = 0.8)
        l0 = plt.scatter([],[], s=4, c= 'b', edgecolors='none')
        l1 = plt.scatter([],[], s=20, c= 'b', edgecolors='none')
        l2 = plt.scatter([],[], s=40, c= 'b', edgecolors='none')
        l3 = plt.scatter([],[], s=100, c= 'b', edgecolors='none')
        l4 = plt.scatter([],[], s=200, c= 'b', edgecolors='none')
        
        labels = ["0.1", "0.5", "1.0", "2.5", "5.0"]
        leg1 = plt.legend([l0, l1, l2, l3, l4], labels, ncol=1, frameon=True, fontsize=12,
        handlelength=1.5, loc='upper center', bbox_to_anchor=(1.2, 0.5),
        fancybox=True, shadow=True,title='Magnitude')   
        
        d0 = plt.scatter([],[], s=100, c= 'deeppink', edgecolors='none')
        d1 = plt.scatter([],[], s=100, c= 'm', edgecolors='none')
        d2 = plt.scatter([],[], s=100, c= 'orchid', edgecolors='none')
        d3 = plt.scatter([],[], s=100, c= 'orangered', edgecolors='none')
        d4 = plt.scatter([],[], s=100, c= 'orange', edgecolors='none')
        
        lab = ["Depth <= 10 km", "10 < Depth <= 50 km", 
               "50 < Depth <= 100 km", "100 < Depth <= 300 km", "300 < Depth"]
        leg2 = plt.legend([d0, d1, d2, d3, d4], lab, ncol=1, frameon=True, fontsize=12,
        handlelength=1.5, loc='center left', bbox_to_anchor=(1, 0.8),
        fancybox=True, shadow=True,title='Depth')
        
        plt.gca().add_artist(leg1)
        
        plt.show()    



        m = Basemap(llcrnrlon=min(self.slons)-5,llcrnrlat=min(self.slats)-5,
        urcrnrlon=max(self.slons)+5, urcrnrlat=max(self.slats)+5,
        resolution='c', projection='merc', lat_0 = 0, lon_0 = 0)  
        
        fig1 = plt.figure(figsize=(10,12))
        fig1.patch.set_facecolor('#e6e8ec')
        ax = fig1.add_axes([0.1,0.1,0.8,0.8])

        m.drawcoastlines()
        m.shadedrelief()
        m.readshapefile('st99_d00', name='states', drawbounds=True)

        title = plt.title('Station Map', 
                          fontsize=20) 
        title.set_y(1.03) # Move the title a bit for niceness
        
        x1, y1 = m(self.slons, self.slats) # Convert coords to projected place in figure
        
        m.scatter(x1, y1, s=50, c= 'b', marker = '^', cmap=cm.cool, alpha = 0.8)



eq_mapper("comcat_phase_sql") 


