#!/usr/bin/env python

import sys
import math
from mergesort import mergesort


# A Vertex Object
class Vertex(object):

    # The class "constructor"
    def __init__(self, id, x_coord, y_coord):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.degree = 0

# An Edge Object
class Edge(object):

    # The class "constructor"
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.distance = int(round(math.sqrt(math.pow((v1.x_coord - v2.x_coord), 2) + math.pow((v1.y_coord - v2.y_coord), 2))))


def create_edge_list(vertex_list):
    """ Creates a list of non redundant egdes connecting every vertex to other all vertices
    Our TSP graph is undirected, so one edge is enough to represent the connection
    between two vertices.
    """
    edge_list = []
    num = len(vertex_list)
    connection_matrix = [[False for y in range(num)] for x in range(num)]

    # TODO: Should only need to go through the first half of the vertices to
    # create a complete Graph
    # For instance, you won't need edge (A, B) & (B, A)
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


def does_create_cycle(tour_list, new_edge):
    """Finds whether there exists a cycle with the added new_edge"""
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
    distance = 0

    for edge in edge_list:
        if edge.v1.degree < 2 and edge.v2.degree < 2:

            has_cycle = does_create_cycle(tour_list, edge)
            should_go_home = len(tour_list) + 1 == num_cities

            if not has_cycle or (has_cycle and should_go_home):
                edge.v1.degree += 1
                edge.v2.degree += 1
                distance += edge.distance
                tour_list.append(edge)

    return tour_list, distance


def print_tour(o, tour_list, current_edge, search_city):
    """Adds tour in order to output file, skipping first city when listed at end"""
    o.write('%i\n' % search_city.id)
    while (len(tour_list) > 1):
        for remaining_edge in tour_list:
            if remaining_edge.v1.id == search_city.id:
                tour_list.remove(remaining_edge)
                print_tour(o, tour_list, remaining_edge, remaining_edge.v2)
                break
            elif remaining_edge.v2.id == search_city.id:
                tour_list.remove(remaining_edge)
                print_tour(o, tour_list, remaining_edge, remaining_edge.v1)
                break
    

# Driver Code
if __name__ == '__main__':
    cities = []
    f = open(sys.argv[1], 'r')

    # Get our Input
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
    tour_list, distance = create_tour(edge_list, len(cities))

    # Print output
    with open(sys.argv[1] + '.tour', 'w') as o:
        o.write('%i\n' % distance)
        current_edge = tour_list[0]
        o.write('%i\n' % current_edge.v1.id)
        tour_list.remove(current_edge)
        print_tour(o, tour_list, current_edge, current_edge.v2)
