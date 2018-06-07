#include <iostream>
#include <fstream>
#include <string.h>
#include <cmath>
#include <vector>
#include <sstream>
#include <locale>


using namespace std;

class Vertex {
private:
    int id;
    int xCoord;
    int yCoord;
    int degree;
public:
    Vertex(int _id, int _xCoord, int _yCoord) {
        id = _id;
        xCoord = _xCoord;
        yCoord = _yCoord;
        degree = 0;
    };

    ~Vertex(){};

    int getId() {
        return id;
    }

    int getXCoord() {
        return xCoord;
    }

    int getYCoord() {
        return yCoord;
    }

    int getDegree(){
	return degree;
    }

    void upDegree(){
	degree++;
    }

    void display() {
        cout << "id: " << id << ", x: " << xCoord << ", y: " << yCoord << endl;
    }
};

class Edge {
private:
    Vertex *v1;
    Vertex *v2;
    int distance;
public:
    Edge(Vertex *_v1, Vertex *_v2) {
        v1 = _v1;
        v2 = _v2;
        distance = round(sqrt(pow(v1->getXCoord() - v2->getXCoord(), 2) + pow(v1->getYCoord() - v2->getYCoord(), 2)));
    };
    ~Edge() {}
    
    Vertex* getV1(){
	return v1;
    }

    Vertex* getV2(){
	return v2;
    }

    int getDistance() {
        return distance;
    }

    void display() {
        cout << "v1.id: " << v1->getId()  << ", v2.id: " << v2->getId() << ", distance: " << distance << endl;
    }
};

void _merge(vector<Edge*>*arr, int leftIndex, int middle, int rightIndex) {
    int sizeOne,
        sizeTwo,
        i, j, k;
    vector<Edge*> leftTemp;
    vector<Edge*> rightTemp;

    sizeOne = middle - leftIndex + 1;
    sizeTwo = rightIndex - middle;

    for (i = 0; i < sizeOne; i++) {
        leftTemp.push_back((*arr)[leftIndex + i]);
    }

    for (j = 0; j < sizeTwo; j++) {
        rightTemp.push_back((*arr)[middle + 1 + j]);
    }

    i = 0;
    j = 0;
    k = leftIndex;

    while (i < sizeOne && j < sizeTwo) {
        if (leftTemp[i]->getDistance() <= rightTemp[j]->getDistance()) {
            (*arr)[k++] = leftTemp[i++];
        } else {
            (*arr)[k++] = rightTemp[j++];
        }
    }

    while (i < sizeOne) {
        (*arr)[k++] = leftTemp[i++];
    }

    while (j < sizeTwo) {
        (*arr)[k++] = rightTemp[j++];
    }
}

void _mergesort(vector<Edge*>*arr, int leftIndex, int rightIndex) {
    int middle;

    if (leftIndex < rightIndex) {
        middle = (leftIndex + (rightIndex - 1)) / 2;

        _mergesort(arr, leftIndex, middle);
        _mergesort(arr, middle + 1, rightIndex);
        _merge(arr, leftIndex, middle, rightIndex);
    }
}

void mergesort(vector<Edge*> *arr) {
    _mergesort(arr, 0 , arr->size() - 1);
}

vector<Edge*> createEdgeList(vector<Vertex*> cities) {

    vector<Edge*> edgeList;
    int numCities = cities.size();
    int **connectionMatrix = new int*[numCities];
    int i, j;

    // initialize connection matric
    for (i = 0; i < numCities; i++) {
        connectionMatrix[i] = new int[numCities];
    }
    for (i = 0; i < numCities; i++) {
        for (j = 0; j < numCities; j++) {
            connectionMatrix[i][j] = 0;
        }
    }

    // calculate edges based on passed cities
    for (auto start = cities.begin(); start != cities.end(); ++start) {


        for (auto destination = cities.begin(); destination != cities.end(); ++destination) {

            if ((*start)->getId() == (*destination)->getId()) {

                continue;
            } 
		
	    else if (connectionMatrix[(*destination)->getId()][(*start)->getId()] == 0) {

                Edge *e = new Edge((*start), (*destination));

                edgeList.push_back(e);

                connectionMatrix[(*start)->getId()][(*destination)->getId()] = 1;

                connectionMatrix[(*destination)->getId()][(*start)->getId()] = 1;
            }
        }
    }


    // cleanup
    for (i = 0; i < numCities; i++) {
        delete[] connectionMatrix[i];
    }
    delete[] connectionMatrix;

    return edgeList;
}


