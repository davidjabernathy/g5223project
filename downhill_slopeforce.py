import math
"""
   /////////////////////////////////
  // SKATE ACCELERATION/VELOCITY //
 //     GOING DOWNHILL CODE     //
/////////////////////////////////

The function will return 3 different variables, the skaters force going
downhill, the downward angle of the hill, and the skater velocity.
This is for visual outputs incase we want to show the angle of the hill
as well as the speed the skater will go.


NOTE: slope_force and skater_velocity are both showing the same thing
just in different ways. Recommend the skater_velocity as it is in speed
and not Newtons of force.
"""

# All variables we will need to have pull from the data

# if needed, top of the hill elevation and botom of hill elevation code

TopHill_elevation = 552 #feet
bottomHill_elevation = 10 #feet
HillHeight = TopHill_elevation - bottomHill_elevation



elevation = 553.1 #feet
street_length = 1.5 #miles

# Variables that will be hard coded or user input
skateweight = 130.86
gravity = 9.8 #m/s^2

def skate_downhill_accel(street_length, skateweight, HillHeight, gravity):

    #finding acceleration of skater
    hillangle = math.sin(elevation/street_length)
    acceleration = gravity * hillangle

    #Time it will take to make it to the bottom
    #d = (InitialVelocity * time) + [acceleration * time^2]/2
    setupFunction = (2 * street_length) / abs(acceleration)
    skateTime = math.sqrt(setupFunction)

    skate_velocity = street_length / skateTime
    
    airfrict = .02
    #Newtons of force
    slope_force = skateweight * hillangle * (9.81 - airfrict)
    print(skate_velocity, "Meters per second")
    
    return(slope_force, hillangle, skate_velocity)


skate_downhill_accel(street_length, skateweight, elevation, gravity)
