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

apiKey = 'AIzaSyAgGQRYnWTzsgf6Xn1DISE99Tdq7Lr9rwU'

def angle_of_hill(elev_change, distance):
    angle = math.atan(elev_change/distance)
    return angle

def down_slope_force(mass, elev_change, distance):
    gravity = 9.8
    air_friction = 0   
    angle = angle_of_hill(elev_change, distance)
    return mass * angle * (gravity - air_friction)

# download city street data.
G = ox.graph_from_place('Columbus, Ohio, USA', network_type='drive')

# add elevation data.
G_elev = ox.add_node_elevations(G, apiKey, max_locations_per_batch=350, pause_duration=0.02)

# iterate through all nodes. Check elevation change between each node's
count = 0
geometry_count = 0
filtered_nodes = set() # use set to avoid adding the same node multiple times
for n in G_elev.nodes():
    for neighbor in G_elev.neighbors(n): # neighbor is a node key
        road = G_elev.get_edge_data(n, neighbor)[0] # road length in meters, right?
        if road['highway'] != 'motorway': # look up road types for other filters
            #if road['name'] == 'Lane Averue':
             #   print(road)
            # neighbors. keep track of pairs with appropriate elevation change.
            change_elev = G_elev.node[n]['elevation'] - G_elev.node[neighbor]['elevation']
            
            # just checking for amount of change now. Later use elevation change and road distance
            # to get possible speed
            if change_elev > 1 or change_elev < -1:
                
                # just checking for amount of change now. Later use elevation change and road distance
                # to get possible speed
                length = road['length']
                skateweight = 150
                TopHill_elevation = 552 #feet
                bottomHill_elevation = 10
                hillHeight = change_elev
                vel = skate_downhill_accel(length, skateweight, hillHeight, gravity=9.8)[2]
                print(vel, length)
                if vel > 5 or vel < -5:
                    
                    # check for curvature usng the linestring
                    
                    if 'geometry' in road.keys():
                        #print(road['geometry'], '\n\n\n\n')
                        print()
                                          
                        
                    # some edges don't have a geometry. How do we handle these?
                    # do they mean they are relatively straight and don't need a more complex geometry?
                    # do they just not have all the data?
                    else:
                        #print(G_elev.get_edge_data(n, neighbor)[0])
                    
                        count += 1

                     
                    # do other types of filtering
                     
                    # if all conditions are passed, add nodes to set
                    filtered_nodes.add(n)
                    filtered_nodes.add(neighbor)
                    #print(change_elev)
            
    # graph of the filtered roads
    G_filtered = G_elev.subgraph(filtered_nodes)

print(len(filtered_nodes))


ox.plot_graph(ox.project_graph(G_filtered))
ox.save_graph_shapefile(G, filename='Columbus', folder=None, encoding='utf-8')
ox.save_graph_shapefile(G_filtered, filename='Filtered Roads', folder=None, encoding='utf-8')

# convert graph to GeoDataFrame. And then to JSON
gdfFiltered = ox.graph_to_gdfs(G_filtered, nodes=False, edges=True, node_geometry=True, fill_edge_geometry=True)
geojsonFiltered = gdfFiltered.to_json()
geojsonFiltered = json.dumps(geojsonFiltered, sort_keys=True, indent=4)

gdf = ox.graph_to_gdfs(G_elev, nodes=False, edges=True, node_geometry=True, fill_edge_geometry=True)
geojson = gdf.to_json()



