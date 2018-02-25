import math
"""
   /////////////////////////////////
  // SKATE ACCELERATION/VELOCITY //
 //     GOING DOWNHILL CODE     //
/////////////////////////////////
"""

# All variables we will need to have pull from the data
"""
if needed, top of the hill elevation and botom of hill elevation code

TopHill_elevation = 552 #feet
bottomHill_elevation = 10
HillHeight = TopHill_elevation - bottomHill_elevaion

"""

elevation = 553.1 #feet
street_length = 1.5 #miles

# Variables that will be hard coded or user input
skateweight = 130.86
gravity = 9.8 #m/s^2

def skate_downhill_accel(street_length, skateweight, elevation, gravity):

    #finding acceleration of skater
    hillangle = sin(elevation/street_length)
    acceleration = gravity * hillangle

    #Time it will take to make it to the bottom
    #d = (InitialVelocity * time) + [acceleration * time^2]/2
    skateTime = sqrt((2 * street_length) / acceleration)

    skate_velocity = street_length / skateTime
    
    airfrict = .02
    slope_force = skateweight * hillangle * (9.81 - airfrict)
    
    return(slope_force, hillangle)
