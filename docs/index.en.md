# Renormalization Group

![Renormalization Group](cn/assets/images/logo.png)

These are self-study notes on **Renormalization Group (RG)** theory, covering critical phenomena, phase transitions, scaling laws, and universality classes. Notes are organized as articles with accompanying [Python code](https://github.com/Liu-Zhihang/Renormalization-Group/tree/main/code) for deeper understanding.

## Course Overview

The renormalization group is one of the most profound ideas in theoretical physics. It answers a core question: **Why do systems with vastly different microscopic details exhibit the same macroscopic behavior near critical points?**

Through "coarse-graining"—progressively eliminating short-range degrees of freedom while retaining long-range effective interactions—RG reveals how different microscopic systems "flow" to the same fixed point under scale transformations, thereby sharing identical critical exponents. This **universality** is one of nature's most profound simplification principles.

This tutorial series starts from statistical mechanics foundations, progressively builds the quantitative language of critical phenomena, and ultimately delves into field-theoretic renormalization group and modern frontier applications.

## Completed Notes

### Part 1: Motivation, Statistical Physics, and Critical Phenomena

- [1. What Is the Renormalization Group](en/1.%20What%20Is%20the%20Renormalization%20Group.md)
- [2. Why Do We Need the Renormalization Group](en/2.%20Why%20Do%20We%20Need%20the%20Renormalization%20Group.md)
- [3. Statistical Mechanics Review: Partition Function, Free Energy, and Fluctuations](en/3.%20Statistical%20Mechanics%20Review%20-%20Partition%20Function%2C%20Free%20Energy%2C%20and%20Fluctuations.md)
- [4. Phase Transitions and Critical Exponents: Scaling Laws and Universality Classes (Part I)](en/4.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20I%29.md)
- [5. Phase Transitions and Critical Exponents: Scaling Laws and Universality Classes (Part II)](en/5.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20II%29.md)

## Code Demonstrations

**[Lecture 2: Why Do We Need the Renormalization Group](en/2.%20Why%20Do%20We%20Need%20the%20Renormalization%20Group.md)**

| Real-Space Renormalization Group Flow |
|:---:|
| ![RG Flow](cn/assets/images/02_001_0bd1b135-4629-48b8-8c04-0c6c07d7fa85.png) |

*Kadanoff block spin coarse-graining: 128×128 → 64×64 → 32×32, microscopic fluctuations fade away as macroscopic order emerges*

**[Lecture 3: Statistical Mechanics Review—Partition Function, Free Energy, and Fluctuations](en/3.%20Statistical%20Mechanics%20Review%20-%20Partition%20Function%2C%20Free%20Energy%2C%20and%20Fluctuations.md)**

| Energy-Entropy Trade-off | Free Energy Landscape | Feature Importance |
|:---:|:---:|:---:|
| ![Energy-Entropy](cn/assets/images/03_013_61356d55-a582-4d0d-9573-1fe7b8951f6f.png) | ![Free Energy](cn/assets/images/03_014_32518e6d-8931-4aa3-8f92-18d0a8a81d5d.png) | ![Features](cn/assets/images/03_015_5840452a-3546-4405-9788-9487a0caef94.png) |

*TERP Explainable AI: Using thermodynamic free energy principles to find optimal explanations*

**[Lecture 5: Phase Transitions and Critical Exponents—Scaling Laws and Universality Classes (Part II)](en/5.%20Phase%20Transitions%20and%20Critical%20Exponents%20-%20Scaling%20Laws%20and%20Universality%20Classes%20%28Part%20II%29.md)**

| 3D Percolation Animation | Finite-Size Scaling Analysis |
|:---:|:---:|
| ![Percolation](cn/assets/images/640.gif) | ![FSS](cn/assets/images/05_008_fc7d2fda-9a45-4db9-a7f7-56fe92cc5ba2.png) |

*Left: 3D Site Percolation cluster evolution; Right: Finite-size scaling analysis*


## License

This project is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).
