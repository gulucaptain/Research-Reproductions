# VirtualRect：方法与复现边界

审阅日期：2026-11-17。依据 arXiv:2611.10518v1 的完整 PDF、HTML 与 TeX 源码，以及 RsCeR 的 CVPR 2025 论文。公开 v1 共 13 页（10 页正文、3 页参考文献），源码压缩包无附录文件或实现；不能声称已阅读尚未取得的会议补充材料。会议入口指向 OpenReview bWCyY4WYr9，当前受浏览器验证限制。

## 输入输出与创新所在

输入是双目图像、已知输入内参及用于尺度换算的基线。输出为两个校正变换和共同的虚拟相机内参。它不是未知内参的通用自标定，也不是无需训练的逐图优化：几何求解在线进行，匹配器与预测头需要学习。

流程为 Efficient LoFTR 匹配 → RANSAC 选择内点 → 五自由度加权几何重拟合 → 共同虚拟相机部署 → 固定立体匹配器计算视差 → 使用对应相机参数计算深度。

本文在 RsCeR 的匹配和受约束求解之上，增加全图单应变换监督、内点可靠性校准、输出虚拟相机的一致部署。新意并非发明双目校正或 Z=fB/d，而是把这些环节纳入学习与评价。

## 可明确实现的几何

RsCeR Eq. 11 给出五参数 theta=(gamma,beta_l,beta_r,alpha_l,alpha_r)：

\[
R_l=R_x(\gamma/2)R_y(\beta_l)R_z(\alpha_l),\qquad
R_r=R_x(-\gamma/2)R_y(\beta_r)R_z(\alpha_r).
\]

配合 H_l=K R_l K_l^{-1} 和 H_r=K R_r K_r^{-1}，匹配点残差为校正后的纵坐标差。内点集确定后，重拟合最小化加权残差平方和，使用阻尼正规方程。当前代码只实现给定内点和权重时的求解核；没有把普通最小二乘冒充完整 RANSAC 系统。

全图监督在规则锚点网格上比较预测 H 和参考 H 的映射结果。实现前必须约定坐标系：像素坐标的 H 不能直接乘归一化坐标的锚点；需要相应的相似变换。当前 API 要求调用者提供一致坐标。

虚拟相机共享焦距尺度 s=exp(eta) 和垂直主点平移 t；两幅图左乘同一个 G=K* K^{-1}。界限为 |eta|<=0.08、|t|<=16 像素。原图重采样和 Z=f*B/d 必须使用同一 K*。

## 我们独立推导的检查条件

令原校正相机主点为 (cx,cy)，共同变换满足：

\[
x^*=s(x-c_x)+c_x,\quad y^*=s(y-c_y)+c_y+t.
\]

因此对于同一对对应点：

\[
e_y^*=s e_y,\quad d^*=s d,\quad Z^*=\frac{sfB}{sd}=Z.
\]

三个可检验后果：

1. 理想对齐保持对齐，但非零像素残差会随缩放改变。仅报告纵向像素残差不足以区分更好的几何与简单缩小，需要同时检查姿态、覆盖和深度。
2. 垂直主点平移在左右纵向残差中抵消。它只能通过视野边界、重采样和下游匹配等影响结果，不能直接修正左右不一致的纵向误差。
3. 变换后误用旧焦距时，理想情况下 Z_wrong/Z=exp(-eta)。在论文允许范围内，带符号相对偏差约为 -7.69% 到 +8.33%。这只是几何一致性结论，不是论文真实图像 MAE 的预测。

还有一个训练实现问题需要补充材料解释：若 support 用离散布尔有效像素计数实现，它对相机参数几乎处处没有可用梯度。需要明确可微近似、解析面积计算或其他优化方式；当前不擅自选一个替代。

## 训练实现中仍缺失的定义

| 缺口 | 为什么不能静默猜测 |
|---|---|
| (mu,nu,alpha,beta,q) 到内点权重 w 的转换 | 预测头输出和截断范围不能唯一确定权重公式；q 的作用也未明示 |
| 19 维汇总特征和 9 维门控输入的逐维定义、归一化 | 输入维数相同不代表模型相同 |
| lambda_H、lambda_e、lambda_s、lambda_d、Huber delta、epsilon_s、distortion beta | 决定目标的相对尺度和优化行为 |
| 锚点网格密度与坐标归一化 | 影响监督强度和几何解释 |
| 两阶段 16,000 步如何分配、冻结哪些模块 | 不能把单阶段数复制给两阶段 |
| 求解器阻尼调度、退化样本处理、RANSAC 采样/评分细节、反传方式 | 决定稳定性及训练梯度 |
| “two matching layers”的确切配置 | 官方 Efficient LoFTR 默认四组 self/cross；本地探针用两组仅为显式假设 |
| depth reference 的精确生成与重投影、阈值、有效掩码和聚合方式 | 数值比较必须保持口径，不能把离线校正预测深度误称真实深度 |
| 五个种子、全部基线检查点和测试脚本 | 防止选择有利随机种子或不同版本 |

当前 `core.risk_weights()` 会明确报未实现，防止猜测的权重被误用于“正式”训练。

## 实验覆盖清单

| 原文位置 | 需要完成的范围 | 当前状态 |
|---|---|---|
| 表 1 | 两个数据集的 SIFT / SuperGlue / RAFT 校正指标，全部比较方法 | 未运行 |
| 表 2 | Carla，MonSter++ / DLNR / HITNet 深度与覆盖，单独测校正耗时 | 未运行 |
| 表 3 | Carla 与 Perturbed SceneFlow 的旋转及平移方向诊断 | 未运行 |
| 表 4 | Carla 训练、Semi-Truck 零样本迁移 | 未运行 |
| 表 5 | CARLA-Drift 全 155×1000 帧、TESO 比较 | 未运行 |
| 表 6 | 行约束、变换监督、风险校准消融 | 未运行 |
| 表 7 | pre-gauge / post-gauge 及旧 K / K* 消融 | 未运行 |

五种子、训练配置、所有失败样本和有效像素数都应留存。CPU/Mac 时间不会与 A40 的毫秒数直接视作复现一致。

## 一手来源

- https://arxiv.org/abs/2611.10518v1
- https://arxiv.org/html/2611.10518v1
- https://neurips.cc/virtual/2026/poster/151291
- https://openreview.net/forum?id=bWCyY4WYr9
- https://openaccess.thecvf.com/content/CVPR2025/papers/Gong_Rectification-specific_Supervision_and_Constrained_Estimator_for_Online_Stereo_Rectification_CVPR_2025_paper.pdf

下载件及哈希位于本地 paper/ 与 reports/provenance.json；原论文和第三方资源不随本项目公开快照分发。
