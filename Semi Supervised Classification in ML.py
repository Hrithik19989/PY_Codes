import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.semi_supervised import LabelPropagation
from sklearn.metrics import accuracy_score, confusion_matrix

#Load the Iris dataset
data = load_iris()

X = data.data
y = data.target

df = pd.DataFrame(X, columns=data.feature_names)
df["target"] = y

df.head()

#Visualize the dataset 
sns.pairplot(df, hue="target")
plt.show()

# Train/Test Split 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

y_train_semi = y_train.copy()

rng = np.random.RandomState(42)
random_unlabeled = rng.rand(len(y_train_semi)) < 0.7

y_train_semi[random_unlabeled] = -1

plt.figure(figsize=(6,4))

plt.scatter(X_train[:,0], X_train[:,1], c=y_train_semi, cmap="viridis")

plt.title("Labeled vs Unlabeled Data")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")

plt.show()

model = LabelPropagation()

model.fit(X_train, y_train_semi)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)

cm = confusion_matrix(y_test, predictions)

sns.heatmap(cm, annot=True, cmap="Blues")

plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")

plt.show()