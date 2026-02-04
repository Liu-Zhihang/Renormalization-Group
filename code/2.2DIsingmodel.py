import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


plt.style.use('dark_background')

class IsingRG:
    """
    2D Ising Model and Renormalization Group Flow Simulator
    """
    def __init__(self, L=64, T=2.27):
        self.L = L
        self.T = T
        # Initialize random state (+1 or -1)
        self.lattice = np.random.choice([-1, 1], size=(L, L))
        
    def energy_change(self, i, j):
        """
        Calculate energy change from flipping a spin (periodic boundary conditions)
        E = -J * sum(s_i * s_j), with J=1
        """
        top = self.lattice[(i - 1) % self.L, j]
        bottom = self.lattice[(i + 1) % self.L, j]
        left = self.lattice[i, (j - 1) % self.L]
        right = self.lattice[i, (j + 1) % self.L]
        neighbors = top + bottom + left + right
        # dE = E_new - E_old = -(-s) * neighbors - (-s * neighbors) = 2 * s * neighbors
        return 2 * self.lattice[i, j] * neighbors

    def metropolis_step(self):
        """Perform one Metropolis Monte Carlo sweep"""
        # Attempt L*L flips, this is called one MCS (Monte Carlo Sweep)
        for _ in range(self.L * self.L):
            i = np.random.randint(0, self.L)
            j = np.random.randint(0, self.L)
            dE = self.energy_change(i, j)
            
            # Metropolis criterion: accept if energy decreases, or with Boltzmann probability if increases
            if dE <= 0 or np.random.rand() < np.exp(-dE / self.T):
                self.lattice[i, j] *= -1

    def simulate(self, steps=1000):
        """Thermalize the system"""
        for _ in range(steps):
            self.metropolis_step()

    def coarse_grain(self, block_size=2):
        """
        Perform Kadanoff block spin transformation (majority rule)
        """
        new_L = self.L // block_size
        new_lattice = np.zeros((new_L, new_L))
        
        for i in range(new_L):
            for j in range(new_L):
                # Extract block_size x block_size block
                block = self.lattice[i*block_size:(i+1)*block_size, 
                                   j*block_size:(j+1)*block_size]
                # Majority rule
                avg_spin = np.sum(block)
                if avg_spin > 0:
                    new_lattice[i, j] = 1
                elif avg_spin < 0:
                    new_lattice[i, j] = -1
                else:
                    # If tied, choose randomly
                    new_lattice[i, j] = np.random.choice([-1, 1])
        return new_lattice

def plot_rg_flow():
    # 2D Ising model critical temperature Tc = 2/ln(1+sqrt(2)) = 2.269
    # We simulate slightly above Tc to observe correlation length
    sim = IsingRG(L=128, T=2.3) 
    print("Equilibrating system near critical point (this may take a few seconds)...")
    sim.simulate(steps=1500)  # Ensure proper thermalization
    
    original = sim.lattice
    # First renormalization step
    rg_1 = sim.coarse_grain(block_size=2)
    
    # Prepare for second renormalization step by creating a new instance
    # For demonstration simplicity, we directly process rg_1
    # Note: Actually evolution should be under the renormalized Hamiltonian
    # This shows configuration space flow through "snapshots"
    rg_2_dummy = IsingRG(L=64, T=2.3) 
    rg_2_dummy.lattice = rg_1
    rg_final = rg_2_dummy.coarse_grain(block_size=2)  # Equivalent to 4x4 blocks in original lattice
    
    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    # Use dark purple/yellow colormap for high contrast and dark theme compatibility
    cmap = colors.ListedColormap(['#440154', '#fde725']) 
    
    axes[0].imshow(original, cmap=cmap, interpolation='nearest')
    axes[0].set_title(f"Original Lattice ({128}x{128})\nMicroscopic Fluctuations", color='white')
    axes[0].axis('off')
    
    axes[1].imshow(rg_1, cmap=cmap, interpolation='nearest')
    axes[1].set_title(f"First RG Step (b=2)\n{64}x{64}", color='white')
    axes[1].axis('off')
    
    axes[2].imshow(rg_final, cmap=cmap, interpolation='nearest')
    axes[2].set_title(f"Second RG Step (b=4)\n{32}x{32}", color='white')
    axes[2].axis('off')
    
    plt.suptitle("Real-Space Renormalization Group Flow: Emergence of Macroscopic Order", 
                 fontsize=16, color='white', y=1.05)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_rg_flow()
