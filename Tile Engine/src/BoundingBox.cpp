//
// Created by Zack on 3/4/2024.
//

#include "BoundingBox.hpp"

BoundingMesh::BoundingMesh(){
    points = nullptr;
}

BoundingMesh::BoundingMesh(string data){
    num_of_points = 0;
    string values;
    string num; int index=0;
    int p_index = 0;
    if(data[0]!='~'){
        ifstream file(data);
        if(!file){cout << "Couldn't open mesh file!" << endl;}
        getline(file, values);
        file.close();
    }
    else{
        values = data.substr(1);
    }
    while(num_of_points==0){
        if(values[index]!=' '){num+=values[index];}
        else{num_of_points = stoi(num);num="";}
        index++;
    }
    points = new float[2*num_of_points];

    for(int i=index;i<values.length(); i++){
        if(values[i]!=' '){num+=values[i];}
        else{points[p_index] = stof(num); num=""; p_index++;}
    }
    if(num!=""){points[p_index] = stof(num);}
}

BoundingMesh::~BoundingMesh(){
    delete [] points;
}

BoundingBox::BoundingBox(){
    x=0;y=0;
    width=0;height=0;
}

BoundingBox::BoundingBox(float world_x, float world_y, float w, float h){
    x = world_x; y = world_y;
    width = w; height = h;
}
