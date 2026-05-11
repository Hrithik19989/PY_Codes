from sklearn.datasets import load_diabetes # Import the function to load the diabetes dataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

diabetes = load_diabetes() # Load the diabetes dataset
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df['progression'] = diabetes.target
sns.pairplot(df)
plt.show()