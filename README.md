# Renormalization Group

[中文README](README_CN.md) | [English Notes](https://zhihangliu.cn/Renormalization-Group/en/) | [中文笔记合集](https://zhihangliu.cn/Renormalization-Group/)

<p align="center">
  <img src="docs/cn/assets/images/logo.png" alt="Renormalization Group" width="400">
</p>

This repository contains self-study notes on **Renormalization Group (RG)** theory, covering critical phenomena, phase transitions, scaling laws, and universality classes. Notes are organized as articles with accompanying [Python code](https://github.com/Liu-Zhihang/Renormalization-Group/tree/main/code) for deeper understanding.

## Course Overview

The renormalization group was born from puzzles over divergent integrals and critical phenomena, yet within half a century it has evolved into a general language for understanding nature. From fundamental particle interactions to starlings swirling in the sky, from layer-by-layer weights in neural networks to fluctuations in Earth's climate, RG thinking pervades the study of multi-scale complex systems. Macroscopic laws are not simple superpositions of microscopic rules, but emergent products of scale transformations. Through RG, we gain insight into why vastly different systems share the same behavioral principles and how to extract the factors governing the whole from a welter of details.

The common challenge of these multi-scale systems is this: when the correlation length tends to diverge, the traditional "separation of scales" assumption completely breaks down—local fluctuations no longer cancel out, but are amplified layer by layer through long-range correlations, coupling directly to macroscopic observables. Facing strong correlations among $10^{23}$ degrees of freedom, the **Renormalization Group** adopts a "divide and conquer" strategy: progressively reducing short-range degrees of freedom, tracking how system parameters "flow" with observation scale, and ultimately converging to fixed points that govern macroscopic behavior.

It is precisely this flow that explains the origin of **universality**—why systems with vastly different microscopic mechanisms share the same critical exponents. Kenneth Wilson received the 1982 Nobel Prize in Physics for developing this theory. This tutorial series starts from the physical picture of critical phenomena, establishes statistical mechanics foundations, introduces the quantitative language of scaling laws and critical exponents, and ultimately delves into field-theoretic renormalization group and modern frontier applications.

## Completed Notes

### Part 1: Motivation, Statistical Physics, and Critical Phenomena

- [1. What Is the Renormalization Group](docs/en/1.%20What%20Is%20the%20Renormalization%20Group.md)
- [2. Why Do We Need the Renormalization Group](docs/en/2.%20Why%20Do%20We%20Need%20the%20Renormalization%20Group.md)
- [3. Statistical Mechanics Review: Partition Function, Free Energy, and Fluctuations](docs/en/3.%20Statistical%20Mechanics%20Review%20-%20Partition%20Function%2C%20Free%20Energy%2C%20and%20Fluctuations.md)
- [4. Phase Transitions and Critical Exponents: Scaling Laws and Universality Classes (Part I)](docs/en/4.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20I%29.md)
- [5. Phase Transitions and Critical Exponents: Scaling Laws and Universality Classes (Part II)](docs/en/5.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20II%29.md)

## Planned Topics

**Part 1: Motivation, Statistical Physics, and Critical Phenomena** (In Progress)

- Landau Theory and Ginzburg Criterion—Success and Failure of Mean Field
- The World of the Ising Model—From 1D Exact Solution to 2D Critical Point
- Block Spins and Coarse-Graining—Kadanoff's Intuitive RG Picture

**Part 2: Real-Space RG and Numerical Methods**

- Real-Space RG Recursion Relations—Relevant Dimensions and Phase Diagrams
- Finite-Size Scaling and Data Collapse
- Monte Carlo Simulation of the Ising Model—From Metropolis to Cluster Algorithms
- Monte Carlo RG—Constructing RG Transformations from Numerical Data
- Ginzburg-Landau Functional and Continuum Field Description
- From Lattice Ising to φ⁴ Field Theory

**Part 3: Field-Theoretic RG and Quantum Field Theory**

- Path Integrals and Gaussian Fields—From Harmonic Oscillator to Free Scalar Field
- φ⁴ Theory and Feynman Diagrams—Where Do Divergences Come From?
- Renormalization Techniques—Regularization, Counterterms, and Physical Parameters
- Callan-Symanzik Equation and β Function
- Wilson's Perspective on RG—"Integrating Out High-Momentum Modes"
- ε Expansion and Wilson-Fisher Fixed Point
- RG in Quantum Field Theory—QED, QCD, and Asymptotic Freedom
- Non-Perturbative RG—Functional RG and Large-N Techniques

**Part 4: Tensor Networks, DMRG, Complex Networks, and Non-Equilibrium RG**

- Density Matrix Renormalization Group (DMRG) and Matrix Product States (MPS)
- Tensor Networks and Multiscale Entanglement Renormalization (MERA, TNR)
- RG on Networks and Graphs—From Laplacian RG to Network RG
- RG in Non-Equilibrium Systems and Active Matter
- Quantum Gravity, Asymptotic Safety, and Holographic RG

**Part 5: RG × Machine Learning & Interdisciplinary Frontiers**

- RG, Information Theory, and Parameter Compression—From Fisher Information to "Emergent Theory"
- Deep Learning and Variational RG—RBM, Neural RG, and Mutual Information RG
- Learning RG with Deep Learning—FRG+NN, Neural Tensor Network, etc.
- New Directions of RG in Complex Systems and Interdisciplinary Applications
- Cutting-Edge Paper Reviews (Throughout the Tutorial)


## Usage

Each Python file corresponds to a specific topic covered in the notes. The code serves as practical implementation of theoretical concepts, developed as part of self-study notes.

Code Output Demonstrations:

**[Lecture 2: Why Do We Need the Renormalization Group](docs/en/2.%20Why%20Do%20We%20Need%20the%20Renormalization%20Group.md)**

| Real-Space Renormalization Group Flow |
|:---:|
| ![RG Flow](docs/cn/assets/images/02_001_0bd1b135-4629-48b8-8c04-0c6c07d7fa85.png) |

*Kadanoff block spin coarse-graining: 128×128 → 64×64 → 32×32, microscopic fluctuations fade away as macroscopic order emerges*

**[Lecture 3: Statistical Mechanics Review—Partition Function, Free Energy, and Fluctuations](docs/en/3.%20Statistical%20Mechanics%20Review%20-%20Partition%20Function%2C%20Free%20Energy%2C%20and%20Fluctuations.md)**

| Energy-Entropy Trade-off | Free Energy Landscape | Feature Importance |
|:---:|:---:|:---:|
| ![Energy-Entropy](docs/cn/assets/images/03_013_61356d55-a582-4d0d-9573-1fe7b8951f6f.png) | ![Free Energy](docs/cn/assets/images/03_014_32518e6d-8931-4aa3-8f92-18d0a8a81d5d.png) | ![Features](docs/cn/assets/images/03_015_5840452a-3546-4405-9788-9487a0caef94.png) |

*TERP Explainable AI: Using thermodynamic free energy principles to find optimal explanations—energy-entropy trade-off, free energy landscape, and key feature ranking*

**[Lecture 5: Phase Transitions and Critical Exponents—Scaling Laws and Universality Classes (Part II)](docs/en/5.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20II%29.md)**

| 3D Percolation Animation | Finite-Size Scaling Analysis |
|:---:|:---:|
| ![Percolation](docs/cn/assets/images/640.gif) | ![FSS](docs/cn/assets/images/05_008_fc7d2fda-9a45-4db9-a7f7-56fe92cc5ba2.png) |

*Left: 3D Site Percolation cluster evolution animation; Right: Finite-size scaling analysis of order parameter and susceptibility*


## License

This project is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

## Citation

If you use or reference these notes, we welcome a citation. BibTeX format:

```bibtex
@misc{liu2024renormalization,
  author       = {Liu, Zhihang},
  title        = {Renormalization Group},
  year         = {2025},
  url          = {https://github.com/Liu-Zhihang/Renormalization-Group},
  note         = {Self-study notes on critical phenomena, phase transitions, scaling laws and universality classes}
}
```
