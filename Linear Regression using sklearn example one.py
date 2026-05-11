import pandas #import the pandas library to read the data from a CSV file
from sklearn import linear_model # Import the linear_model module from sklearn to perform linear regression

df = pandas.read_csv("data.csv") # Read the data from a CSV file named "data.csv" into a pandas DataFrame called df

X = df[['Weight', 'Volume']]   # Select the 'Weight' and 'Volume' columns from the DataFrame as the features (input variables) for the linear regression model and assign them to X
y = df['CO2']   # Select the 'CO2' column from the DataFrame as the target variable (output variable) for the linear regression model and assign it to y

regr = linear_model.LinearRegression()  # Create a LinearRegression object called regr, which will be used to fit the linear regression model to the data
regr.fit(X, y)

#predict the CO2 emission of a car where the weight is 2300kg, and the volume is 1300cm3:
predictedCO2 = regr.predict([[2300, 1300]]) # Use the fitted linear regression model (regr) to predict the CO2 emission for a new data point with a weight of 2300 kg
# and a volume of 1300 cm3. The predict method takes a 2D array as input, so we pass [[2300, 1300]] to represent the features of the new data point. 
# The predicted CO2 emission is stored in the variable predictedCO2.

predictedCO2 = regr.predict([[3300, 1300]])
print(predictedCO2) # Print the predicted CO2 emission value to the console. 
# This will output the result of the linear regression prediction based on the input features (weight and volume).


print(regr.coef_) # Print the coefficients of the linear regression model, which represent the weights assigned to each feature (Weight and Volume) in the linear equation that predicts CO2 emissions.
