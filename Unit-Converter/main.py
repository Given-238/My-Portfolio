from utils import get_float_input
import length, weight, temperature, speed, time_units

def main_menu():
    print("\n=== Unit Converter ===")
    print("1. Length")
    print("2. Weight/Mass")
    print("3. Temperature")
    print("4. Speed")
    print("5. Time")
    print("0. Exit")

def length_menu():
    print("\n-- Length Converter --")
    print("1. Meters → Kilometres")
    print("2. Kilometres → Meters")
    print("3. Meters → Centimetres")
    print("4. Centimetres → Meters")

def weight_menu():
    print("\n-- Weight Converter --")
    print("1. Kg → Grams")
    print("2. Grams → Kg")
    print("3. Kg → Pounds")
    print("4. Pounds → Kg")

def temp_menu():
    print("\n-- Temperature Converter --")
    print("1. Celsius → Fahrenheit")
    print("2. Fahrenheit → Celsius")
    print("3. Celsius → Kelvin")
    print("4. Kelvin → Celsius")

def speed_menu():
    print("\n-- Speed Converter --")
    print("1. m/s → km/h")
    print("2. km/h → m/s")
    print("3. m/s → mph")
    print("4. mph → m/s")

def time_menu():
    print("\n-- Time Converter --")
    print("1. Seconds → Minutes")
    print("2. Minutes → Seconds")
    print("3. Hours → Minutes")
    print("4. Minutes → Hours")

while True:
    main_menu()
    choice = input("Choose: ")

    if choice == "1":
        length_menu()
        c = input("Choose: ")
        v = get_float_input("Value: ")
        if c == "1": print(length.meters_to_km(v))
        elif c == "2": print(length.km_to_meters(v))
        elif c == "3": print(length.meters_to_cm(v))
        elif c == "4": print(length.cm_to_meters(v))

    elif choice == "2":
        weight_menu()
        c = input("Choose: ")
        v = get_float_input("Value: ")
        if c == "1": print(weight.kg_to_grams(v))
        elif c == "2": print(weight.grams_to_kg(v))
        elif c == "3": print(weight.kg_to_pounds(v))
        elif c == "4": print(weight.pounds_to_kg(v))

    elif choice == "3":
        temp_menu()
        c = input("Choose: ")
        v = get_float_input("Value: ")
        if c == "1": print(temperature.c_to_f(v))
        elif c == "2": print(temperature.f_to_c(v))
        elif c == "3": print(temperature.c_to_k(v))
        elif c == "4": print(temperature.k_to_c(v))

    elif choice == "4":
        speed_menu()
        c = input("Choose: ")
        v = get_float_input("Value: ")
        if c == "1": print(speed.mps_to_kmph(v))
        elif c == "2": print(speed.kmph_to_mps(v))
        elif c == "3": print(speed.mps_to_mph(v))
        elif c == "4": print(speed.mph_to_mps(v))

    elif choice == "5":
        time_menu()
        c = input("Choose: ")
        v = get_float_input("Value: ")
        if c == "1": print(time_units.seconds_to_minutes(v))
        elif c == "2": print(time_units.minutes_to_seconds(v))
        elif c == "3": print(time_units.hours_to_minutes(v))
        elif c == "4": print(time_units.minutes_to_hours(v))

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")