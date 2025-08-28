import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader

class QuantumStateNN(nn.Module):
    """Neural network representing a quantum state"""
    def __init__(self, num_qubits, hidden_dim=128):
        super().__init__()
        self.num_qubits = num_qubits
        # Input is measurement basis configuration
        self.net = nn.Sequential(
            nn.Linear(num_qubits, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2),  # Outputs [real, imag] parts
            nn.Tanh()  # Keep outputs bounded
        )
        
    def forward(self, x):
        # x: batch_size × num_qubits (measurement basis)
        return self.net(x)
    
    def amplitude(self, basis_state):
        """Returns complex amplitude for a basis state"""
        # Convert binary basis state to measurement configuration
        config = torch.tensor([1 if b == '1' else -1 for b in basis_state], 
                            dtype=torch.float32)
        real, imag = self(config.unsqueeze(0))[0]
        return torch.complex(real, imag)

class EntanglementAwareLoss(nn.Module):
    """Custom loss that preserves quantum properties"""
    def __init__(self):
        super().__init__()
        
    def forward(self, predicted, target):
        # Preserve normalization
        norm_loss = torch.abs(1.0 - torch.sum(predicted**2))
        # Preserve entanglement patterns
        ent_loss = self.calculate_entanglement_loss(predicted)
        return norm_loss + ent_loss
    
    def calculate_entanglement_loss(self, state):
        # Measures how well entanglement is preserved
        # Implementation depends on specific entanglement metric
        return 0.0  # Placeholder

class QuantumSimulator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state_nn = QuantumStateNN(num_qubits)
        self.optimizer = optim.Adam(self.state_nn.parameters(), lr=0.001)
        self.loss_fn = EntanglementAwareLoss()
        
    def apply_gate(self, gate_matrix, qubit_indices):
        """Applies a quantum gate by adjusting the neural state"""
        # Convert gate operation into training data
        # Create training pairs (input_state, output_state_after_gate)
        # Then train the network to approximate the gate operation
        pass
        
    def measure(self, basis_states):
        """Returns probabilities of measuring each basis state"""
        with torch.no_grad():
            probs = []
            for state in basis_states:
                amp = self.state_nn.amplitude(state)
                probs.append(torch.abs(amp)**2)
            return torch.softmax(torch.tensor(probs), dim=0)
            
    def train_step(self, input_states, target_states):
        self.optimizer.zero_grad()
        outputs = self.state_nn(input_states)
        loss = self.loss_fn(outputs, target_states)
        loss.backward()
        self.optimizer.step()
        return loss.item()

# Example usage
if __name__ == "__main__":
    simulator = QuantumSimulator(num_qubits=4)
    
    # Simulate Hadamard on first qubit (create superposition)
    hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    simulator.apply_gate(hadamard, [0])
    
    # Simulate CNOT (create entanglement)
    cnot = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]])
    simulator.apply_gate(cnot, [0, 1])
    
    # Measure probabilities
    basis_states = ['0000', '0001', '0010', '0011', 
                   '0100', '0101', '0110', '0111',
                   '1000', '1001', '1010', '1011',
                   '1100', '1101', '1110', '1111']
    probs = simulator.measure(basis_states)
    print("Measurement probabilities:")
    for state, prob in zip(basis_states, probs):
        print(f"{state}: {prob:.4f}")