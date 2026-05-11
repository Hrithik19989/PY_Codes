import numpy
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

#Create the arrays that represent the values of the x and y axis:
x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

# NumPy has a method that lets us make a polynomial model based on the x and y arrays. The 3 means that we want a 3rd degree polynomial (a cubic function).x``
mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

#Then specify how the line will display, we start at position 1, and end at position 22, and we want 100 evenly spaced points in between.
myline = numpy.linspace(1, 22, 100)


plt.scatter(x, y) #Draw the original scatter plot of the data points (x, y) to visualize the relationship between the two variables.
plt.plot(myline, mymodel(myline)) #Draw the line of polynomial regression on the scatter plot using the predicted y values (mymodel(myline)) 
#corresponding to the x values (myline).
plt.show() # Display the diagram
print(r2_score(y, mymodel(x))) #Print the R-squared value to show how well the data points fit the polynomial regression model.
speed = mymodel(17)
print(speed)