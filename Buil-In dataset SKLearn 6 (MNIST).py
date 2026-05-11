import matplotlib.pyplot as plt # Import the matplotlib library and give it the alias 'plt'
from sklearn.datasets import fetch_openml # Import the function to fetch datasets

# Load the MNIST dataset
mnist = fetch_openml('mnist_784', version=1, as_frame=True)
X, y = mnist['data'], mnist['target'] 

# Plot the first 10 images
fig, axes = plt.subplots(2, 5, figsize=(10, 5))
for i, ax in enumerate(axes.flatten()):
    ax.imshow(X.iloc[i].values.reshape(28, 28), cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Digit: {y.iloc[i]}")
plt.show()