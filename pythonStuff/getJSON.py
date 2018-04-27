#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 09:30:20 2018
@author: djabernathy
"""

import osmnx as ox
import geopandas as gp
import math
import sys
sys.path.append('/Users/djabernathy/Desktop/Geog5223/g5223project/')
from downhill_slopeforce import *
import json

apiKey = 'AIzaSyAgGQRYnWTzsgf6Xn1DISE99Tdq7Lr9rwU'
saving_directory = 'C:/Users/G5223/Desktop/'

city = 'Milwaukee'
state = 'Wisconsin'
country = 'USA'
network_type = 'drive'
location_string = city + ', ' + state + ', ' + country

filter_list = ['motorway','motorway_link']

filtered_nodes_slow = set() # use set to avoid adding the same node multiple times
filtered_nodes_moderate = set() # nodes are added to these sets as they are found
filtered_nodes_fast = set()

def road_Filter(road, should_filter=True):
    highway_filters = []
    if(should_filter):
        #list your filters here
        highway_filters = filter_list
    for filter_item in highway_filters:
        if road['highway'] == filter_item:
            return False
    return True

# download city street data and elevation data
G = ox.graph_from_place(location_string, network_type= network_type) 
G_elev = ox.add_node_elevations(G, apiKey, max_locations_per_batch=350, pause_duration=0.02)

# iterate through all nodes. Check elevation change between each node's
count = 0
geometry_count = 0
for n in G_elev.nodes():
    for neighbor in G_elev.neighbors(n): # neighbor is a node key
        road = G_elev.get_edge_data(n, neighbor)[0] # road length in meters, right?
        if road_Filter(road): # look up road types for other filters
            #if road['name'] == 'Lane Averue':
             #   print(road)
            # neighbors. keep track of pairs with appropriate elevation change.
            change_elev = G_elev.node[n]['elevation'] - G_elev.node[neighbor]['elevation']

            # checks for change in elevation
            length = road['length']
            skateweight = 150
            TopHill_elevation = 552 #feet
            bottomHill_elevation = 10
            hillHeight = change_elev
            vel = skate_downhill_accel(length, skateweight, hillHeight, gravity=9.8)[2]
            print(vel, length)
            if vel > 3 or vel < -3:
    
                # check for curvature usng the linestring
                road['velocity'] = vel
                if 'geometry' in road.keys():
                    #print(road['geometry'], '\n\n\n\n')
                    print()
   
            else:
                #print(G_elev.get_edge_data(n, neighbor)[0])
                count += 1
        
                # if all conditions are passed, add nodes to set
                if vel < 20:    
                    filtered_nodes_slow.add(n)
                    filtered_nodes_slow.add(neighbor)
                elif vel < 45:    
                    filtered_nodes_moderate.add(n)
                    filtered_nodes_moderate.add(neighbor)
                else:    
                    filtered_nodes_fast.add(n)
                    filtered_nodes_fast.add(neighbor)
                #print(change_elev)

    # graph of the filtered roads
    G_filtered_slow = G_elev.subgraph(filtered_nodes_slow)
    G_filtered_moderate = G_elev.subgraph(filtered_nodes_moderate)
    G_filtered_fast = G_elev.subgraph(filtered_nodes_fast)

#ox.plot_graph(ox.project_graph(G))

#This saves as a shapefile instead of JSON
#ox.save_graph_shapefile(G, filename='Columbus', folder=None, encoding='utf-8')
#ox.save_graph_shapefile(G_filtered, filename='Filtered Roads', folder=None, encoding='utf-8')

# convert graph to GeoDataFrame. And then to JSON
gdfFiltered_slow = ox.graph_to_gdfs(G_filtered_slow, nodes=False, edges=True, node_geometry=True, fill_edge_geometry=True)
geojsonFiltered_slow = gdfFiltered_slow.to_json()

gdfFiltered_moderate = ox.graph_to_gdfs(G_filtered_moderate, nodes=False, edges=True, node_geometry=True, fill_edge_geometry=True)
geojsonFiltered_moderate = gdfFiltered_moderate.to_json()

gdfFiltered_fast = ox.graph_to_gdfs(G_filtered_fast, nodes=False, edges=True, node_geometry=True, fill_edge_geometry=True)
geojsonFiltered_fast = gdfFiltered_fast.to_json()
#geojsonFiltered = json.dumps(geojsonFiltered, sort_keys=True, indent=4)

f = open(saving_directory + city + 'FilteredSlow.js', 'w')
result = 'var milwaukeeFilteredSlow =' + str(geojsonFiltered_slow)
f.write(result)
f.close()

f = open(saving_directory + city + 'FilteredModerate.js', 'w')
result = 'var milwaukeeFilteredModerate =' + str(geojsonFiltered_moderate)
f.write(result)
f.close()

f = open(saving_directory + city + 'FilteredFast.js', 'w')
result = 'var milwaukeeFilteredFast =' + str(geojsonFiltered_fast)
f.write(result)
f.close()
