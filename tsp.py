#!/usr/bin/env python
import timeit
import sys
import math
import random
from mergesort import mergesort


# A Vertex Object
class Vertex(object):

    # The class "constructor"
    def __init__(self, id, x_coord, y_coord):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.degree = 0

    def __repr__(self):
        return self.id


# An Edge Object
class Edge(object):

    # The class "constructor"
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.distance = round(math.sqrt(math.pow((v1.x_coord - v2.x_coord), 2) + math.pow((v1.y_coord - v2.y_coord), 2)), 0)

def create_edge_list(vertex_list):
    """ Creates a list of non redundant edges connecting every vertex to all other vertices
    Our TSP graph is undirected, so one edge is enough to represent the connection
    between two vertices.
    """
   
    edge_list = []
    num = len(vertex_list)
  
    connection_matrix = [[False for y in range(num)] for x in range(num)]
 
    for start in vertex_list:
        for destination in vertex_list:

            # Check if it is the same city, no need to add to list
            if start.id == destination.id:
                continue

            elif not connection_matrix[destination.id][start.id]:
                new_edge = Edge(start, destination)
                edge_list.append(new_edge)
                connection_matrix[start.id][destination.id] = True
                connection_matrix[destination.id][start.id] = True 

    return edge_list

def distance_comparator(x, y):
    """Used in mergesort to compare two cities"""
    return x.distance <= y.distance

def does_create_cycle(tour_list, new_edge=None):
    """Determines if a cycle has been or will be created"""
    if not new_edge:
        new_edge = current_e = tour_list[0]
        current_v = current_e.v1
        tour_list = tour_list[1:]

    else:
        current_v = new_edge.v1
        current_e = new_edge

    done = False

    while not done:
        found = False
        for edge in tour_list:
            if edge == current_e:
                continue
            if edge.v1 == current_v or edge.v2 == current_v:
                found = True
                if edge.v1 == current_v:
                    current_v = edge.v2
                else:
                    current_v = edge.v1
                current_e = edge
                break
        if not found:
            return False
        else:
            if current_e.v1 == new_edge.v2 or current_e.v2 == new_edge.v2:
                 return True

def create_tour(edge_list, num_cities):
    tour_list = []

    for edge in edge_list:
        if edge.v1.degree < 2 and edge.v2.degree < 2:

            has_cycle = does_create_cycle(tour_list, edge)

            should_go_home = len(tour_list) + 1 == num_cities
            
            if not has_cycle or (has_cycle and should_go_home):
                edge.v1.degree += 1
                edge.v2.degree += 1
                tour_list.append(edge)

    return tour_list

def get_distance(v1, v2):
    """Compute distance between two vertices"""
    return round(math.sqrt(math.pow((v1.x_coord - v2.x_coord), 2) + math.pow((v1.y_coord - v2.y_coord), 2)))

def edge_swap_odd_even(e1, e2):
    """Swaps vertices so odds are connected and evens are connected"""
    temp = e1.v2
    e1.v2 = e2.v1
    e2.v1 = temp
    e1.distance = get_distance(e1.v1, e1.v2)
    e2.distance = get_distance(e2.v1, e2.v2)

def edge_swap_inside_outside(e1, e2):
    """Swaps vertices so inside vertices are connected to outside vertices"""
    temp = e1.v2
    e1.v2 = e2.v2
    e2.v2 = temp
    e1.distance = get_distance(e1.v1, e1.v2)
    e2.distance = get_distance(e2.v1, e2.v2)

