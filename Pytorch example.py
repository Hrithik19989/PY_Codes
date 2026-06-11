import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim

class CustomRegressionDataset(Dataset):
    def __init__(self, num_samples=1000):
        # Generate dummy features (10 numbers per sample) and labels
        self.X = torch.randn(num_samples, 10)
        # Label is a linear combination with some added noise
        self.y = self.X.sum(dim=1, keepdim=True) + torch.randn(num_samples, 1)

    def __len__(self):
        # Tells PyTorch how big the dataset is
        return len(self.X)

    def __getitem__(self, idx):
        # Fetches exactly one pair of features and label by index
        sample_x = self.X[idx]
        sample_y = self.y[idx]
        return sample_x, sample_y

# Instantiate the dataset
dataset = CustomRegressionDataset(num_samples=1000)

# Create the DataLoader iterator
dataloader = DataLoader(
    dataset=dataset, 
    batch_size=32, 
    shuffle=True, 
    num_workers=0  # Set higher (e.g., 2 or 4) on real machines for parallel loading
)


# A simple 2-layer fully connected network
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(10, 5)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(5, 1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

# Check if GPU is available, else use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleNet().to(device)
criterion = nn.MSELoss()  # Mean Squared Error for regression
optimizer = optim.Adam(model.parameters(), lr=0.01)

epochs = 5

for epoch in range(epochs):
    model.train()  # 1. Set model to training mode (activates Dropout/BatchNorm behavior)
    running_loss = 0.0
    
    # 2. Iterate over batches provided by the DataLoader
    for batch_idx, (inputs, targets) in enumerate(dataloader):
        # 3. Move data tensors over to the target device (GPU or CPU)
        inputs, targets = inputs.to(device), targets.to(device)
        
        # 4. Clear old gradients from the previous step
        optimizer.zero_grad()
        
        # 5. Forward Pass: Compute model predictions
        outputs = model(inputs)
        
        # 6. Compute Loss: Measure prediction error
        loss = criterion(outputs, targets)
        
        # 7. Backward Pass: Compute gradients for every parameter
        loss.backward()
        
        # 8. Optimization Step: Update the model weights
        optimizer.step()
        
        # Track statistics
        running_loss += loss.item() * inputs.size(0)
        
    epoch_loss = running_loss / len(dataloader.dataset)
    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {epoch_loss:.4f}")
