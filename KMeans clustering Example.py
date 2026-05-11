
from sklearn.datasets import load_iris # Import the load_iris function to load the Iris dataset
from sklearn.cluster import KMeans # Import the KMeans class for clustering

# This program demonstrates how to use KMeans clustering from Scikit-learn
# to group the Iris dataset into three clusters based on feature similarity.

iris = load_iris()# Load the Iris dataset (features and labels)
kmeans = KMeans(n_clusters=3)# Create a KMeans clustering object with 3 clusters (since Iris has 3 species)

kmeans.fit(iris.data)# Fit the KMeans model to the Iris data (find clusters)
cluster_labels = kmeans.labels_ # Get the cluster labels assigned to each data point

print("Cluster Labels:", cluster_labels)# Print the cluster labels for each sample in the dataset