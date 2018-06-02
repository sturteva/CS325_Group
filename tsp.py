#!/usr/bin/env python

import sys
import math

#A Vertex Object
class Vertex(object):
	
	#The class "constructor"
	def __init__(self, number,xCoord,yCoord):
		self.number = number
		self.xCoord = xCoord
		self.yCoord = yCoord
		self.degree = 0
		self.visited = False

def make_vertex(number,xCoord,yCoord):
	vertex = Vertex(number,xCoord,yCoord)
	return vertex

#An Edge Object
class Edge(object):

	#The class "constructor"
	def __init__(self,v1,v2): 
		self.v1 = v1
		self.v2 = v2
		self.distance = math.sqrt(math.pow((v1.xCoord - v2.xCoord),2) + math.pow((v1.yCoord - v2.yCoord),2))


def make_edge(v1,v2):
	edgeList = []
	edge = Edge(v1,v2)
	return edge

def createEdgeList(vertexList,num):

	edgeList = []
	connectionMatrix =[[False for y in range(num)] for x in range(num)] 

	#Should only need to go through the first half of the vertices to
	#create a complete Graph - if it doesn't, just go through the list
	for i in range(len(vertexList)):

		for destination in vertexList:

			#Check if it is the same city, no need to add to list
			if  vertexList[i].number == destination.number:
				continue

			elif not connectionMatrix[destination.number][vertexList[i].number]:
				newEdge = make_edge(vertexList[i],destination)
				edgeList.append(newEdge)
				connectionMatrix[vertexList[i].number][destination.number] = True
				connectionMatrix[destination.number][vertexList[i].number] = True
				
	return edgeList


# Merges two subarrays of arr[].
def merge(arr, leftIndex, middle, rightIndex):
        sizeOne = middle - leftIndex + 1
        sizeTwo = rightIndex - middle

        # create temp arrays
        leftTemp = [0] * (sizeOne)
        rightTemp = [0] * (sizeTwo)

        # Copy data to temp arrays L[] and R[]
        for i in range(0 , sizeOne):
                leftTemp[i] = arr[leftIndex + i]

        for j in range(0 , sizeTwo):
                rightTemp[j] = arr[middle + 1 + j]

        # Merge the temp arrays back into arr..r]
        i = 0
        j = 0
        k = leftIndex

        while i < sizeOne and j < sizeTwo :
                if leftTemp[i].distance <= rightTemp[j].distance:
                        arr[k] = leftTemp[i]
                        i += 1
                else:
                        arr[k] = rightTemp[j]
                        j += 1
                k += 1

        # Copy the remaining elements of L[], if there
        # are any
        while i < sizeOne:
                arr[k] = leftTemp[i]
                i += 1
                k += 1

        # Copy the remaining elements of R[], if there
        # are any
        while j < sizeTwo:
                arr[k] = rightTemp[j]
                j += 1
                k += 1


def mergesort(arr,leftIndex,rightIndex):
	if leftIndex < rightIndex:

		#samee as (l+r)/2, but avoids overflow for
	        # large l and h
        	middle = (leftIndex+(rightIndex-1))/2

	        # Sort first and second halves
	        mergesort(arr, leftIndex, middle)
	        mergesort(arr, middle+1, rightIndex)
	        merge(arr, leftIndex, middle, rightIndex)


def createTour(edgeList,num):
	
	tourList = []
	tourDistance = 0
	for each in edgeList:
	
		#check degree of both vertices
		if each.v1.degree >= 2 | each.v2.degree >= 2 :
			continue

		else:
			if len(tourList) == num:
				break
			else:
				tourList.append(each)
				each.v1.visited = True
				each.v2.visited = True	
				each.v1.degree += 1
				each.v2.degree += 1
				tourDistance += each.distance

	print(tourDistance)
	return tourList

#Driver Code

cities = []
f = open(sys.argv[1],"r")

#Get our Input
for line in f:
	item = line.split(' ')

	for i in range(len(item)):
		item[i] = int(item[i])

	tempNumber = item[0]
	tempX_Coord = item[1]
	tempY_Coord = item[2]
	newCity = make_vertex(tempNumber,tempX_Coord,tempY_Coord)
	cities.append(newCity)

edgeList = createEdgeList(cities,len(cities))

mergesort(edgeList,0,len(edgeList)-1)

tourList = createTour(edgeList,len(cities))

###OUTPUT###
for each in tourList:
	print ("V1 #: %d" % each.v1.number)
	print ("V2 #: %d" % each.v2.number)
	print ("Distance: %d" % each.distance)
print("# of cities in tour: %d" % len(tourList))
