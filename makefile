CXX = g++
RM = rm -rf
CXXFLAGS = -std=c++11 -Wall -g -Wno-sign-compare
OBJS =  srcTsp.o
ZIP = tsp.zip

all: tsp

tsp: ${OBJS}
	${CXX} ${OBJS} -o tsp

tsp.o: srcTsp.cpp
	${CXX} ${CXXFLAGS} -c srcTsp.cpp

clean:
	${RM} *o tsp *SYM

run:
	make && ./tsp testIn.txt

zip:
	zip ${ZIP} *.hpp *.cpp data/* makefile *.pdf

valgrind:
	make && valgrind ./tsp --leak-check=full -v

