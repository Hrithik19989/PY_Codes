from sklearn.datasets import load_linnerud  # Import the function to load the Linnerud dataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

linnerud = load_linnerud()  # Load the Linnerud dataset
X = linnerud.data  # Extract the feature data
y = linnerud.target  # Extract the target data

df = pd.DataFrame(X, columns=linnerud.feature_names)
df_targets = pd.DataFrame(y, columns=linnerud.target_names)

sns.pairplot(df_targets)
plt.show()