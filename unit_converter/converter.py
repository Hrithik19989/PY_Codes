# UNIT CONVERTER CLI

UNITS = {
    "Length": {
        "km":     1000,
        "m":      1,
        "cm":     0.01,
        "mm":     0.001,
        "miles":  1609.344,
        "feet":   0.3048,
        "inches": 0.0254,
    },
    "Weight": {
        "kg":      1,
        "g":       0.001,
        "mg":      0.000001,
        "pounds":  0.453592,
        "ounces":  0.028349,
    },
    "Speed": {
        "km/h": 0.277778,
        "m/s":  1,
        "mph":  0.44704,
    }
}

def convert_unit(value , from_unit , to_unit , category):
    factors = UNITS[category]
    base = value * factors[from_unit]
    return base / factors[to_unit]

def convert_temprature(value , from_unit , to_unit):
      # First convert to Celsius
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        celsius = value - 273.15
        
    # Then convert Celsius to target
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return (celsius * 9 / 5) + 32
    elif to_unit == "kelvin":
        return celsius + 273.15
    
def show_units(category):
    if category == "Temperature":
        units = ["celsius" , "fahrenheit" , "kelvin"]
    else:
        units = list(UNITS[category].keys())
    
    print(f"\n  Available units:")
    
    for i , unit in enumerate(units , 1):
        print(f"    {i}. {unit}")
    return units
    
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")
            
def get_choice(prompt, options):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"  Enter a number between 1 and {len(options)}.")
        except ValueError:
            print("  Please enter a valid number.")
            
def run_conversion(category):
    print(f"\n  📐 {category} Converter")
    print("  " + "-" * 30)
    
    units = show_units(category)
    
    from_unit = get_choice("\n Convert FROM UNIT(Enter a number): " ,units)
    to_unit = get_choice("Convert TO UNIT(Enter a number): " ,units)
    
    if from_unit == to_unit:
        print("  Same unit selected — result is the same value.")
        return
    
    value = get_float(f" Enter value in {from_unit} : ")
    
    if category == "Temperature":
        result = convert_temprature(value , from_unit , to_unit)
    else:
        result = convert_unit(value , from_unit , to_unit , category)
    print(f"\n  ✅ {value:g} {from_unit} = {result:.4f} {to_unit}")
    
    
CATEGORIES = list(UNITS.keys()) + ["Temperature"]

def menu():
    print("\n  📏 UNIT CONVERTER")
    print("  " + "=" * 25)
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(CATEGORIES) + 1}. Exit")
    
def main():
    while True:
        menu()
        choice = get_choice("\n  Choose a category: ", CATEGORIES + ["Exit"])

        if choice == "Exit":
            print("\n  Goodbye! 👋\n")
            break
        else:
            run_conversion(choice)
            input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()