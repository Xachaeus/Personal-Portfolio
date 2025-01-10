//
// Created by Zack on 1/15/2024.
//

#include "World.hpp"

World::World(){
    width = 0; height = 0;
    map = nullptr;
    loaded = false;
    srand((unsigned)time(nullptr));
}

World::World(int w_width, int w_height){
    width = w_width; height = w_height;
    map = new int*[width];
    for(int i=0; i<width; i++){
        map[i] = new int[height];
    }
    loaded = true;
}

World::~World(){
    for(int i=0; i<width; i++){
        delete [] map[i];
    }
    delete [] map;
    loaded = false;
}

void World::clear_map(){
    for(int i=0; i<width; i++){
        delete [] map[i];
    }
    delete [] map;
    width = 0;
    height = 0;
    map = nullptr;
    loaded = false;
}

void World::generate_random_world(int w, int h){
    width = w;
    height = h;
    map = new int*[width];
    for(int x=0; x<width; x++){
        map[x] = new int[height];
        for(int y=0; y<height; y++){
            map[x][y] = ((int)rand()%10 > 2)? 1 : 0;
        }
    }
    loaded = true;
}

int World::load_from_file(string filename){
    loaded = false;
    /*
    fstream file(filename);
    string world_data((std::istreambuf_iterator<char>(file)),
                      std::istreambuf_iterator<char>());
    file.close(); //Close the filename once the data has been gathered
     */
    ifstream file(filename, ios::binary);
    size_t size;
    file.read(reinterpret_cast<char*>(&size), sizeof(size));
    string world_data;
    world_data.resize(size);
    file.read(&world_data[0], size);
    file.close();

    string val = "";
    int index = 0;
    int count = 0;

    cout<<"Getting metadata..."<<endl;

    while(!loaded){ //Get format information
        if(world_data.substr(index,1)!=";"){
            cout<<"Recording number..."<<world_data.substr(index,1)<<endl;
            val.append(world_data.substr(index,1));
        }
        else{
            cout<<"Found divider..."<<endl;
            if(width==0){
                width = stoi(val);
                val="";
            }
            else{
                height = stoi(val);
                val = "";
                cout<<"Creating map..."<<endl;
                map = new int*[width];
                for(int j=0;j<width;j++){
                    map[j] = new int[height];
                }
                loaded = true;
            }
        }
        index++;
    }
    cout<<"Getting world data..."<<endl;
    for(int i=index; count<width*height; i+=3){ //Get actual information
        val = world_data.substr(i,3);
        //cout<<"Recording tile ID: " << val << "at: " << count%width << ", " << (int)floor(count/width)<< endl;
        map[count%width][(int)floor(count/width)] = stoi(val);
        count++;
    }

    return 0;
}

int World::write_to_file(string filename){
    ofstream file(filename, ios::out | ios::binary);
    string world_data = "";
    world_data.append(to_string(width));
    world_data.append(";");
    world_data.append(to_string(height));
    world_data.append(";");
    for(int i=0; i<width*height; i++){
        if(map[i%width][(int)floor(i/width)]){
            world_data.append("001");
        }
        else{
            world_data.append("000");
        }
    }
    //file << world_data;
    size_t size = world_data.size();
    file.write(reinterpret_cast<const char*>(&size), sizeof(size));
    file.write(world_data.c_str(), size);
    file.close();
    return 1;
}