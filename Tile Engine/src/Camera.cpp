//
// Created by Zack on 1/15/2024.
//

#include "Camera.hpp"

Camera::Camera(Display* c_display, World* c_world, int c_texture_size, float c_scale){
    display = c_display;
    world = c_world;
    texture_size = c_texture_size*c_scale;
    scale = c_scale;
    world_display_window_width = display->width/(texture_size) + 2;
    world_display_window_height = display->height/(texture_size) + 2;
    posx = 0;
    posy = 0;
    textures = nullptr;
    texture_count = 0;
}
Camera::~Camera(){
    for(int i=0; i<texture_count; i++){delete textures[i];}
    delete [] textures;
}

void Camera::render_world() const{
    float view_extension = 1; //Defines how far off-screen the camera will process tiles.
    //Get camera's position offset as exact pixel measurement
    float px = floor(posx) + floor((posx-floor(posx))*(float)texture_size)/(float)texture_size;
    float py = floor(posy) + floor((posy-floor(posy))*(float)texture_size)/(float)texture_size;

    for(int x=(int)max((float)0, x_coord(px)-((float)world_display_window_width/2) - view_extension);
        x<(int)min((float)world->width, x_coord(px)+((float)world_display_window_width/2) + view_extension); x++){

        for(int y=(int)max((float)0, y_coord(py)-((float)world_display_window_height/2) - view_extension);
            y<(int)min((float)world->height, y_coord(py)+((float)world_display_window_height/2) + view_extension); y++){

            //Calculate the exact screen pixel coordinates of each tile, taking the camera's partial offset into account
            int sx = ((x*texture_size - (int)floor(x_coord(px)*(float)texture_size) + display->width/2));
            int sy = ((y*texture_size - (int)floor(y_coord(py)*(float)texture_size) + display->height/2));

            /* Only uncomment for debugging purposes
            SDL_Rect r1; SDL_Rect r2;
            r1.x = x1; r2.x = x1+texture_size/2;
            r1.y = y1; r2.y = y1;
            r1.w = texture_size/2; r2.w = texture_size/2;
            r1.h = texture_size; r2.h = texture_size;
            SDL_SetRenderDrawColor(display->renderer, 255,0,0,255);
            SDL_RenderFillRect(display->renderer, &r1);
            SDL_SetRenderDrawColor(display->renderer, 0,255,0,255);
            SDL_RenderFillRect(display->renderer, &r2);
             */
            textures[world->map[x][y]]->render(sx, sy, texture_size, texture_size);
        }
    }
}

void Camera::load_textures(const string& filename){
    cout << "\nLoading textures..." << endl;

    ifstream file(filename);
    string line;
    if(!file){cout<<"Couldn't open textures file!" << endl;}

    size_t num_of_lines = count(
            istreambuf_iterator<char>(file),
            istreambuf_iterator<char>(),
            '\n') + 1;
    cout << "Texture count: " << num_of_lines << endl;

    textures = new Texture*[num_of_lines];

    file.close();
    file.open(filename);

    for(int index=0; index<num_of_lines; index++){
        getline(file,line);
        string components[2];
        string info;
        for(char i : line){
            if(i==':'){components[0] = info; info="";}
            else{info += i;}
        }
        components[1] = info;

        textures[index] = new Texture(display, components[1], index);
        textures[index]->name = components[0];
        if(!textures[index]->sdl_texture){cout << "Could not load texture: " << components[0] << endl;}
        texture_count++;
    }
    cout << "Textures loaded!" << endl;

}