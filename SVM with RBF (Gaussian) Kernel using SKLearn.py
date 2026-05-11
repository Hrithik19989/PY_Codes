from sklearn import svm
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import numpy as np

X, y = make_classification(
    n_samples=300,# number of samples
    n_features=2,# number of features
    n_classes=2,# number of classes to classify
    n_redundant=0,# number of redundant features
    n_informative=2,# number of informative features
    random_state=42 #random state for reproducibility
)

# Create and fit the SVM model with a linear kernel
def plot_decision_boundary(model, X, y, title):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
 # Create a grid of points to evaluate the model
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 400),
        np.linspace(y_min, y_max, 400)
    )
 # Predict the class labels for each point in the grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure()
    plt.contourf(xx, yy, Z, alpha=0.3) # Plot the original data points
    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()
    
model_rbf = svm.SVC(kernel='rbf')
model_rbf.fit(X, y)
plot_decision_boundary(model_rbf, X, y, "SVM with RBF Kernel")