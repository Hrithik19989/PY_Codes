#Import the modules 
import matplotlib.pyplot as plt# Import matplotlib for plotting
from scipy import stats # Import stats module from scipy for statistical functions (used for linear regression)

#Create the arrays that represent the values of the x and y axis:
x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

#Execute a method that returns some important key values of Linear Regression
#Perform linear regression on the data points (x, y) to find the slope, intercept, correlation coefficient (r), p-value, and standard error of the estimate.
slope, intercept, r, p, std_err = stats.linregress(x, y)

#Define a function that calculates the predicted y values based on the linear regression parameters (slope and intercept) for a given x value.
def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x)) #Run each value of the x array through the function. This will result in a new array with new values for the y-axis:

plt.scatter(x, y) #Draw the original scatter plot of the data points (x, y) to visualize the relationship between the two variables.
plt.plot(x, mymodel) #Draw the line of linear regression on the scatter plot using the predicted y values (mymodel) corresponding to the x values. 
# This line represents the best fit line for the data points based on the linear regression analysis.
plt.show() # Display the diagram
print(r) #Print the correlation coefficient (r) to show how well the data points fit the linear regression model. 
# The closer r is to 1 or -1, the stronger the linear relationship between x and y.