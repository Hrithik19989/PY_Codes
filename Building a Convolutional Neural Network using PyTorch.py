import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from keras.datasets import cifar10
import numpy as np

# 1. Data Prep (Channels First: NCHW + No One-Hot)
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
train_images = np.transpose(train_images / 255.0, (0, 3, 1, 2)).astype(np.float32)
test_images = np.transpose(test_images / 255.0, (0, 3, 1, 2)).astype(np.float32)
train_labels = train_labels.flatten().astype(np.int64)
test_labels = test_labels.flatten().astype(np.int64)

train_loader = DataLoader(TensorDataset(torch.tensor(train_images), torch.tensor(train_labels)), batch_size=64, shuffle=True)
test_loader = DataLoader(TensorDataset(torch.tensor(test_images), torch.tensor(test_labels)), batch_size=64, shuffle=False)

# 2. Architecture Definition
class CIFAR10CNN(nn.Module):
    def __init__(self):
        super(CIFAR10CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=(3, 3))
        self.pool = nn.MaxPool2d(kernel_size=(2, 2))
        self.fc1 = nn.Linear(32 * 15 * 15, 128) # Manual math required
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        return self.fc2(x) # Softmax is omitted (built into loss)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CIFAR10CNN().to(device)

# 3. Model Compilation Setup
optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

# 4. Training Engine (Explicit Loop)
for epoch in range(10):
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()                 # Clear old slopes
        loss = criterion(model(images), labels) # Forward pass + loss
        loss.backward()                       # Calculate slopes
        optimizer.step()                      # Update weights
