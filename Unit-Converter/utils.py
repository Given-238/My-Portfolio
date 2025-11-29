def get_float_input(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Enter a valid number.")