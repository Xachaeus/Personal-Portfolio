//
// Created by Zack on 1/14/2024.
//

#include "Display.hpp"

#include <utility>

Display::Display(int w_width, int w_height, std::string w_title){
    width = w_width; height = w_height; title = std::move(w_title);
    dev_log = new Log(this, 0, height-100, 100,100);
}
Display::~Display(){
    SDL_DestroyWindow(window);
    SDL_DestroyRenderer(renderer);
    delete dev_log;
}

bool Display::Init(){
    if(SDL_Init(SDL_INIT_EVERYTHING) < 0){
        std::cout << "SDL initialization failed with error: " << SDL_GetError() << std::endl;
        return EXIT_FAILURE;
    }
    window = SDL_CreateWindow(title.c_str(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, SDL_WINDOW_OPENGL);
    if(!window){
        std::cout << "Failed to create window: " << SDL_GetError() << std::endl;
    }
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC);
    if(!renderer){
        std::cout << "Failed to create renderer: " << SDL_GetError() << std::endl;
    }

    return true;
}

void Display::quit(){
    if (window != nullptr) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }

    if (renderer != nullptr) {
        SDL_DestroyRenderer(renderer);
        renderer = nullptr;
    }

    SDL_Quit();
}

Log::Log(){
    display = nullptr;
    x = 0; y = 0;
    width = 0; height = 0;
}
Log::Log(Display* d, int lx, int ly, int w, int h){
    display = d; x = lx; y = ly; width = w; height = h;
}

void Log::log(std::string message){
    //TTF_Font
}