import numpy
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
 
 #Create the arrays that represent the values of the x and y axis:
x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

# NumPy has a method that lets us make a polynomial model based on the x and y arrays. The 3 means that we want a 3rd degree polynomial (a cubic function).x``
mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

#Then specify how the line will display, we start at position 2, and end at position 95, and we want 100 evenly spaced points in between.
myline = numpy.linspace(2, 95, 100)

plt.scatter(x, y) #Draw the original scatter plot of the data points (x, y) to visualize the relationship between the two variables.
plt.plot(myline, mymodel(myline)) #Draw the line of polynomial regression on the scatter plot using the predicted y values (mymodel(myline)) 
#corresponding to the x values (myline).
plt.show() # Display the diagram

#Print the R-squared value to show how well the data points fit the polynomial regression model.
print(r2_score(y, mymodel(x)))