from math_tools import solve_linear, solve_quadratic, trig_values
from physics_tools import projectile_motion, newtons_second_law, weight_on_earth
from utils import get_float_input

def main_menu():
    print("\n=== Math & Physics Helper Toolkit ===")
    print("1. Solve Linear Equation")
    print("2. Solve Quadratic Equation")
    print("3. Trigonometry Calculator")
    print("4. Projectile Motion Calculator")
    print("5. Newton's Second Law (F = ma)")
    print("6. Weight on Earth")
    print("0. Exit")

while True:
    main_menu()
    choice = input("Select option: ")

    if choice == "1":
        a = get_float_input("Enter a: ")
        b = get_float_input("Enter b: ")
        print("Solution:", solve_linear(a, b))

    elif choice == "2":
        a = get_float_input("Enter a: ")
        b = get_float_input("Enter b: ")
        c = get_float_input("Enter c: ")
        print("Solutions:", solve_quadratic(a, b, c))

    elif choice == "3":
        angle = get_float_input("Enter angle (degrees): ")
        print(trig_values(angle))

    elif choice == "4":
        u = get_float_input("Initial velocity (m/s): ")
        angle = get_float_input("Angle (degrees): ")
        print(projectile_motion(u, angle))

    elif choice == "5":
        m = get_float_input("Mass (kg): ")
        a = get_float_input("Acceleration (m/s^2): ")
        print("Force =", newtons_second_law(m, a))

    elif choice == "6":
        m = get_float_input("Mass (kg): ")
        print("Weight =", weight_on_earth(m))

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Try again.")