//
// Created by Zack on 1/15/2024.
//

#include "Texture.hpp"

Texture::Texture(){
    display = nullptr;
    surface = nullptr;
    sdl_texture = nullptr;
    name="";
    id = 0;
}

Texture::Texture(Display* disp, std::string path, int t_id){
    id = t_id;
    display = disp;
    surface = SDL_LoadBMP(path.c_str());
    if(!surface){
        std::cout << "Failed to find texture: " << SDL_GetError() << std::endl;
    }
    sdl_texture = SDL_CreateTextureFromSurface(display->renderer, surface);
    if(!sdl_texture){
        std::cout << "Failed to load texture: " << SDL_GetError() << std::endl;
    }
    SDL_FreeSurface(surface);
    surface = nullptr;
    name="";

}

Texture::~Texture(){
    SDL_DestroyTexture(sdl_texture);
    sdl_texture = nullptr;
}

void Texture::render(int x, int y, int width, int height){
    SDL_Rect img;
    img.x = x;
    img.y = y;
    img.w = width;
    img.h = height;
    SDL_RenderCopy(display->renderer, sdl_texture, NULL, &img);
}