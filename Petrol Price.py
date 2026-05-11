Petrol_price = 3.50
stock = 1000

while stock >= 0:
    if stock > 250:
        print("The price of petrol is $", Petrol_price)
        print("The stock of petrol is", stock, "litres.")
        Petrol_price += 0.50
        stock -= 50
    elif stock > 0 and stock <= 250:
        print("The price of petrol is $", Petrol_price)
        print("The stock of petrol is", stock, "litres.")
        Petrol_price += 2.50
        stock -= 50
    elif stock == 0:
        print("The petrol station is out of stock.")
        break
