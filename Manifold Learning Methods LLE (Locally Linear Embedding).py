from sklearn.datasets import load_digits
from sklearn.manifold import LocallyLinearEmbedding
import matplotlib.pyplot as plt

digits = load_digits()
X = digits.data
y = digits.target

lle = LocallyLinearEmbedding(n_components=2, random_state=42)
X_lle = lle.fit_transform(X)

plt.scatter(X_lle[:, 0], X_lle[:, 1], c=y)
plt.show()