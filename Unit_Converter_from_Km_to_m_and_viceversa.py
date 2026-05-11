 #Unit coverter from Km to m and viceversa  
#Function to convert Km to m
def km_to_m(km):
    m = km * 1000
    return m

#Function to convert m to Km
def m_to_km(m):
    km = m / 1000
    return km
#Example usage
input_value = float(input("Enter the value: "))
unit = input("Enter the unit converting into (km or m): ")

if unit == "km":
    result = km_to_m(input_value)
    print(f"{input_value} km is equal to {result} m")
elif unit == "m":
    result = m_to_km(input_value)
    print(f"{input_value} m is equal to {result} km")
else:
    print("Invalid unit. Please enter 'km' or 'm'.")
    
