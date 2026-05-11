import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

X, _ = make_moons(n_samples=5000, noise=0.05, random_state=42)

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c='blue', s=10, alpha=0.5, edgecolor='k')
plt.title('Moon-shaped Dataset (5000 points)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

def plot_k_distance_graph(X, k):
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(X)
    distances, _ = neigh.kneighbors(X)
    distances = np.sort(distances[:, k-1])
    
    plt.figure(figsize=(10, 6))
    plt.plot(distances, marker='o', markersize=3)
    plt.xlabel('Points sorted by distance')
    plt.ylabel(f'{k}-th nearest neighbor distance')
    plt.title('K-distance Graph')
    plt.grid(True)
    plt.show()
    
plot_k_distance_graph(X, k=10)

epsilon = 0.12
min_samples = 10
dbscan_model = DBSCAN(eps=epsilon, min_samples=min_samples)
cluster_labels = dbscan_model.fit_predict(X)

plt.figure(figsize=(10, 6))

unique_labels = set(cluster_labels)
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_labels)))

for k, col in zip(unique_labels, colors):
    class_member_mask = (cluster_labels == k)
    xy = X[class_member_mask]
    if k == -1:
        plt.scatter(xy[:, 0], xy[:, 1], c='red', s=10, alpha=0.5, edgecolor='k', label='Noise')
    else:
        plt.scatter(xy[:, 0], xy[:, 1], c=[col], s=10, alpha=0.5, edgecolor='k', label=f'Cluster {k}')

plt.title('DBSCAN Clustering Results (5000 points)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
n_noise = list(cluster_labels).count(-1)
print(f'Number of clusters found: {n_clusters}')
print(f'Number of noise points: {n_noise}')