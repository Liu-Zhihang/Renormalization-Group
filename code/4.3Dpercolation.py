"""
Lecture 4 Practice Code: 3D Percolation Phase Transition Analysis and Visualization
================================================================
Features:
1. Monte Carlo simulation of 3D site percolation
2. Order parameter and susceptibility calculation with finite-size scaling analysis
3. Data collapse to verify universality class membership
4. Generate 3D visualization GIF of percolation cluster evolution

Author: Renormalization Group Lecture Series Companion Code
================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
import matplotlib.animation as animation
import os

# Set plotting style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'dejavusans'

# ============================================================
# Part 1: Union-Find Data Structure
# ============================================================
# Union-Find is an efficient data structure for handling connectivity problems.
# In percolation problems, we need to quickly determine whether two sites
# belong to the same cluster and merge clusters when adding new connections.
# With path compression and union by rank optimization, each operation has
# amortized time complexity close to O(1).

class UnionFind:
    """
    Union-Find data structure for efficient connected component computation.
    """
    def __init__(self, n):
        # parent[i] stores the parent node of node i
        # Initially each node is its own parent (i.e., each node forms a separate cluster)
        self.parent = list(range(n))
        # size[i] stores the size of the tree rooted at node i
        self.size = [1] * n
        # Track the current number of connected components
        self.n_components = n
    
    def find(self, x):
        """
        Find the root node of the cluster containing node x.
        Uses path compression optimization: directly connect all visited nodes to the root.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, a, b):
        """
        Merge the clusters containing nodes a and b.
        Uses union by rank optimization: attach smaller tree to larger tree for balance.
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # Already in the same cluster
        # Attach smaller tree to larger tree
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.n_components -= 1
        return True
    
    def get_cluster_sizes(self):
        """Get all cluster sizes, sorted in descending order"""
        cnt = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            cnt[root] += 1
        sizes = sorted(cnt.values(), reverse=True)
        return sizes
    
    def get_cluster_labels(self):
        """
        Return the cluster label for each node.
        Labels are sorted by cluster size: largest cluster has label 0, second largest has label 1, etc.
        """
        cluster_map = defaultdict(list)
        for i in range(len(self.parent)):
            root = self.find(i)
            cluster_map[root].append(i)
        
        # Sort clusters by size in descending order
        sorted_clusters = sorted(cluster_map.values(), key=len, reverse=True)
        labels = np.zeros(len(self.parent), dtype=int)
        for label, cluster in enumerate(sorted_clusters):
            for node in cluster:
                labels[node] = label
        return labels


# ============================================================
# Part 2: 3D Site Percolation Core Simulation Functions
# ============================================================
# 3D site percolation model: on an L x L x L cubic lattice, each site is
# "occupied" with probability p. If two adjacent sites are both occupied,
# they belong to the same connected cluster. When p exceeds the critical
# probability p_c = 0.3116, a macroscopic cluster spanning the entire
# system (percolating cluster) emerges.

def generate_percolation_config(L, p):
    """
    Generate a 3D site percolation configuration and compute connected clusters.
    
    Parameters:
        L: Linear size of the cubic lattice
        p: Occupation probability
    
    Returns:
        occupied: Boolean array indicating whether each site is occupied
        cluster_labels: Cluster label for each site (unoccupied sites have label -1)
        S1: Order parameter (relative size of largest cluster)
        chi: Susceptibility (second moment excluding largest cluster)
        sizes: List of all cluster sizes (descending order)
    """
    N = L * L * L
    # Randomly decide whether each site is occupied
    occupied = np.random.random(N) < p
    n_occupied = np.sum(occupied)
    
    # If no sites are occupied, return zero values
    if n_occupied == 0:
        return occupied, np.full(N, -1, dtype=int), 0, 0, []
    
    # Build index mapping for occupied sites
    # index_map: original index -> compressed index
    # reverse_map: compressed index -> original index
    occupied_indices = np.where(occupied)[0]
    index_map = {old: new for new, old in enumerate(occupied_indices)}
    reverse_map = {new: old for old, new in index_map.items()}
    
    # Build edge list: connect adjacent occupied sites
    edges = []
    for idx in occupied_indices:
        # Convert 1D index to 3D coordinates
        x, y, z = idx // (L*L), (idx // L) % L, idx % L
        # Check three positive direction neighbors
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if nx < L and ny < L and nz < L:
                nidx = nx * L * L + ny * L + nz
                if occupied[nidx]:
                    edges.append((index_map[idx], index_map[nidx]))
    
    # Use Union-Find to compute connected components
    uf = UnionFind(n_occupied)
    for a, b in edges:
        uf.union(a, b)
    
    sizes = uf.get_cluster_sizes()
    cluster_labels_occupied = uf.get_cluster_labels()
    
    # Map labels back to original index space
    cluster_labels = np.full(N, -1, dtype=int)
    for new_idx, old_idx in reverse_map.items():
        cluster_labels[old_idx] = cluster_labels_occupied[new_idx]
    
    # Compute physical quantities
    # Order parameter S1: fraction of total sites in largest cluster
    s1 = sizes[0] if sizes else 0
    S1 = s1 / N
    
    # Susceptibility chi: second moment excluding largest cluster
    # This measures fluctuations in "typical cluster size"
    chi = sum(s**2 for s in sizes[1:]) / N if len(sizes) > 1 else 0
    
    return occupied, cluster_labels, S1, chi, sizes


def compute_observables(L, p, n_samples=50):
    """
    Perform Monte Carlo sampling for given parameters, return mean and standard error of observables.
    
    Parameters:
        L: System linear size
        p: Occupation probability
        n_samples: Number of Monte Carlo samples
    
    Returns:
        S1_mean, chi_mean: Mean values of observables
        S1_err, chi_err: Standard errors
    """
    S1_list, chi_list = [], []
    
    for _ in range(n_samples):
        _, _, S1, chi, _ = generate_percolation_config(L, p)
        S1_list.append(S1)
        chi_list.append(chi)
    
    return (np.mean(S1_list), np.mean(chi_list),
            np.std(S1_list)/np.sqrt(n_samples),
            np.std(chi_list)/np.sqrt(n_samples))


# ============================================================
# Part 3: 3D Visualization and GIF Generation
# ============================================================
# Intuitively demonstrate the percolation phase transition through animation:
# as occupation probability p increases from low to high, observe how cluster
# structure evolves from isolated small dots to a large network spanning the system.

def create_percolation_gif(L=15, p_values=None, output_path='percolation_3d.gif'):
    """
    Generate a GIF animation of 3D percolation cluster evolution.
    
    The animation shows how cluster structure evolves as occupation probability p
    increases from low to high. The largest cluster is shown in red, other clusters in blue.
    
    Parameters:
        L: System linear size (recommend 10-20, larger is slow)
        p_values: Sequence of occupation probabilities to display
        output_path: Output GIF file path
    """
    if p_values is None:
        # Gradual transition from subcritical to supercritical
        p_values = np.linspace(0.15, 0.45, 30)
    
    # Use fixed random seed for animation continuity
    # This ensures consistency in site occupation across frames
    np.random.seed(42)
    base_random = np.random.random(L * L * L)
    
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    
    def update(frame):
        """Update plot for each frame"""
        fig.clear()
        ax = fig.add_subplot(111, projection='3d', facecolor='black')
        
        p = p_values[frame]
        # Determine occupation state based on base random numbers and current probability
        occupied = base_random < p
        
        # Compute cluster structure
        N = L * L * L
        n_occupied = np.sum(occupied)
        
        if n_occupied > 0:
            # Reuse logic from generate_percolation_config
            occupied_indices = np.where(occupied)[0]
            index_map = {old: new for new, old in enumerate(occupied_indices)}
            reverse_map = {new: old for old, new in index_map.items()}
            
            edges = []
            for idx in occupied_indices:
                x, y, z = idx // (L*L), (idx // L) % L, idx % L
                for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if nx < L and ny < L and nz < L:
                        nidx = nx * L * L + ny * L + nz
                        if occupied[nidx]:
                            edges.append((index_map[idx], index_map[nidx]))
            
            uf = UnionFind(n_occupied)
            for a, b in edges:
                uf.union(a, b)
            
            sizes = uf.get_cluster_sizes()
            cluster_labels_occupied = uf.get_cluster_labels()
            
            cluster_labels = np.full(N, -1, dtype=int)
            for new_idx, old_idx in reverse_map.items():
                cluster_labels[old_idx] = cluster_labels_occupied[new_idx]
            
            S1 = sizes[0] / N if sizes else 0
            chi = sum(s**2 for s in sizes[1:]) / N if len(sizes) > 1 else 0
        else:
            cluster_labels = np.full(N, -1, dtype=int)
            S1, chi = 0, 0
        
        # Plot occupied sites
        occupied_mask = occupied.reshape(L, L, L)
        labels_3d = cluster_labels.reshape(L, L, L)
        
        x, y, z = np.where(occupied_mask)
        
        if len(x) > 0:
            labels_flat = labels_3d[occupied_mask]
            
            # Color mapping: largest cluster in red, others in blue gradient
            colors = np.zeros((len(x), 4))
            for i, label in enumerate(labels_flat):
                if label == 0:  # Largest cluster
                    colors[i] = [1, 0.2, 0.2, 0.9]  # Red, high opacity
                else:
                    # Other clusters in blue tones, smaller clusters are darker
                    intensity = max(0.3, 1 - label * 0.03)
                    colors[i] = [0.2, 0.5, intensity, 0.6]
            
            ax.scatter(x, y, z, c=colors, s=60, depthshade=True)
        
        # Set axes
        ax.set_xlim(0, L)
        ax.set_ylim(0, L)
        ax.set_zlim(0, L)
        ax.set_xlabel('X', color='white', fontsize=12)
        ax.set_ylabel('Y', color='white', fontsize=12)
        ax.set_zlabel('Z', color='white', fontsize=12)
        
        # Set transparent background
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('gray')
        ax.yaxis.pane.set_edgecolor('gray')
        ax.zaxis.pane.set_edgecolor('gray')
        ax.tick_params(colors='white')
        
        # Determine current phase
        p_c = 0.3116
        if p < p_c - 0.03:
            phase = "Subcritical"
            phase_color = '#66CCFF'
        elif abs(p - p_c) <= 0.03:
            phase = "Critical"
            phase_color = '#FFFF66'
        else:
            phase = "Supercritical"
            phase_color = '#FF6666'
        
        # Title shows current parameters and observables
        title = f'3D Site Percolation (L={L})\n'
        title += f'p = {p:.3f}  |  $p_c$ = 0.3116  |  '
        ax.set_title(title, color='white', fontsize=14, pad=20)
        
        # Add observable information on the plot
        info_text = f'$S_1$ = {S1:.3f}\n$\\chi$ = {chi:.1f}\n{phase}'
        ax.text2D(0.02, 0.95, info_text, transform=ax.transAxes,
                  fontsize=12, color=phase_color, verticalalignment='top',
                  bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        # Rotate view angle for dynamic effect
        ax.view_init(elev=20, azim=frame * 4)
        
        return ax,
    
    print(f"Generating GIF animation ({len(p_values)} frames)...")
    print(f"  System size: L = {L}")
    print(f"  Probability range: p in [{p_values[0]:.2f}, {p_values[-1]:.2f}]")
    
    anim = animation.FuncAnimation(fig, update, frames=len(p_values), 
                                   interval=250, blit=False)
    anim.save(output_path, writer='pillow', fps=4, dpi=100)
    plt.close()
    print(f"GIF saved: {output_path}")


# ============================================================
# Part 4: Complete FSS Analysis Pipeline
# ============================================================

def run_fss_analysis(output_dir='.'):
    """
    Run complete finite-size scaling analysis and generate analysis plots.
    """
    print("=" * 70)
    print("3D Site Percolation Finite-Size Scaling Analysis")
    print("=" * 70)
    
    # Parameter settings
    p_c = 0.3116  # Critical probability for 3D site percolation
    p_values = np.linspace(0.20, 0.42, 25)
    L_values = [8, 12, 16, 20]
    n_samples = 50
    
    # 3D percolation critical exponents (literature values)
    beta = 0.41    # Order parameter exponent
    gamma = 1.80   # Susceptibility exponent
    nu = 0.88      # Correlation length exponent
    nu_bar = 3 * nu  # d * nu
    
    # Monte Carlo sampling
    print("\nRunning Monte Carlo simulation...")
    results = {L: {'p': [], 'S1': [], 'chi': [], 'S1_err': [], 'chi_err': []} 
               for L in L_values}
    
    for L in L_values:
        print(f"  L = {L}:", end=" ")
        for i, p in enumerate(p_values):
            S1, chi, S1_err, chi_err = compute_observables(L, p, n_samples)
            results[L]['p'].append(p)
            results[L]['S1'].append(S1)
            results[L]['chi'].append(chi)
            results[L]['S1_err'].append(S1_err)
            results[L]['chi_err'].append(chi_err)
            if (i + 1) % 10 == 0:
                print(f"{i+1}", end=" ")
        print("Done")
    
    # Generate analysis plots
    print("\nGenerating analysis plots...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(L_values)))
    
    # (a) Order parameter vs p
    ax1 = axes[0, 0]
    for L, color in zip(L_values, colors):
        ax1.errorbar(results[L]['p'], results[L]['S1'], 
                     yerr=results[L]['S1_err'],
                     label=f'L = {L}', color=color, marker='o', 
                     markersize=4, capsize=2, linewidth=1.5)
    ax1.axvline(p_c, color='red', linestyle='--', label=f'$p_c$ = {p_c}', alpha=0.7)
    ax1.set_xlabel('Occupation probability $p$', fontsize=12)
    ax1.set_ylabel('Order parameter $S_1$', fontsize=12)
    ax1.set_title('(a) Order Parameter vs Occupation Probability', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(alpha=0.3)
    
    # (b) Susceptibility vs p
    ax2 = axes[0, 1]
    for L, color in zip(L_values, colors):
        ax2.errorbar(results[L]['p'], results[L]['chi'], 
                     yerr=results[L]['chi_err'],
                     label=f'L = {L}', color=color, marker='s', 
                     markersize=4, capsize=2, linewidth=1.5)
    ax2.axvline(p_c, color='red', linestyle='--', label=f'$p_c$ = {p_c}', alpha=0.7)
    ax2.set_xlabel('Occupation probability $p$', fontsize=12)
    ax2.set_ylabel('Susceptibility $\\chi$', fontsize=12)
    ax2.set_title('(b) Susceptibility vs Occupation Probability', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(alpha=0.3)
    
    # (c) S1 data collapse
    ax3 = axes[1, 0]
    for L, color in zip(L_values, colors):
        N = L ** 3
        p_arr = np.array(results[L]['p'])
        S1_arr = np.array(results[L]['S1'])
        x_scaled = (p_arr - p_c) * N ** (1/nu_bar)
        y_scaled = S1_arr * N ** (beta/nu_bar)
        ax3.scatter(x_scaled, y_scaled, label=f'L = {L}', color=color, s=40, alpha=0.8)
    ax3.axvline(0, color='white', linestyle=':', alpha=0.5)
    ax3.set_xlabel('$(p - p_c) N^{1/\\bar{\\nu}}$', fontsize=12)
    ax3.set_ylabel('$S_1 \\cdot N^{\\beta/\\bar{\\nu}}$', fontsize=12)
    ax3.set_title(f'(c) Data Collapse for $S_1$ ($\\beta$={beta}, $\\bar{{\\nu}}$={nu_bar:.2f})', fontsize=14)
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # (d) chi data collapse
    ax4 = axes[1, 1]
    for L, color in zip(L_values, colors):
        N = L ** 3
        p_arr = np.array(results[L]['p'])
        chi_arr = np.array(results[L]['chi'])
        x_scaled = (p_arr - p_c) * N ** (1/nu_bar)
        y_scaled = chi_arr * N ** (-gamma/nu_bar)
        ax4.scatter(x_scaled, y_scaled, label=f'L = {L}', color=color, s=40, alpha=0.8)
    ax4.axvline(0, color='white', linestyle=':', alpha=0.5)
    ax4.set_xlabel('$(p - p_c) N^{1/\\bar{\\nu}}$', fontsize=12)
    ax4.set_ylabel('$\\chi \\cdot N^{-\\gamma/\\bar{\\nu}}$', fontsize=12)
    ax4.set_title(f'(d) Data Collapse for $\\chi$ ($\\gamma$={gamma}, $\\bar{{\\nu}}$={nu_bar:.2f})', fontsize=14)
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.suptitle('3D Site Percolation: Finite-Size Scaling Analysis', fontsize=16, y=1.02)
    
    fig_path = os.path.join(output_dir, 'percolation_fss_analysis.png')
    plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"FSS analysis plot saved: {fig_path}")
    
    # Output scaling law verification
    print("\n" + "=" * 70)
    print("Scaling Law Verification")
    print("=" * 70)
    alpha_perc = -0.62
    print(f"\n3D Percolation Critical Exponents (Literature Values):")
    print(f"  beta = {beta}, gamma = {gamma}, nu = {nu}, alpha = {alpha_perc}")
    
    rushbrooke = alpha_perc + 2*beta + gamma
    print(f"\nRushbrooke Scaling Law: alpha + 2*beta + gamma = {rushbrooke:.2f} (Theoretical value: 2)")
    print(f"Hyperscaling: d*nu = {3*nu:.2f}, 2-alpha = {2-alpha_perc:.2f}")
    
    return results


def main():
    """Main function: run complete analysis pipeline"""
    print("\n" + "=" * 70)
    print("3D Percolation Phase Transition Analysis and Visualization")
    print("=" * 70)
    
    # Set output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run FSS analysis
    print("\n[1/2] Running finite-size scaling analysis...")
    run_fss_analysis(output_dir)
    
    # Generate GIF animation
    print("\n[2/2] Generating 3D visualization animation...")
    gif_path = os.path.join(output_dir, 'percolation_3d.gif')
    create_percolation_gif(L=15, output_path=gif_path)
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
