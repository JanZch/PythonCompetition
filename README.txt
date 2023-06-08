# PythonCompetition

To do:
balancing work 
 - make misslemaxtimer a function of time
 - adjust speeds and turn speeds
points, lives
gameover
Sidescrolling
  

Rules:
• Submissions by one student, or as a team submission by maximum of two students is allowed
• One Raspberry Pi Zero kit can be won per person, so in groups of two, both students can win
one! In each lecture group three submissions will be awarded. All nominated entries receive a
certificate.
• The Standard Libraries supplied with Python and the use of pygame, numpy, scipy, matplotlib are
allowed. Do not use any other libraries as the goal is to make the simulation yourself, also the
physics, and AI!
• Do not download large sections of code of other people. We check your entry against many
repositories where similar programs can be found (or sites of Python courses). Merely changing
the graphics of an existing game or simulation is not enough effort for the bonus and may even
lead to a fraud being reported to the exam committee.
• Use the programming style as taught in the course to make your code readable:
– Use comment lines, whitespace and docstrings
– Use sensible names for variables and functions
– Use two or more script files to organize your project

Brainstorming 

IDEA 1
  Main Gameplay:
• Asteroids 
• Bodies are probably stationary and projectiles are affected by their gravity
  AI:
• There is an enemy(ies) 
• The AI can move and shoot
• It has waypoints on a map that tell it where to go
• the AI moves between waypoints depending on player position and tries to shoot meanwhile

IDEA 2 <---- THIS ONE
  Main Gameplay:
• Flying V dodging missiles
• Top-down view, continuous speed, can only control direction
• Missiles have the same velocity, but lower turn rate
• Flying V has a turbo, where you can temporarily increase speed to outrun missiles
• Area loops
• More and more missiles as time goes on
• Missiles come in from edge of the map
• Extra: radar-guided and heat-seeking missiles, chaff and flares
