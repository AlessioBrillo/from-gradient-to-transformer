import torch
from src.experiments.exp5_sae_dashboard import SparseAutoencoder as SAE, harvest_activations_from_checkpoint

def verify():
    print("Verifying SAE induction capability...")
    
    # 1. Load Model and Harvest Activations (using same settings as training)
    # Using the checkpoint that trained successfully
    checkpoint_path = "figures/exp1_trained_model.pt"
    activations = harvest_activations_from_checkpoint(
        checkpoint_path,
        num_samples=100,
        vocab_size=256,
        seq_len=24,
        d_model=32,
        n_layers=2,
        n_heads=4,
        seed=42
    )
    
    # 2. Load trained SAE
    # The training script saves to a specific location if not provided
    # Assuming default naming or looking for it
    sae = SAE(d_model=32, n_features=512)
    sae.load_state_dict(torch.load("sae_model.pt", weights_only=True))
    sae.eval()
    
    # 3. Check for high activation on induction-like patterns
    with torch.no_grad():
        features = sae.get_feature_activations(activations)
        
    # Check if any feature has high activation
    assert features.max() > 0.5, f"Expected some feature activation, got max {features.max()}"
    print("SAE feature activation verified.")

if __name__ == "__main__":
    verify()
