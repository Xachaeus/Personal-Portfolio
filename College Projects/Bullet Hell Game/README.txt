CONROLS:
Movement: WSAD
Shoot: SPACE
Special: F

This game was a personal project I made for myself to practice
different types of programming applications. I decided to make
a bullet hell game because it would involve utilizing an
object-oriented approach effectively and efficiently, would
require the management of several hundred individual projectiles
in an efficient manner, and would require practice in
parallel computing techniques to effectively simulate and
control the trajectories of those projectiles. I would also have
to utilize some basic game design conecepts, such as ensuring good 
visibility of the projectiles and the UI elements. Because
the central focus of this project was the programming aspect, I
elected not to use any outside assets, and created all of the
visuals with built-in drawing functions.

I made the program in Python using Pygame, mostly because I am
very familiar with the library and wanted to focus on the concepts
instead of the actual language. I did not use any libraries other
than Pygame, and only used the Pygame library for rendering and
time-tracking purposes; I implemented the rest of the game's 
functionality myself.

The game is very simple: move a player around, avoid enemy 
projectiles, and try to hit the enemy with your projectiles. The
enemy moves around at the top of the screen, and your projectiles
have a limited spread and only travel up, so in order to win the 
game, the player has to do more than just dodge incoming projectiles.
The player has a special attack that they can use to deal a lot of
damage to the enemy. To charge the special, the player must remain in
close proximity to the enemy; the closer they are to the enemy, the
faster the special will charge. If the player gets
too far away from the enemy, the special attack will stop charging,
and if the player gets even farther, the special attack will slowly 
lose charge. This mechanic keeps the player from just hiding at the
bottom of the screen where the enemy's projectile patterns are the
most spread-out.

The enemy unleashes projectiles in waves called patterns. Each pattern
will continue for a certain amount of time, stop, and after a short
pause, another pattern will begin. Each pattern is designed to have
a unique visual appearance, as well as a unique method for avoiding
the pattern's projectiles.

The projectile mechanics revolve around timers, like much of the rest
of the game. In order to prevent varying performances or frame rate
drops from affecting the speed of the game, everything in the game
that moves calculates the number of pixels to travel based on the amount
of time passed since the last frame. The mechanics for timing how long
patterns last for, as well as the paths of the projectiles, are also built
on timers. Each projectile is an object with a unique set of properties,
and each projectile has its own function to call to calculate its movement
for each frame. The movement function is passed the projectile object and
the amount of time since that projectile was fired, and uses this
information to move the projectile along an organized and calculated path.
For example, the function could tell the projectile to travel straight
for 3 seconds, then start rotating around the enemy for two seconds,
then travel straight forever while increasing its size slowly. Because each
projectile is processed individually and independently of the others,
the path each one follows is entirely arbitrary.

This is where game design comes in. Designing each pattern involves
choosing where projectiles spawn, how often they spawn (for the duration
of the pattern), and what path they follow once they spawn. These values
are manually adjusted to create interesting and challenging patterns for the
player to avoid.

The game is obviously missing several important features of any publishable
game, including a main menu, proper handling for after the player or enemy
is killed, and the ability to adjust the game settings without changing a 
text file, not even to mention the complete lack of game audio. However, as
an exercise in game development and efficient parallel computing,
this project was very helpful for me.
