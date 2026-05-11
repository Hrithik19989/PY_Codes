import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris # Import the function to load the Iris dataset

iris = load_iris() # Load the Iris dataset
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target
sns.pairplot(df, hue='species')
plt.show()