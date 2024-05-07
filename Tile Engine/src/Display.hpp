//
// Created by Zack on 1/14/2024.
//
#define SDL_MAIN_HANDLED
#include <iostream>
#include <SDL2/SDL.h>

#ifndef WINTER2024GAMEPROJECT_DISPLAY_HPP
#define WINTER2024GAMEPROJECT_DISPLAY_HPP

struct Log;

struct Display{
    Display(int w_width, int w_height, std::string w_title);
    ~Display();
    bool Init();
    void quit();
    inline void clear(){SDL_SetRenderDrawColor(renderer, 200,200,200,255); SDL_RenderClear(renderer);}
    inline void draw_line(int x1, int y1, int x2, int y2){SDL_RenderDrawLine(renderer, x1, y1, x2, y2);}
    inline void flip(){
        SDL_RenderPresent(renderer);
        Uint64 new_ticks = SDL_GetTicks64();
        deltaTime = (new_ticks-ticks)/1000.0;
        ticks = new_ticks;
    }
    const unsigned char* keyboard = SDL_GetKeyboardState(NULL);
    int width; int height; std::string title;
    Uint64 ticks=0;
    double deltaTime=0;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Event event;
    Log* dev_log;
};

struct Log{
    Log();
    Log(Display*, int lx, int ly, int w, int h);
    void log(std::string);
    Display* display;
    int x; int y;
    int width; int height;
    SDL_Rect messages[4];
};

#endif //WINTER2024GAMEPROJECT_DISPLAY_HPP