def two_opt(tour_list, edge_list, start_time):
    """Uses a 2-opt approach to optimize original tour"""     
    current_time = timeit.default_timer()
    i = 0

    # Only run optimizations while under time limit
    while (current_time - start_time) * 1000 < 140000 and i < len(tour_list):
        # Randomly choose two edges to swap
        edge1 = tour_list[len(tour_list) - 1 - i]
        edge2 = tour_list[len(tour_list) - i - 2]
        v1 = edge1.v1
        v2 = edge1.v2
        v3 = edge2.v1
        v4 = edge2.v2

        target_distance = edge1.distance + edge2.distance
        
        # Check that a vertex in one edge is not also in other edge
        if v1 != v3 and v1 != v4 and v2 != v3 and v2 != v4:
            # Compute possible swap distances
            odd_even = get_distance(v1, v3) + get_distance(v2, v4)
            inside_outside = get_distance(v2, v3) + get_distance(v1, v4)

            # Take better swap if its distance is smaller than target_distance
            if odd_even < inside_outside and odd_even < target_distance:
                edge_swap_odd_even(edge1, edge2)

                # A cycle is not created, reset and restart
                if not does_create_cycle(tour_list):
                    edge_swap_odd_even(edge1, edge2)
            
            elif inside_outside < target_distance:
                edge_swap_inside_outside(edge1, edge2)

                # A cycle is not created, reset and restart
                if not does_create_cycle(tour_list):
                    edge_swap_inside_outside(edge1, edge2)
                            
        i += 1
        current_time = timeit.default_timer()
         
    return tour_list

def write_tour(o, tour_list):
    """Adds tour in order to output file, skipping first city when listed at end"""
    o.write('%i\n' % tour_list[0].v1.id)
    o.write('%i\n' % tour_list[0].v2.id)
    search_city = tour_list[0].v2
    tour_list = tour_list[1:len(tour_list) - 1]

    i = 0

    for edge in tour_list:
        if edge.v1.id == search_city.id:
            'Entered if'
            o.write('%i\n' % edge.v2.id)
            search_city = edge.v2
        elif edge.v2.id == search_city.id:
            o.write('%i\n' % remaining_edge.v1.id)
            search_city = remaining_edge.v1
    o.close()

def print_checks(run_time, distance):
    print 'Runtime in milliseconds is: ', run_time * 1000
    print 'Runtime in seconds is: ', run_time

    if sys.argv[1] == 'tests/tsp_example_1.txt':
        print 'Optimal distance is: ', 108159
        print 'Our distance is: ', distance
        print 'Ratio is: ', distance / 108159

    elif sys.argv[1] == 'tests/tsp_example_2.txt':
        print 'Optimal distance is: ', 2579
        print 'Our distance is: ', distance
        print 'Ratio is: ', distance / 2579

    elif sys.argv[1] == 'tests/tsp_example_3.txt':
        print 'Optimal distance is: ', 1573084
        print 'Our distance is: ', distance
        print 'Ratio is: ', distance / 1573084

    else:
        print 'Our distance is: ', distance

# Driver Code
if __name__ == '__main__':
    start_time = timeit.default_timer()  
    cities = []

    with open(sys.argv[1], 'r') as f:
        # Get our input
        for line in f:
            item = line.split()
    
            for i in range(len(item)):                    
                item[i] = int(item[i])
    
            id = item[0]
            x_coord = item[1]
            y_coord = item[2]
            new_city = Vertex(id, x_coord, y_coord)
            cities.append(new_city)
    
        f.close()

    edge_list = create_edge_list(cities)
    mergesort(edge_list, comparator=distance_comparator)
    tour_list = create_tour(edge_list, len(cities))

    # Checks if we are under 3 minutes to continue optimization
    # Leaving 40 seconds to write to the file (this number can be changed)
    time_check = timeit.default_timer()
    if (time_check - start_time) * 1000 < 140000:
        tour_list = two_opt(tour_list, edge_list, start_time)

    # Calculate new distance
    distance = 0
    for each in tour_list:
        distance += each.distance

    # Currently broken - Write to output file
    # with open(sys.argv[1] + '.tour', 'w') as o:
    #     o.write('%i\n' % distance)
    #     write_tour(o, tour_list)

    end_time = timeit.default_timer()
    run_time = (end_time - start_time)
    print_checks(run_time, distance)
