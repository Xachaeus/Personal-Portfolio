//
// Created by Zack on 1/15/2024.
//
#include "Display.hpp"
#include "World.hpp"
#include "Texture.hpp"
#include <fstream>
#include <algorithm>

#ifndef WINTER2024GAMEPROJECT_CAMERA_HPP
#define WINTER2024GAMEPROJECT_CAMERA_HPP

struct Camera{
    Camera(Display*, World*, int, float);
    ~Camera();
    void render_world() const;
    void load_textures(const string&);
    [[nodiscard]] float inline x_coord(float x) const{return x+((float)world->width/2);}
    [[nodiscard]] float inline y_coord(float y) const{return (float)world->height-(y+((float)world->height/2));}
    Display* display;
    World* world;
    int texture_size;
    float scale;
    float posx; float posy;
    int world_display_window_width; int world_display_window_height;
    Texture** textures;
    int texture_count;
    float deltaTime;
};

#endif //WINTER2024GAMEPROJECT_CAMERA_HPP
