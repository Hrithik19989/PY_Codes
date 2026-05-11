from sklearn.datasets import load_wine  # Import the function to load the wine dataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

wine = load_wine()  # Load the wine dataset
X = wine.data  # Extract the feature data
y = wine.target  # Extract the target data

df = pd.DataFrame(X, columns=wine.feature_names)  # Now 'wine' is defined
df['cultivar'] = y

sns.pairplot(df, hue='cultivar')
plt.show()