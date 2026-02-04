"""
Breast Cancer + TERP + Free Energy
Run this script after TERP has completed optimization. It will output three figures:
1. bc_terp_energy_entropy_curve.png  — Energy-Entropy trajectory
2. bc_terp_free_energy_landscape.png — Free energy landscape 3D
3. bc_terp_feature_importance.png    — Important features bar chart
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.datasets import load_breast_cancer

plt.style.use("dark_background")


def load_terp_results(
    path_unf="TERP_results_2/unfaithfulness_scores_final.npy",
    path_S="TERP_results_2/interpretation_entropy_final.npy",
    path_opt="TERP_results_2/optimal_scores_unfaithfulness_interpretation_entropy.npy",
):
    """Load TERP output: U_j, S_j and optimal point (U*, S*)."""
    U = np.load(path_unf)
    S = np.load(path_S)
    try:
        optimal_scores = np.load(path_opt)
        U_star, S_star = optimal_scores
    except FileNotFoundError:
        # If optimal point file not found, find minimum zeta at fixed theta
        theta0 = 5.0
        zeta = U + theta0 * S
        j_star = np.argmin(zeta)
        U_star, S_star = U[j_star], S[j_star]
    return U, S, U_star, S_star


def plot_energy_entropy_curve(U, S, U_star, S_star):
    """Energy-Entropy trajectory, analogous to RG flow."""
    j_axis = np.arange(1, len(U) + 1)

    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(S, U, c=j_axis, cmap="viridis", s=40, zorder=3)
    ax.plot(S, U, color="#1f77b4", lw=1.5, alpha=0.7)

    ax.scatter([S_star], [U_star], c="red", s=80, zorder=5,
               label="Optimal interpretation")
    ax.annotate(
        r"$(S^*, U^*)$",
        xy=(S_star, U_star),
        xytext=(S_star + 0.02, U_star + 0.015),
        arrowprops=dict(arrowstyle="-", color="white"),
        fontsize=12,
    )

    ax.set_xlabel(r"Interpretation entropy $S_j$")
    ax.set_ylabel(r"Unfaithfulness $U_j$")
    ax.set_title("TERP: Energy–Entropy Trade-off (Breast Cancer)")
    ax.grid(alpha=0.2)
    cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Number of features $j$")
    ax.legend(frameon=False)

    plt.tight_layout()
    plt.savefig("bc_terp_energy_entropy_curve.png", dpi=300,
                bbox_inches="tight")
    plt.show()


def plot_free_energy_surface(U, S,
                             theta_min=0.0, theta_max=8.0, n_theta=80):
    """3D free energy landscape: zeta_j(theta) = U_j + theta * S_j."""
    U = np.asarray(U)
    S = np.asarray(S)
    j_axis = np.arange(1, len(U) + 1)

    theta_vals = np.linspace(theta_min, theta_max, n_theta)
    Theta, J = np.meshgrid(theta_vals, j_axis)

    U_rep = np.repeat(U.reshape(-1, 1), n_theta, axis=1)
    S_rep = np.repeat(S.reshape(-1, 1), n_theta, axis=1)

    Z = U_rep + Theta * S_rep  # zeta_j(theta)

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(
        Theta, J, Z,
        cmap=cm.plasma,
        linewidth=0,
        antialiased=True,
        alpha=0.95,
    )

    ax.set_xlabel(r"Temperature-like parameter $\theta$")
    ax.set_ylabel(r"Number of features $j$")
    ax.set_zlabel(r"Free-energy-like $\zeta_j(\theta)$")
    ax.set_title("TERP Free-Energy Landscape (Breast Cancer)")

    fig.colorbar(surf, shrink=0.6, aspect=12, label=r"$\zeta_j$")
    ax.grid(alpha=0.15)

    plt.tight_layout()
    plt.savefig("bc_terp_free_energy_landscape.png", dpi=300,
                bbox_inches="tight")
    plt.show()


def plot_feature_importance():
    """Plot bar chart of important features selected by TERP, with medical meaning."""
    data = load_breast_cancer()
    feature_names = data.feature_names
    w = np.load("TERP_results_2/optimal_feature_weights.npy")

    # Sort by absolute value, take top 10
    idx_sorted = np.argsort(-np.abs(w))
    top_k = 10
    top_idx = idx_sorted[:top_k]
    names = [feature_names[i] for i in top_idx]
    w_abs = np.abs(w[top_idx])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(names[::-1], w_abs[::-1], color="cyan")
    ax.set_xlabel("Absolute weight (importance)")
    ax.set_title("Top TERP Features (Breast Cancer)")
    plt.tight_layout()
    plt.savefig("bc_terp_feature_importance.png", dpi=300,
                bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    U, S, U_star, S_star = load_terp_results()
    plot_energy_entropy_curve(U, S, U_star, S_star)
    plot_free_energy_surface(U, S, theta_min=0.0, theta_max=8.0, n_theta=80)
    plot_feature_importance()
