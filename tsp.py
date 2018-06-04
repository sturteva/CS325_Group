#!/usr/bin/env python

import sys
import math
from mergesort import mergesort

# A Vertex Object
class Vertex(object):

    # The class "constructor"
    def __init__(self, id, xCoord, yCoord):
        self.id = id
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.degree = 0


# An Edge Object
class Edge(object):

    # The class "constructor"
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.distance = int(round(math.sqrt(math.pow((v1.xCoord - v2.xCoord), 2) + math.pow((v1.yCoord - v2.yCoord), 2))))


# A Tour Object
class Tour(object):

    #The class "constructor"
    def __init__(self):
        self.distance = 0
        self.city_list = []


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


def compare_distances(x, y):
    return x.distance <= y.distance


def create_tour(edge_list):
    tour = Tour()
    num = len(edge_list)
    for edge in edge_list:

        # Check degree of both vertices
        if edge.v1.degree >= 2 or edge.v2.degree >= 2:
            continue

        else:
            if len(tour.city_list) == num:
                break
            else:
                tour.city_list.append(edge)
                edge.v1.degree += 1
                edge.v2.degree += 1
                tour.distance += edge.distance

    return tour


def print_tour(tour, current_edge):
    print current_edge.v1.id
    for remaining_edge in tour.city_list:
        if remaining_edge.v1.id == current_edge.v2.id:
            tour.city_list.remove(remaining_edge)
            print_tour(tour, remaining_edge)
            break


def create_fake_tour():
    tour = Tour()
    tour.distance = 5
    vertex_one = Vertex(1, 0, 100)
    vertex_two = Vertex(2, 500, 400)
    vertex_three = Vertex(3, 300, 200)
    vertex_four = Vertex(4, 200, 800)
    edge_one = Edge(vertex_one, vertex_two)
    edge_two = Edge(vertex_two, vertex_four)
    edge_three = Edge(vertex_four, vertex_three)
    edge_four = Edge(vertex_three, vertex_one)
    tour.city_list = [edge_one, edge_two, edge_three, edge_four]


# Driver Code
if __name__ == '__main__':
    cities = []
    f = open(sys.argv[1], 'r')

    # Get our Input
    for line in f:
        item = line.split(' ')

        for i in range(len(item)):
            item[i] = int(item[i])

        temp_number = item[0]
        temp_x_coord = item[1]
        temp_y_coord = item[2]
        new_city = Vertex(temp_number, temp_x_coord, temp_y_coord)
        cities.append(new_city)

    f.close()

    edge_list = create_edge_list(cities)

    mergesort(edge_list, 0, len(edge_list)-1, compare_distances)

    tour = create_tour(edge_list)
    # tour = create_fake_tour()

    ###OUTPUT###
    print 'Total Distance: ', tour.distance
    current_edge = tour.city_list[0]
    tour.city_list.remove(current_edge)
    print_tour(tour, current_edge)
