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
        self.distance = math.sqrt(math.pow((v1.xCoord - v2.xCoord), 2) + math.pow((v1.yCoord - v2.yCoord), 2))


def createEdgeList(vertexList, num):
    edgeList = []
    connectionMatrix = [[False for y in range(num)] for x in range(num)]

    # Should only need to go through the first half of the vertices to
    # create a complete Graph - if it doesn't, just go through the list
    for i in range(len(vertexList)):

        for destination in vertexList:

            # Check if it is the same city, no need to add to list
            if vertexList[i].id == destination.id:
                continue

            elif not connectionMatrix[destination.id][vertexList[i].id]:
                newEdge = Edge(vertexList[i],destination)
                edgeList.append(newEdge)
                connectionMatrix[vertexList[i].id][destination.id] = True
                connectionMatrix[destination.id][vertexList[i].id] = True

    return edgeList

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

    edgeList = createEdgeList(cities,len(cities))

    mergesort(edgeList, 0, len(edgeList)-1, compare_distances)

    tourList = createTour(edgeList,len(cities))

    ###OUTPUT###
    for tour in tourList:
        print ("V1 #: %d" % tour.v1.id)
        print ("V2 #: %d" % tour.v2.id)
        print ("Distance: %d" % tour.distance)
    print("# of cities in tour: %d" % len(tourList))
