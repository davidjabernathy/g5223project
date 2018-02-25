#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 09:30:20 2018

@author: djabernathy
"""

import osmnx as ox
import math

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
            if change_elev > 5 or change_elev < -5:
                
                # check for curvature usng the linestring
                
                if 'geometry' in road.keys():
                    print(road['geometry'], '\n\n\n\n')
                                      
                    
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