//
// Created by Zack on 3/4/2024.
//

#include <math.h>

#ifndef WINTER2024GAMEPROJECT_MATH_HPP
#define WINTER2024GAMEPROJECT_MATH_HPP

struct vec2{
    vec2();
    vec2(float, float);
    union{
        struct{
            float x; float y;
        };
        struct{
            float u; float v;
        };
    };
    inline vec2 operator+(vec2 v){return vec2(x+v.x, y+v.y);}
    inline vec2 operator-(vec2 v){return vec2(x-v.x, y-v.y);}
    inline float magnitude(){return sqrt(x*x + y*y);}
    inline vec2 normal(){return vec2(x/magnitude(), y/magnitude());}
    inline float dot(vec2 v){return x*v.x + y*v.y;}
};


#endif //WINTER2024GAMEPROJECT_MATH_HPP
