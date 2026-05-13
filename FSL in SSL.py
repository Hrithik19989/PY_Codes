import random
import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision.datasets import CIFAR10
import timm

random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

model = timm.create_model("resnet50", pretrained=True, num_classes=0)
model.eval().to(device)

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

train_dataset = CIFAR10(root="./data", train=True, transform=transform, download=True)
test_dataset  = CIFAR10(root="./data", train=False, transform=transform, download=True)

class_names = train_dataset.classes
print("Classes:", class_names)

selected_classes = [0, 1, 2]
num_support_per_class = 5
num_query_per_class   = 5

support_indices, query_indices = [], []

for cls in selected_classes:
    train_idxs = [i for i, y in enumerate(train_dataset.targets) if y == cls]
    test_idxs  = [i for i, y in enumerate(test_dataset.targets)  if y == cls]

    support_indices.extend(random.sample(train_idxs, num_support_per_class))
    query_indices.extend(random.sample(test_idxs,  num_query_per_class))
    
support_images, support_labels = zip(*[train_dataset[i] for i in support_indices])
query_images,   query_labels   = zip(*[test_dataset[i]  for i in query_indices])

support_images = torch.stack(support_images).to(device)
query_images   = torch.stack(query_images).to(device)

support_labels = list(support_labels)
query_labels   = list(query_labels)

with torch.no_grad():
    support_embeddings = model(support_images)
    query_embeddings   = model(query_images)

support_embeddings = F.normalize(support_embeddings, p=2, dim=1)
query_embeddings   = F.normalize(query_embeddings, p=2, dim=1)

similarity = torch.mm(query_embeddings, support_embeddings.T)
_, nearest = similarity.max(dim=1)
predicted_labels = [support_labels[i] for i in nearest.cpu().tolist()]

print("\nFew-Shot Classification Results:")
for i, (t, p) in enumerate(zip(query_labels, predicted_labels), 1):
    print(f"Query {i}: True = {class_names[t]:12s} | Pred = {class_names[p]}")

correct = sum(int(t == p) for t, p in zip(query_labels, predicted_labels))
acc = 100.0 * correct / len(query_labels)
print(f"\nAccuracy: {acc:.2f}%")