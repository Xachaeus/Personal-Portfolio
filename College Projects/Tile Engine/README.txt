Instructions: The executable can be found in cmake-build-debug as
Winter2024GameProject. Once launched from within the existing
file tree, it will load a pre-generated world. Use the WSAD keys
to navigate through the world.

This project was intended to be developed into a larger full-blown
game, but the engine was useful and adaptable enough that I decided
to leave it as its own engine for future projects. The engine can
generate, save, load, and edit tile-based worlds with an arbitrary
number of tile types. It also allows for smooth scrolling through
the tile-based world without stutters or gaps in between individual
tiles, and efficiently displays a large number of tiles.

The engine works with two custom file formats: one for efficiently
storing world and tile information, and one for linking tile IDs
to textures. Both are functionally text files that are interpreted
by the engine. The world files store the dimensions of the world,
and then sequentially list the tile IDs of every tile in the world
from top-left to bottom-right. Tile IDs are stored as three-character
numbers, allowing up to 1000 different types of tiles. Future
versions of the engine will utilize more efficient ways of recording
tile IDs to maximize the number of possible tiles. The tile info
file stores tile information in order (i.e. ID 0 is first, then ID 1,
etc.) and gives each tile a name and the path to its texture. This
allows for easy modification of tile names, values, and IDs, without
having to dig through the source code.

The engine is built on SDL2 and sequentially renders each tile
based on the current camera position. The engine calculates which
tiles are in view from the camera position and tile size, and only
does calculations on visible tiles (i.e. it isn't necessary to check
each tile to see if it is in view; the index ranges of visible tiles
are calculated to avoid this). One drawback of the program is that it
draws tiles sequentially instead of in parallel/it does not utilize
shaders; each visible tile is iterated through and drawn through SDL
individually. Future versions of the engine will utilize a shader-based
rendering approach to remove this handicap and enable even faster 
rendering. 

The engine is also designed to be fully-implementable with other
projects; it is object-oriented, meaning other developers could
subclass the necessary objects for the engine to tweak and tailor the
exact information they need for their games.

The project required me to utilize several of the concepts I had learned
in my CISC 220: Data Structures, such as efficiently allocating and
deallocating memory for the world, and developing an algorithm to
discern which tiles to process on a given frame. It was a fun project
that I plan to build on in the future and possibly use for a future game.