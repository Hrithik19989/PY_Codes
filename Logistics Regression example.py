
import numpy as np # Import numpy for numerical operations
import matplotlib.pyplot as plt # Import matplotlib for plotting (not used in this code, but commonly used for visualization)
from sklearn import datasets # Import datasets module to load sample datasets
from sklearn.model_selection import train_test_split # Import train_test_split to split data into training and testing sets
from sklearn.preprocessing import StandardScaler # Import StandardScaler to standardize features
from sklearn.linear_model import LogisticRegression # Import LogisticRegression for building the logistic regression model
from sklearn.metrics import accuracy_score, classification_report # Import metrics for evaluating the model

#This example uses Logistic Regression to classify flowers in the Iris dataset and check how accurately the model predicts their types.

iris = datasets.load_iris()# Load the iris dataset (a classic dataset for classification)
X = iris.data # Assign the features (input variables) to X
y = iris.target # Assign the target labels (output variable) to y

# Split the dataset into training and testing sets (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler() # Create a StandardScaler object for feature scaling
X_train = scaler.fit_transform(X_train) # Fit the scaler on the training data and transform it (standardize features)
X_test = scaler.transform(X_test) # Transform the test data using the same scaler (use statistics from training set)

log_reg = LogisticRegression() # Create a LogisticRegression object (this will be our model)
log_reg.fit(X_train, y_train) # Train (fit) the logistic regression model on the training data

y_pred = log_reg.predict(X_test)# Predict the labels for the test set
accuracy = accuracy_score(y_test, y_pred) # Calculate the accuracy of the model on the test set
print("Accuracy:", accuracy) # Print the accuracy result