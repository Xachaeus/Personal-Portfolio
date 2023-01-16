This folder contains my attempts to build a software rasterization engine
from scratch. For this project, I did not follow an actual tutorial; instead,
I researched the rasterization process from the book "Computer Graphics from 
Scratch" by Gabriel Gambetta, and figured out the rest of the mechanics 
independently.

The main program, main.py, contains all of the information about the world.
The WASD keys are used to reposition the camera, and the arrow keys rotate
the camera. The space bar and shift keys also control camera height. The
program is very simple; it supports different colors for different triangles,
and is able to correctly overlay one object over another depending on which 
is closer, but it does not support any textures, lighting, or physics.
This project was essentially just about recreating the rasterization process
from scratch to deepen my own understanding of it, and not to make a functional
rendering engine. However, I had fun making it, and I still enjoy seeing
the whole process come together.

There are several supplementary files, which all contain different objects to
organize the code. The Vector3 file defines a vector object, and utilizes Python
dunder methods to allow easy operations with the object. The Vector3 object is
utilized by every other object in the project.

The Draw file defines functions for drawing triangles onto the screen. To rectreate
the pixel-by-pixel drawing operations done in the GPU in an actual rendering engine,
these functions mathematically determine which pixels need to be filled for a given
line or triangle, and manually set the color of each pixel, one by one. This is
not particularly necessary, but since this project was supposed to be a learning
experience, I figured it would be best to do everything from scratch that I could.

The Triangle file defines a Triangle object which stores three Vector3 objects as the
vertices of the shape. It doesn't have any real methods, and basically just functions
to organize data easier.

The Box file allows a developer to define all of the triangles which make up a box
simply by creating them automatically from a given position and given dimensions.
Again, though the Box object does define several triangles for the developer, it
doesn't have any methods to use after the triangles have been defined, and again 
acts primarily as data storage.

The Camera object contains all of the methods for rendering the scene. It allows
the developer to reposition it before it renders the scene, and translates all of
the triangles in the scene from world space to camera space automatically. It then
utilizes the functions from the Draw file to render the scene to the window.

The Ray file defines a ray object as storage; the main file uses this to figure out
which triangles are closer when they overlap.

Finally, the Rasterizer file utilizes the other files to perform simple renders of
small scenes; it's used to test the rendering engine when it's being adjusted.