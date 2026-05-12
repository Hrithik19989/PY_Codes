import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Step 1: Generate and split dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
X_labeled, y_labeled = X[:100], y[:100]
X_unlabeled, X_test, y_unlabeled, y_test = train_test_split(X[100:], y[100:], test_size=0.2, random_state=42)

# Step 2: Initialize and train the model
model = RandomForestClassifier(
    n_estimators=100, max_depth=10, min_samples_split=5, min_samples_leaf=2, 
    max_features="sqrt", bootstrap=True, random_state=42
)
model.fit(X_labeled, y_labeled)

# Step 3: Perform self-training iterations
confidence_threshold = 0.9  

for iteration in range(5):
    print(f"Iteration {iteration + 1}: Labeled Samples - {len(y_labeled)}")
    
    pseudo_labels = model.predict(X_unlabeled)
    pseudo_probabilities = model.predict_proba(X_unlabeled).max(axis=1)
    confident_indices = np.where(pseudo_probabilities > confidence_threshold)[0]
    
    # Update labeled dataset
    X_labeled = np.vstack((X_labeled, X_unlabeled[confident_indices]))
    y_labeled = np.hstack((y_labeled, pseudo_labels[confident_indices]))
    
    # Remove pseudo-labeled samples from the unlabeled set
    X_unlabeled = np.delete(X_unlabeled, confident_indices, axis=0)
    
    # Retrain the model
    model.fit(X_labeled, y_labeled)

print(f"Final number of labeled samples: {len(y_labeled)}")

# Step 4: Evaluate the final model
y_pred = model.predict(X_test)
print("Final Model Accuracy on Test Data:", accuracy_score(y_test, y_pred))