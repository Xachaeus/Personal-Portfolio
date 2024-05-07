//
// Created by Zack on 1/15/2024.
//
#include "Display.hpp"
#ifndef WINTER2024GAMEPROJECT_TEXTURES_HPP
#define WINTER2024GAMEPROJECT_TEXTURES_HPP

struct Texture{
    Texture(Display*, std::string, int);
    Texture();
    ~Texture();
    void render(int x, int y, int width, int height);
    Display* display;
    SDL_Surface* surface;
    SDL_Texture* sdl_texture;
    std::string name;
    int id;
};

#endif //WINTER2024GAMEPROJECT_TEXTURES_HPP
