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
        self.visited = False


# An Edge Object
class Edge(object):

    # The class "constructor"
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.distance = int(round(math.sqrt(math.pow((v1.xCoord - v2.xCoord), 2) + math.pow((v1.yCoord - v2.yCoord), 2))))


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

def createTour(edgeList, num):
    tourList = []
    tourDistance = 0
    for edge in edgeList:

        # Check degree of both vertices
        if edge.v1.degree >= 2 or edge.v2.degree >= 2:
            continue

        else:
            if len(tourList) == num:
                break
            else:
                tourList.append(edge)
                edge.v1.visited = True
                edge.v2.visited = True
                edge.v1.degree += 1
                edge.v2.degree += 1
                tourDistance += edge.distance

    print(tourDistance)
    return tourList

# Driver Code
if __name__ == '__main__':
    cities = []
    f = open(sys.argv[1], 'r')

    # Get our Input
    for line in f:
        item = line.split(' ')

        for i in range(len(item)):
            item[i] = int(item[i])

        tempNumber = item[0]
        tempX_Coord = item[1]
        tempY_Coord = item[2]
        newCity = Vertex(tempNumber, tempX_Coord, tempY_Coord)
        cities.append(newCity)

    f.close()

    edgeList = create_edge_list(cities)

    mergesort(edgeList, 0, len(edgeList)-1, compare_distances)

    tourList = createTour(edgeList,len(cities))

    ###OUTPUT###
    for tour in tourList:
        print ("V1 #: %d" % tour.v1.id)
        print ("V2 #: %d" % tour.v2.id)
        print ("Distance: %d" % tour.distance)
    print("# of cities in tour: %d" % len(tourList))
