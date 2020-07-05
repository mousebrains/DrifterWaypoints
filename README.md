# For a drifter and a glider, calculate a set of waypoints in the drifter's moving frame

We will be receiving drifter GPS fixes periodically.
When the glider surfaces, get its GPS fix and depth averaged current.
Given a predefined pattern, calculate a set of waypoints in the drifter's moving reference frame.

# Original README

For a drifter reporting a GPS position periodically, 
follow it with a glider flying a prescribed pattern.

The GPS coordinates are loaded at startup and again when they are updated.
The last n coordinates are used to calculate a drifter velocity, 
in addition to the last known fix. 
The velocity and last fix are used to predict the drifters when the glider surfaces.

The Glider's position, through water velocity, and depth averaged currents are
read from the surface log on SFMC when the glider surfaces.
The drifter's expected position and velocity are then used to project where the drifter will be
when the glider dives again. A set of waypoints if generated for the glider so it will fly a 
pattern about the drifter, in the drifter's moving frame.

