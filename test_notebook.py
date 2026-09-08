import sys
sys.path.insert(0, 'src')
import torch
import yaml
import numpy as np
from models.decoder_only_transformer import DecoderOnlyTransformer
import experiments.exp6_capstone as exp6
import experiments.exp1_induction_heads as exp1
import experiments.exp4_circuit_patching as exp4
import experiments.exp5_sae_dashboard as exp5
from torch.utils.data import DataLoader, TensorDataset

# Load config from YAML
with open('configs/capstone.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

# Load checkpoint
ckpt_path = 'checkpoints/exp6_capstone_seed0_step2000.pt'
ckpt = torch.load(ckpt_path, map_location='cpu')

# Recreate model
task_cfg = cfg['task']
model_cfg = cfg['model']
vocab_size = task_cfg['induction']['vocab_size'] + task_cfg['modular']['modulus'] + 10
model = DecoderOnlyTransformer(
    vocab_size=vocab_size,
    d_model=model_cfg['d_model'],
    n_layers=model_cfg['n_layers'],
    n_heads=model_cfg['n_heads'],
    d_mlp=model_cfg['d_mlp'],
    dropout=model_cfg['dropout'],
    rotary_base=model_cfg['rotary_base'],
    rmsnorm_eps=model_cfg['rmsnorm_eps'],
).to('cpu')
model.load_state_dict(ckpt['model'])
model.eval()

print('Model loaded:', sum(p.numel() for p in model.parameters()), 'parameters')

# Batch size from training config
batch_size = cfg['training']['batch_size']

# Cell 2: Fourier - pass tensor directly (function handles detach)
modular_offset = task_cfg['modular'].get('vocab_offset', 0)
modulus = task_cfg['modular']['modulus']
embed_weights = model.embed.weight[modular_offset:modular_offset+modulus]
fourier_result = exp6.fourier_decomposition(embed_weights, modulus)

# Analyze sparsity
sparsity_result = exp6.analyze_fourier_sparsity(fourier_result['fourier_magnitudes'], modulus)
print('Fourier k_99 (mean):', sparsity_result['k_99_mean'], '/', modulus)
print('Fourier k_90 (mean):', sparsity_result['k_90_mean'], '/', modulus)
print('Fourier sparsity:', fourier_result.get('sparsity', 'N/A'))

# Cell 3: K-composition - use RoundRobinDataLoader (proper induction batches with task_id=1)
induction_cfg = task_cfg['induction']
_, ind_val = exp1.make_repeated_token_data(
    vocab_size=induction_cfg['vocab_size'],
    seq_len=induction_cfg['seq_len'],
    num_train=induction_cfg['num_train'],
    num_val=induction_cfg['num_val'],
    prefix_ratio=induction_cfg['prefix_ratio'],
    seed=cfg.get('seed', 0) + 1000
)
ind_val_loader = DataLoader(ind_val, batch_size=batch_size, shuffle=False)

# Create RoundRobin with only induction (task_id=1)
class InductionOnlyRoundRobin:
    def __init__(self, loader):
        self.loader = loader
        self.iterator = iter(loader)
    def __iter__(self):
        self.iterator = iter(self.loader)
        return self
    def __next__(self):
        x, y = next(self.iterator)
        return x, y, None, 1  # task_id=1 for induction
    def __len__(self):
        return len(self.loader)

induction_only_loader = InductionOnlyRoundRobin(ind_val_loader)

with torch.no_grad():
    kcomp_result = exp6.compute_k_composition_scores(model, induction_only_loader, num_batches=5)
print('K-comp result keys:', list(kcomp_result.keys()))
# Find max kcomp value
kcomp_values = [v for k, v in kcomp_result.items() if not k.startswith('_')]
if kcomp_values:
    print('Max K-comp:', max(kcomp_values))
else:
    print('Max K-comp: N/A')
print('_vacuous:', kcomp_result.get('_vacuous', False))
print('_diagnosis_step2:', kcomp_result.get('_diagnosis_step2', 'N/A'))
print('_diagnosis_step1_max:', kcomp_result.get('_diagnosis_step1_max', 'N/A'))
print('_diagnosis_best_pair:', kcomp_result.get('_diagnosis_best_pair', 'N/A'))

# Note: DecoderOnlyTransformer doesn't support record_attn like AttentionOnlyTransformer
# So diag+1 mass is not directly computable. The K-comp Step 1 diagnosis gives similar info.
print('\nNote: diag+1 mass requires AttentionOnlyTransformer (exp1) with record_attn=True.')
print('K-comp Step 1 diagnosis (max duplicate mass):', kcomp_result.get('_diagnosis_step1_max', 'N/A'))

# Cell 4: Circuit patching
# Create clean and corrupted induction batches using proper function
clean_data = exp1.make_repeated_token_data(
    vocab_size=induction_cfg['vocab_size'],
    seq_len=induction_cfg['seq_len'],
    num_train=batch_size,
    num_val=batch_size,
    prefix_ratio=induction_cfg['prefix_ratio'],
    seed=cfg.get('seed', 0)
)
clean_x, clean_y = clean_data[0].tensors
clean_answer = clean_y[:, -1]

corrupted_data = exp1.make_repeated_token_data(
    vocab_size=induction_cfg['vocab_size'],
    seq_len=induction_cfg['seq_len'],
    num_train=batch_size,
    num_val=batch_size,
    prefix_ratio=induction_cfg['prefix_ratio'],
    seed=cfg.get('seed', 0) + 2
)
corrupted_x, corrupted_y = corrupted_data[0].tensors
corrupted_answer = corrupted_y[:, -1]

# Patch all layers at the last position (where induction happens)
layers_to_patch = list(range(model.n_layers))
positions_to_patch = [induction_cfg['seq_len'] - 2]  # second-to-last position

act_patch_result = exp4.run_activation_patching(
    model,
    clean_x,
    clean_answer,
    corrupted_x,
    corrupted_answer,
    layers_to_patch=layers_to_patch,
    positions_to_patch=positions_to_patch,
)
# Results is dict mapping (layer, pos) -> {clean_diff, patched_diff, recovery}
recoveries = [v['recovery'] for v in act_patch_result.values()]
mean_recovery = np.mean(recoveries)
print('Activation patching recovery (mean):', mean_recovery)
print('Activation patching per (layer, pos):', {k: v['recovery'] for k, v in act_patch_result.items()})

# Path patching: test all heads in layers 0-3
heads_to_test = [(l, h) for l in range(model.n_layers) for h in range(model.n_heads)]
path_patch_result = exp4.run_path_patching_to_logits(
    model,
    clean_x,
    clean_answer,
    corrupted_x,
    corrupted_answer,
    heads=heads_to_test,
    pos=induction_cfg['seq_len'] - 2,
)
print('Path patching result keys:', list(path_patch_result.keys()))
path_recovery = path_patch_result.get('mean_recovery', 0.0)
print('Path patching recovery (mean):', path_recovery)
print('Path patching _vacuous:', path_patch_result.get('_vacuous', False))

# Cell 5: SAE
# Create a dataloader for activation harvesting
harvest_data = exp1.make_repeated_token_data(
    vocab_size=induction_cfg['vocab_size'],
    seq_len=induction_cfg['seq_len'],
    num_train=1000,
    num_val=100,
    prefix_ratio=induction_cfg['prefix_ratio'],
    seed=cfg.get('seed', 0) + 100
)
harvest_loader = DataLoader(harvest_data[0], batch_size=32, shuffle=True)

activations_dict = exp6.harvest_activations(model, harvest_loader, hooks=["ln_final"], max_tokens=5000)
activations = activations_dict['ln_final']
print('Activations shape:', activations.shape)

# Create SAE model
sae_model = exp5.SparseAutoencoder(d_model=activations.shape[-1], n_features=256)

# Create DataLoader for SAE training
sae_loader = DataLoader(TensorDataset(activations, torch.zeros(activations.shape[0])), batch_size=32, shuffle=True)

sae_history = exp5.train_sae(
    sae_model,
    sae_loader,
    epochs=5000,
    lr=1e-3,
    l1_coeff=1e-3,
    seed=42
)

# Extract final metrics
final_mse = sae_history['mse'][-1]
final_l0 = sae_history['l0'][-1]
print('SAE MSE:', final_mse)
print('SAE L0:', final_l0, '/ 256')

# Compute FVE
with torch.no_grad():
    recon, latent = sae_model(activations.to('cpu'))
    mse = torch.nn.functional.mse_loss(recon, activations).item()
    total_var = activations.var().item()
    fve = 1 - mse / total_var if total_var > 0 else 0
    print('SAE FVE:', fve)
    dead = (latent.abs().sum(dim=0) < 1e-4).sum().item()
    print('SAE Dead features:', dead, '/ 256')

print('All cells executed successfully!')