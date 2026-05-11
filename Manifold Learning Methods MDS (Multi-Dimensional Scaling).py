from sklearn.datasets import load_digits
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

digits = load_digits()
X = digits.data
y = digits.target

mds = MDS(n_components=2, random_state=42)
X_mds = mds.fit_transform(X)

plt.scatter(X_mds[:, 0], X_mds[:, 1], c=y)
plt.show()