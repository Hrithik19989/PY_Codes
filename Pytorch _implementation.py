import torch
import torch.nn as nn

class ComplexMultiLayerNN(nn.Module):
    def __init__(self, input_dim: int, hidden_dims: list, output_dim: int, dropout_rate: float = 0.3):
        """
        A complex Deep Neural Network featuring flexible hidden layers,
        Batch Normalization, and Dropout Regularization.
        """
        super(ComplexMultiLayerNN, self).__init__()
        
        # We use nn.ModuleList to properly register a dynamic sequence of layers
        self.hidden_layers = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        
        # 1. Build the Input -> First Hidden Layer connection
        current_dim = input_dim
        for h_dim in hidden_dims:
            # Linear Transformation
            self.hidden_layers.append(nn.Linear(current_dim, h_dim))
            # Batch Normalization stabilizes training across deep structures
            self.batch_norms.append(nn.BatchNorm1d(h_dim))
            # Dropout combats overfitting in complex architectures
            self.dropouts.append(nn.Dropout(p=dropout_rate))
            current_dim = h_dim
            
        # 2. Build the Final Hidden -> Output Layer connection
        self.output_layer = nn.Linear(current_dim, output_dim)
        
        # 3. Activation Functions
        self.relu = nn.ReLU()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the computational graph and forward pass mechanics.
        """
        for linear, bn, dropout in zip(self.hidden_layers, self.batch_norms, self.dropouts):
            x = linear(x)      # Weight multiplication & bias addition
            x = bn(x)          # Normalize feature distributions
            x = self.relu(x)   # Introduce non-linearity
            x = dropout(x)     # Randomly zero out activations
            
        # Output layer raw logits (No activation here; handled by CrossEntropyLoss)
        logits = self.output_layer(x)
        return logits

# ==========================================
# 🛑 PIPELINE DEMONSTRATION & VERIFICATION
# ==========================================
if __name__ == "__main__":
    # 1. Hyperparameters & Configuration
    BATCH_SIZE = 32
    INPUT_FEATURES = 100
    HIDDEN_ARCHITECTURE = [512, 256, 128, 64]  # 4 Deep Hidden Layers
    NUM_CLASSES = 10                            # e.g., Multi-class Classification
    LEARNING_RATE = 0.001
    
    # Execution Device configuration
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Deploying network execution on: {device}")
    
    # 2. Instantiate Model, Loss Function, and Optimizer
    model = ComplexMultiLayerNN(
        input_dim=INPUT_FEATURES, 
        hidden_dims=HIDDEN_ARCHITECTURE, 
        output_dim=NUM_CLASSES,
        dropout_rate=0.25
    ).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    
    print("\n--- Model Architecture Topology ---")
    print(model)
    
    # 3. Generate Dummy Dataset
    mock_inputs = torch.randn(BATCH_SIZE, INPUT_FEATURES).to(device)
    mock_targets = torch.randint(0, NUM_CLASSES, (BATCH_SIZE,)).to(device)
    
    # 4. Single Optimization Step (Forward & Backward Pass)
    model.train() # Set to training state (activates Dropout & BatchNorm track)
    
    # Zero gradients from previous operations
    optimizer.zero_grad()
    
    # Forward Pass
    predictions = model(mock_inputs)
    loss = criterion(predictions, mock_targets)
    
    # Backward Pass (Autograd gradient computation)
    loss.backward()
    
    # Parameter update step
    optimizer.step()
    
    print("\n--- Verification Run ---")
    print(f"Input Shape:  {list(mock_inputs.shape)} -> [Batch Size, Features]")
    print(f"Output Shape: {list(predictions.shape)} -> [Batch Size, Target Classes]")
    print(f"Initial Optimization Loss value: {loss.item():.4f}")
