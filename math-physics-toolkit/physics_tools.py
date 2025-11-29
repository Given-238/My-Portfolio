import math

def projectile_motion(u, angle_deg):
    """Returns time of flight, max height, range"""
    g = 9.8
    angle = math.radians(angle_deg)
    
    time_of_flight = (2 * u * math.sin(angle)) / g
    max_height = (u**2 * math.sin(angle)**2) / (2*g)
    range_distance = (u**2 * math.sin(2*angle)) / g

    return {
        "time_of_flight": time_of_flight,
        "max_height": max_height,
        "range": range_distance
    }

def newtons_second_law(mass, acceleration):
    """F = ma"""
    return mass * acceleration

def weight_on_earth(mass):
    """Calculate weight (N) on Earth"""
    g = 9.8
    return mass * g