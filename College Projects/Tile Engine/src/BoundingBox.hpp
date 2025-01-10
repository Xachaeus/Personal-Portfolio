//
// Created by Zack on 3/4/2024.
//

#include <iostream>
#include <fstream>

#ifndef WINTER2024GAMEPROJECT_BOUNDINGBOX_HPP
#define WINTER2024GAMEPROJECT_BOUNDINGBOX_HPP

using namespace std;

struct BoundingMesh{
    BoundingMesh();
    BoundingMesh(string data);
    ~BoundingMesh();
    float* points;
    int num_of_points;
    inline float x(int i){return points[i*2];}
    inline float y(int i){return points[(i*2) + 1];}
};

struct BoundingBox{
    BoundingBox();
    BoundingBox(float world_x,float world_y,float w,float h);
    float x; float y;
    float width; float height;

    inline bool contains(float px, float py){return px<(x+width/2) && px>(x-width/2) && py<(y+height/2) && py>(y-height/2);}
};

#endif //WINTER2024GAMEPROJECT_BOUNDINGBOX_HPP
