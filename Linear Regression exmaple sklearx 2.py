# Step 1: Importing all the required libraries 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Step 2: Reading the dataset:
df = pd.read_csv("data.csv")
X = df[['Weight', 'Volume']] 

# Taking only the selected two attributes from the dataset
y = df[['Price', 'CO2']]
#display the first 5 rows  of the dataset to check if it is loaded correctly
y.head()