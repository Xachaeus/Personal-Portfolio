This folder contains two launchable programs: Raycaster.py and Raycasting_Engine.py. Both
programs use settings from an additional file, Settings.py, which allows easy toggling
of the player's FOV, the number of rays being casted, how quickly the player moves,
and how quickly they turn.

The first program, Raycaster.py, was designed by following a video tutorial; however,
the program in the video was written in C, and I was unable to get OpenGL working on my
PC at the time, so I opted to work with Python. I then translated the code from the video as 
directly as I could. When the program is run, a Raycasted view is shown in the right half of the
window, and a top-down 2D view of the scene, with the rays shown, is visible on the left
side of the window. The original program from the tutorial, however, did not have any
collision detection, so I implemented a simple detection system myself, which essentially
only allowed the player to move if their next projected position was outside of a wall.
I eventually replaced it with a form of sliding collision, where the player could slide
along a wall if they tried to walk into it.

The second program, Raycasting_Engine.py, uses the same mathematics as the first program,
but was redesigned for efficiency and included some extra features. In this version, I added
the ability to include simple textures (for performance reasons, the textures were limited
to 8x8px) which could be imported as whole images. The program also includes an "easy mapping"
feature, which allows a developer to design a maze simply with numbers in a list. The program
parses the information from the list to build a grid, and when the rays are cast, they first
detect which kind of wall they've hit, and then figure out how far along the wall they've hit
to determine which row of the texture they should display. The program contains a level feature
as well, so that when one maze is solved, another one loads instantly.

These two programs, though rudimentary, were the first proper game engines I've ever worked on,
and remain some of my favorite projects.
