 #Q4. Train a simple Linear Regression model using scikit-learn to predict house prices using any sample dataset. Print the model accuracy (R2 score).
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
import seaborn as sns

#Sample and load dataset
house_prices = pd.read_csv('Real-estate1.csv') 

#Prepare the data
print(house_prices.head()) # Check the first few rows of the dataset
X = [
    'X2 house age',
    'X3 distance to the nearest MRT station',
    'X4 number of convenience stores',
    'X5 latitude',
    'X6 longitude'
]
y = 'Y house price of unit area'

X = house_prices[X]
y = house_prices[y]
#Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)
#Predict the house prices on the test set
y_predict = model.predict(X_test)

#Calculate and print the R2 score
r2 = r2_score(y_test, y_predict)
print(f"R2 Score: {r2}")

#Optional: Visualize the predictions vs actual values and regression line with separate colors for y_test and y_predict
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_predict, color='blue', label='Predicted')
sns.scatterplot(x=y_test, y=y_test, color='purple', label='Actual')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted House Prices')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'm--', lw=2)
plt.legend()
plt.grid()
plt.show()



