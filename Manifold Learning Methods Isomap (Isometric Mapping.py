from sklearn.datasets import load_digits
from sklearn.manifold import Isomap
import matplotlib.pyplot as plt

digits = load_digits()
X = digits.data
y = digits.target

isomap = Isomap(n_components=2)
X_isomap = isomap.fit_transform(X)

plt.scatter(X_isomap[:, 0], X_isomap[:, 1], c=y)
plt.show()