//Used Master Branch version for now
bool does_create_cycle(vector<Edge*> tour_list, Edge* new_edge){

	Vertex* current_v = new_edge->getV1();
	Edge* current_e = new_edge;
	
	bool done = false;

	while(!done){
		
		bool found = false;

		for(auto start = tour_list.begin(); start != tour_list.end(); ++start){
	
			if((*start) == current_e)
				continue;
			
			if((*start)->getV1() == current_v || (*start)->getV2() == current_v){
				found = true;
				if((*start)->getV1() == current_v)
					current_v = (*start)->getV2();

				else
					current_v = (*start)->getV1();
				current_e = (*start);
				break;
			}
		}

		if(!found)
			return false;

		else{
			if(current_e->getV1() == new_edge->getV2() || current_e->getV2() == new_edge->getV2())
				return true;
		}

	}

	return NULL;
}

vector<Edge*> create_tour(vector<Edge*> edge_list,int num_cities){

	vector<Edge*> tour_list;
	 
	for(auto start = edge_list.begin(); start != edge_list.end(); ++start){
		
		if((*start)->getV1()->getDegree() < 2 && (*start)->getV2()->getDegree() < 2){

			bool has_cycle = does_create_cycle(tour_list,(*start));	

			bool should_go_home = false;
			
			if(tour_list.size()+1 == num_cities){
				should_go_home = true;
			}

			if(!has_cycle || (has_cycle && should_go_home)){

				(*start)->getV1()->upDegree();
				(*start)->getV2()->upDegree();
				tour_list.push_back((*start));
								
			}
			
		}

	}
	

	return tour_list;

}

void print_tour(ofstream&  o, vector<Edge*> tour_list, Vertex* search_city){

	while(!tour_list.empty()){

		int i = 0;
		for(auto start = tour_list.begin(); start!= tour_list.end(); ++start){

			
			if((*start)->getV1()->getId() == search_city->getId()){
				
				o << search_city->getId() << endl;
				search_city = (*start)->getV2();
				tour_list.erase(tour_list.begin() + i);
				break;
			
			}

			else if((*start)->getV2()->getId() == search_city->getId()){

				o << search_city->getId() << endl;
				search_city = (*start)->getV1();
				tour_list.erase(tour_list.begin() + i);
				break;
			}
		
			i++;
		}

	}

	o << search_city->getId() << endl;

}

int main (int argc, char *argv[]) {
    string line;
    vector<Vertex*> cities;
    cout << "Starting tsp..." << endl;
    // read clargs
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " path/to/inputFile" << endl;
        return 1;
    }

    cout << "Opening - " << argv[1] << endl;
    // open file
    ifstream f(argv[1]);

    if (!f.is_open()) {
        cerr << "could not open file: " << argv[1] << endl;
        return 1;
    }

    
    // create cities from file contents
    while (getline(f, line)) {

        stringstream ss(line);
        string token;
        vector<string> tokens;
	
	//removes all whitespaces
        while(!ss.eof()){
		
		ss >> token;
//		cout << token << endl; 
		tokens.push_back(token);
		if(tokens.size() == 3)
			break;
	}
	
//		cout << "vertex being created" << endl;
                Vertex *v = new Vertex(
                stoi(tokens[0]),
                stoi(tokens[1]),
                stoi(tokens[2])
            );

           cities.push_back(v);
        

	}
    
    if (f.bad()) {
        cerr << "error reading file: " << argv[1] << endl;
        return 1;
    }

    f.close();


	
    // creat all edges
    vector<Edge*> edgeList = createEdgeList(cities);
	
    // sort
    mergesort(&edgeList);

    // remove, here for debug
/*    for (auto iter = edgeList.begin(); iter != edgeList.end(); ++iter) {
        (*iter)->display();
    }*/

    int num_cities = cities.size();
    // create tour
    vector<Edge*> tour_list = create_tour(edgeList,num_cities);

     //remove, here for debug
/*     for(auto iter = tour_list.begin(); iter != tour_list.end(); ++iter){
		cout << "in tour display loop" << endl;
		(*iter)->display();
     }*/


    
    int distance = 0;

    //calculate distance
   for(auto iter = tour_list.begin(); iter != tour_list.end(); ++iter){
	distance += (*iter)->getDistance();
   }

// write output
     
   char* str = argv[1];
   strcat(str,".tour");

   //Can remove next line
   cout << "Output string is: " << str << endl;	


   ofstream o (str);

   if(!o.is_open()){

        cerr << "could not open file: " << str << endl;
        return 1;
    }	 

   o << distance << endl;	
   Edge* current_edge = tour_list[0];
   o << current_edge->getV1()->getId() << endl;
   tour_list.erase(tour_list.begin());
   print_tour(o,tour_list, current_edge->getV2());

    // cleanup
    o.close();    
    cities.clear();
    edgeList.clear();
    tour_list.clear();


    return 0;

}

