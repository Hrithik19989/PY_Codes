#Step 1: Import Required Libraries
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt

#Step 2: Load the Dataset
digits = load_digits()
X = digits.data

#Step 3: Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Step 4: Defining Divisive Clustering Function
def divisive_clustering(X, depth=0, max_depth=3, min_size=50):
  
    if depth == max_depth or len(X) <= min_size:
        return [X]

    
    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(X)

    cluster_1 = X[labels == 0]
    cluster_2 = X[labels == 1]

    
    return (
        divisive_clustering(cluster_1, depth + 1, max_depth, min_size) +
        divisive_clustering(cluster_2, depth + 1, max_depth, min_size)
    )

#Step 5: Execute Divisive Clustering
final_clusters = divisive_clustering(
    X_scaled,
    max_depth=3,
    min_size=50
)

#Step 6: Analyze Cluster Sizes 
cluster_sizes = [len(cluster) for cluster in final_clusters]
cluster_sizes

labels = np.empty(X_scaled.shape[0], dtype=int)

start = 0
for i, cluster in enumerate(final_clusters):
    size = len(cluster)
    labels[start:start + size] = i
    start += size
    
#Step 8: Evaluate Cluster Quality    
sil_score = silhouette_score(X_scaled, labels)
print("Score :", round(sil_score, 2))

#Step 9: Visualizing Divisive Hierarchical Clustering Tree
def build_tree(X, depth=0, max_depth=3, min_size=50, node_name="Root"):
    
    if depth == max_depth or len(X) <= min_size:
        return {
            "name": f"{node_name}\n(size={len(X)})",
            "children": []
        }

    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(X)

    cluster_1 = X[labels == 0]
    cluster_2 = X[labels == 1]

    return {
        "name": f"{node_name}\n(size={len(X)})",
        "children": [
            build_tree(cluster_1, depth + 1, max_depth, min_size, node_name + " → C1"),
            build_tree(cluster_2, depth + 1, max_depth, min_size, node_name + " → C2")
        ]
    }

tree = build_tree(X_scaled, max_depth=3, min_size=50)

def compute_positions(node, depth=0, x=0, positions=None, width=8):
    
    if positions is None:
        positions = {}

    positions[node["name"]] = (x, -depth)

    children = node["children"]
    if children:
        dx = width / len(children)
        start_x = x - width/2 + dx/2

        for i, child in enumerate(children):
            compute_positions(child,
                              depth + 1,
                              start_x + i * dx,
                              positions,
                              width / 2)
    return positions

def extract_edges(node, edges=None):
    
    if edges is None:
        edges = []

    for child in node["children"]:
        edges.append((node["name"], child["name"]))
        extract_edges(child, edges)

    return edges

def plot_tree(tree):

    positions = compute_positions(tree)
    edges = extract_edges(tree)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    
    for parent, child in edges:
        x1, y1 = positions[parent]
        x2, y2 = positions[child]
        ax.plot([x1, x2], [y1, y2], 'k-')
    
    for node, (x, y) in positions.items():

        if "Root" in node:
            color = "lightblue"
        elif "C1" in node or "C2" in node:
            color = "lightgreen"
        else:
            color = "lightyellow"

        ax.text(x, y, node,
                ha='center',
                va='center',
                bbox=dict(boxstyle="round",
                          facecolor=color,
                          edgecolor="black"))

    plt.title("Divisive Hierarchical Clustering Tree", fontsize=14)
    plt.tight_layout()
    plt.show()
plot_tree(tree)