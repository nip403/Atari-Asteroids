# Atari-Asteroids
A clone of the classic game Asteroids by Atari in Python 3.x using the Pygame module.

The game is still in Alpha development.

# Maths
I draw the spaceship and the asteroid polygons using these equations:
- x = cx + r * cos(theta)
- y = cy + r * sin(theta)

where (cx,cy) is the centre point of the circle, r is the radius, and theta is the angle in [radians](https://en.wikipedia.org/wiki/Radian).\
Note that radians=0 begins at the rightmost point on the circle.

Refer to this [wikipedia article](http://en.wikipedia.org/wiki/Circle#Equations) for more information on Parametric equations.

# Gameplay
I am still working on the core game mechanics. You can move the ship using the UP arrow.\
Use the LEFT and RIGHT arrow keys to rotate the ship.

The ship has a momentum which gives it a smooth movement, and that is shown by the ship's collision circle changing colour.\
Currently, when a bullet hits an asteroid, it splits into 2, then 3, then 4 etc. children asteroids respectively.

In future, the game will progress toward 2 modes:
- Endless waves
- Levels

I am also planning to implement:
- A scoring system
- A particle system to replace the collision circle
- Startscreen
- Deathscreen
- Menu/level select
- Multiple difficulties (it will affect the number of children spawned and speed)

# Requirements
I am using the [Python 3.7](https://www.python.org/downloads/release/python-370/) IDLE.\
Download project and run main.py to use.\
Python 3.6 and Pygame 1.7.x or above is required.\
You can download pygame either [here](https://www.pygame.org/download.shtml) or [here](https://bitbucket.org/pygame/pygame/downloads/).

If you are running any version before 3.6, you will need to rewrite all f-strings using either of the following:
- % operator
- format() method
