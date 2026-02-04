# 重整化群

[中文README](README_CN.md) | [English Notes](https://zhihangliu.cn/Renormalization-Group/en/) | [中文笔记合集](https://zhihangliu.cn/Renormalization-Group/)

![重整化群](docs/cn/assets/images/logo.png)

这是**重整化群（Renormalization Group, RG）**理论的自学笔记，涵盖临界现象、相变、标度律与普适类等内容。笔记以文章形式整理，并配有 [Python 代码](https://github.com/Liu-Zhihang/Renormalization-Group/tree/main/code) 以加深理解。

## 课程概述

重整化群是理论物理中最深刻的思想之一。它回答了一个核心问题：**为什么微观细节迥异的系统，在临界点附近会表现出相同的宏观行为？**

通过"粗粒化"——逐步消去短程自由度、只保留长程有效相互作用——RG揭示了不同微观系统如何在尺度变换下"流动"到同一个固定点，从而共享相同的临界指数。这种**普适性**是自然界最深刻的简化原理之一。

本系列教程从统计力学基础出发，逐步建立临界现象的定量语言，最终深入场论重整化群与现代前沿应用。

## 已完成笔记

### 第1部分：动机、统计物理与临界现象

- [1. 什么是重整化群](docs/cn/1.什么是重整化群.md)
- [2. 为什么需要重整化群](docs/cn/2.为什么需要重整化群.md)
- [3. 统计力学回顾：配分函数、自由能与涨落](docs/cn/3.统计力学回顾：配分函数、自由能与涨落.md)
- [4. 相变与临界指数：标度律与普适类（上）](docs/cn/4.相变与临界指数：标度律与普适类（上）.md)
- [5. 相变与临界指数：标度律与普适类（下）](docs/cn/5.相变与临界指数：标度律与普适类（下）.md)

## 规划主题

**第1部分：动机、统计物理与临界现象**（进行中）

- Landau 理论与 Ginzburg 判据——平均场的成功与失败
- 伊辛模型的世界——从 1D 精确解到 2D 临界点
- 块自旋与粗粒化——Kadanoff 的直观 RG 图像

**第2部分：实空间 RG 与数值方法**

- 实空间 RG 递推关系——相关维度与相图
- 有限尺寸标度与数据塌缩
- Monte Carlo 模拟伊辛模型——从 Metropolis 到簇算法
- Monte Carlo RG——从数值数据构造 RG 变换
- Ginzburg–Landau 泛函与连续场描述
- 从格点伊辛到 φ⁴ 场论

**第3部分：场论重整化群与量子场论**

- 路径积分与高斯场——从简谐振子到自由标量场
- φ⁴ 理论与费曼图——发散从哪里来？
- 重整化技术——正则化、反项与物理参数
- Callan–Symanzik 方程与 β 函数
- Wilson 视角的重整化群——"积出高动量模式"
- ε 展开与 Wilson–Fisher 固定点
- 量子场论中的 RG——QED、QCD 与渐近自由
- 非微扰重整化群——函数 RG 与大‑N 技巧

**第4部分：张量网络、DMRG、复杂网络与非平衡 RG**

- 密度矩阵重整化群（DMRG）与矩阵乘积态（MPS）
- 张量网络与多尺度纠缠重整化（MERA、TNR）
- 网络与图上的重整化群——从 Laplacian RG 到 Network RG
- 非平衡系统与主动物质中的 RG
- 量子引力、渐近安全与全息重整化群

**第5部分：RG × 机器学习 & 跨学科前沿**

- RG、信息论与参数压缩——从 Fisher 信息到"涌现理论"
- 深度学习与变分 RG——RBM、Neural RG 与互信息 RG
- 用深度学习"学会" RG——FRG+NN、Neural Tensor Network 等
- RG 在复杂系统与跨学科中的新方向介绍
- 前沿顶刊解读（贯穿教程）


## 使用说明

每个 Python 文件对应笔记中涵盖的特定主题。代码是理论概念的实践实现，作为自学笔记的一部分开发。

代码输出演示：

**[第2讲：为什么需要重整化群](docs/cn/2.为什么需要重整化群.md)**

| 2D Ising 模型临界现象 |
|:---:|
| ![2D Ising](docs/cn/assets/images/02_004_f0635ec7-cbcb-4d52-b32e-00add981f03e.jpg) |

*2D Ising 模型在不同温度下的构型：高温无序态、临界点附近的分形团簇、低温有序态*

**[第3讲：统计力学回顾——配分函数、自由能与涨落](docs/cn/3.统计力学回顾：配分函数、自由能与涨落.md)**

| 自由能景观 | 涨落-耗散关系 |
|:---:|:---:|
| ![Free Energy](docs/cn/assets/images/03_009_6747cc3f-112f-417b-baad-96162266f939.png) | ![Fluctuation](docs/cn/assets/images/03_010_052cde74-62ca-4229-b4e7-2b37f9713be8.png) |

*左：不同温度下的自由能景观，展示相变时对称性破缺；右：涨落-耗散定理的数值验证*

**[第4讲：相变与临界指数——标度律与普适类（上）](docs/cn/4.相变与临界指数：标度律与普适类（上）.md)**

| 序参量与响应函数 | 幂律分布与双对数图 |
|:---:|:---:|
| ![Order Parameter](docs/cn/assets/images/04_001_69ca0e9e-d7df-49ef-8901-c7c0a2f8c2ee.png) | ![Power Law](docs/cn/assets/images/04_002_88fc564e-4c7e-4568-9ef7-2cbd9d4248bc.png) |

**[第5讲：相变与临界指数——标度律与普适类（下）](docs/cn/5.相变与临界指数：标度律与普适类（下）.md)**

| 3D 渗流相变动画 |
|:---:|
| ![Percolation](docs/cn/assets/images/640.gif) |

*3D Site Percolation：随着占据概率 p 增加，团簇从孤立小点演化为贯穿系统的宏观网络*

| 有限尺寸标度分析 | 数据塌缩验证普适性 |
|:---:|:---:|
| ![FSS](docs/cn/assets/images/05_008_fc7d2fda-9a45-4db9-a7f7-56fe92cc5ba2.png) | ![Collapse](docs/cn/assets/images/05_006_ca25362d-8001-4e29-b7f4-d843b9c12158.png) |

*左：序参量和磁化率的有限尺寸标度分析；右：使用3D渗流临界指数成功实现数据塌缩*


## 许可证

本项目采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 许可。
