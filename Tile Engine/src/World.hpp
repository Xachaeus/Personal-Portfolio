//
// Created by Zack on 1/15/2024.
//
#include "Display.hpp"
#include "Texture.hpp"
#include <fstream>
#include <cmath>
#include <random>
#include <time.h>

#ifndef WINTER2024GAMEPROJECT_WORLD_HPP
#define WINTER2024GAMEPROJECT_WORLD_HPP

using namespace std;

struct World{
    World();
    World(int, int);
    ~World();
    void clear_map();
    int load_from_file(string);
    int write_to_file(string);
    void generate_random_world(int w, int h);
    float inline x_coord(float x){return x+((float)width/2);}
    float inline y_coord(float y){return y-((float)height/2);}
    bool loaded = false;
    int width; int height;
    int** map;

};

#endif //WINTER2024GAMEPROJECT_WORLD_HPP
