#include "Display.hpp"
#include "Texture.hpp"
#include "Camera.hpp"
#include "BoundingBox.hpp"

int main() {
    Display display(500,500, "Test Window");
    display.Init();
    double &deltaTime = display.deltaTime;

    World world;

    cout<<"Loading file..."<<endl;
    //world.load_from_file("src/testworld.txt");
    world.load_from_file("src/testrecord.txt");
    //world.generate_random_world(10000,10000);
    cout<<"File loaded!"<<endl;
    //world.write_to_file("src/testrecord.txt");

    Camera cam(&display, &world, 25, 1);

    cam.load_textures("src/textures.txt");

    bool pressed = false;

    bool running = true;
    while(running){
        display.clear();

        if(display.keyboard[SDL_SCANCODE_W]){cam.posy += 10*deltaTime;}
        if(display.keyboard[SDL_SCANCODE_D]){cam.posx += 10*deltaTime;}
        if(display.keyboard[SDL_SCANCODE_S]){cam.posy -= 10*deltaTime;}
        if(display.keyboard[SDL_SCANCODE_A]){cam.posx -= 10*deltaTime;}
        if(display.keyboard[SDL_SCANCODE_F]){if(!pressed){cout << "Framerate: " << 1.0/deltaTime << "\nDelta Time: " << deltaTime << endl; pressed=true;}}
        else{pressed = false;}
        cam.render_world();

        if (SDL_PollEvent(&display.event)){
            switch(display.event.type){
                case SDL_QUIT: running = false;
            }
        }
        display.flip();
    }
    display.quit();
    return 0;
}