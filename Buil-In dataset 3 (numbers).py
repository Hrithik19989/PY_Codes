import matplotlib.pyplot as plt
from sklearn.datasets import load_digits  # Import the function to load the digits dataset

digits = load_digits()  # Load the digits dataset

fig, axes = plt.subplots(2, 5, figsize=(10, 5))
for i, ax in enumerate(axes.flatten()):
    ax.imshow(digits.images[i], cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Digit: {digits.target[i]}")
plt.show()