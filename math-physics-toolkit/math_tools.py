import math

def solve_linear(a, b):
    """Solve ax + b = 0"""
    if a == 0:
        return "No solution (a cannot be zero)"
    return -b / a

def solve_quadratic(a, b, c):
    """Solve ax^2 + bx + c = 0"""
    d = b**2 - 4*a*c
    if d < 0:
        return "No real solutions"
    x1 = (-b + math.sqrt(d)) / (2*a)
    x2 = (-b - math.sqrt(d)) / (2*a)
    return x1, x2

def trig_values(angle_deg):
    angle = math.radians(angle_deg)
    return {
        "sin": math.sin(angle),
        "cos": math.cos(angle),
        "tan": math.tan(angle)
    }