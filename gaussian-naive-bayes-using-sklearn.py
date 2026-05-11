from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Generate a synthetic dataset
X, y = make_classification(n_samples=100, n_features=2,
                           n_redundant=0, n_clusters_per_class=1,
                           random_state=42)

# Visualize the dataset
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolor='k')
plt.title('Synthetic Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the Gaussian Naive Bayes classifier
gnb = GaussianNB()

# Train the model
gnb.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = gnb.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Load the Census Income dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
column_names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 
                'marital-status', 'occupation','relationship', 'race', 
                'sex', 'capital-gain', 'capital-loss', 'hours-per-week',
                'native-country', 'income']
census_data = pd.read_csv(url, names=column_names)

# Display the first few rows of the dataset
print(census_data.head())

# Convert categorical variables to numerical values
le = LabelEncoder()
categorical_features = ['workclass', 'education', 'marital-status',
                        'occupation', 'relationship', 'race', 'sex',
                        'native-country', 'income']
for feature in categorical_features:
    census_data[feature] = le.fit_transform(census_data[feature])

# Normalize continuous variables
census_data[
  ['age', 'fnlwgt', 'education-num', 'capital-gain', 
             'capital-loss', 'hours-per-week']] = census_data[
  ['age', 'fnlwgt','education-num', 'capital-gain', 'capital-loss',
   'hours-per-week']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# Display the preprocessed data
print(census_data.head())

# Extract features and labels
X = census_data.drop('income', axis=1)
y = census_data['income']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the Gaussian Naive Bayes classifier
gnb = GaussianNB()

# Train the model
gnb.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = gnb.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
