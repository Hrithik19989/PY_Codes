from scipy import stats # Import stats module from scipy for statistical functions (used for linear regression)

x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

slope , intercept , r, p ,std_err = stats.linregress(x,y)

def myfunc(x):
    return slope * x + intercept 

mymodel =list(map(myfunc ,x))

speed = myfunc(10)  #Predict the y value for a new x value (10 in this case) using the linear regression model (myfunc).
print(speed) #Print the predicted y value for the new x value (10) to see the result of the linear regression prediction.