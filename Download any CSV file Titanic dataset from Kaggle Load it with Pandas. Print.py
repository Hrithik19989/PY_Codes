import pandas as pd
# Load the Titanic dataset from a CSV file
titanic_data = pd.read_csv('titanic.csv')
# Print the first few rows of the dataset
print(titanic_data.head(18))
#Print:number of rows, column names, and count of missing values
print("Number of rows:", titanic_data.shape[0])
print("Column names:", titanic_data.columns)
print("Count of missing values:")
print(titanic_data.isnull().sum())