# VirtualRect 本地完整复现可行性

审阅日期：2026-11-17。结论：**可开始明确组件的独立实现；目前不能承诺在这台 Mac 上完成原设置、原数据、全部表格的数值复现。** 首要障碍是方法定义与评估资源缺口，其次是数据空间和完整训练成本。增加算力不能自动解决缺失定义。

## 本机与已运行检查

- Apple M4 Pro，12 核 CPU、16 核 GPU、48 GB 统一内存；检查时可用磁盘约 24 GiB，无已挂载外置盘。
- 独立 Python 3.12 环境；锁定依赖见 requirements-lock.txt。
- Apple MPS 在可访问设备的运行环境中确认为可用；受限进程会返回不可用，不据此判定硬件不支持。
- 几何检查：5 个种子，每种子 256 个无噪声合成对应点；5 次 LM 后最大行残差 RMSE 为 1.14e-13 像素。51 组共同虚拟相机变换通过深度尺度一致性检查。它们不验证抗外点、学习模块或真实图像表现。
- 随机权重匹配器组件探针：1024×512、一个双目对、两组 self/cross、FP32，CNN+coarse Transformer 的代理损失反向传播可运行；预热后两次耗时约 0.376 秒，末尾驱动分配内存约 3.16 GiB。**不包含粗匹配置信度矩阵、细匹配、求解器、优化器、正式损失和数据读取；不是完整训练吞吐，也不是峰值内存。**
- 初次导入失败来自 Kornia 新版本路径变化和缺少依赖；固定 kornia 0.7.3、loguru 0.7.3 并补齐依赖后运行通过，日志全部保留。

完整 batch=16 未测试。在 1024×512、1/8 特征图上有 8192 个位置，单个全对应 FP32 矩阵每样本约 256 MiB，batch=16 单个矩阵约 4 GiB；实际需要多份中间量、梯度、优化器和系统内存。48 GB 统一内存不能等同于 48 GB 独占显存。

## 数据实查

官方 FloSR README 的旧 Carla 桶已不存在，旧 Semi-Truck 前缀为空。但作者项目页指向的同一官方桶根目录有迁移后数据；本次已恢复链接并下载标定与划分文件，保存 SHA-256。

| 数据 | 核验结果 | 原始存储规模与问题 |
|---|---|---|
| Carla-Flowguided | 官方新目录存在；划分、配置、相机位姿下载成功 | 六个图像压缩包合计约 67.83 GiB；分卷是同一内容，不能重复计数 |
| Semi-Truck Highway | 官方新目录存在；标定与划分下载成功 | 图像压缩包约 1,019.96 GiB，尚未下载图像 |
| Perturbed SceneFlow | 原论文给出构造方式与规模；未找到作者处理后的版本或生成脚本 | 重渲染时的采样、种子、可见性和孔洞处理不唯一；自行生成只能标作重建版本 |
| CARLA-Drift | TESO 官方仓库及读取代码可用，作者链接声明八部分数据 | 数据主机 HTTPS 握手超时，本次不能确认下载可用或文件大小；不等于数据已撤回 |

新目录：

- https://torc-public-data-sharing.s3.amazonaws.com/index.html?prefix=carla-dataset/
- https://torc-public-data-sharing.s3.amazonaws.com/index.html?prefix=semi-truck-highway/
- https://cmp.felk.cvut.cz/teso/

划分检查：Carla 训练 6949 行，验证 774 行但 773 个唯一样本；第一行 `(0,1,True,True,cam_p_0/00006228.png,cam_p_1/00006228.png)` 重复两次。Semi-Truck 为 40007/10022 行。两个数据集的训练/验证完全相同 CSV 行交集均为空，这不证明场景隔离。正式基线应确认是否保留重复行，报告两种聚合的影响，不能静默去重。

可行的数据工程方案是从压缩流中解码并保存论文输入分辨率的无损缓存，同时保存原路径、原始字节哈希、插值方式与缩放后的 K。这样可减少落盘量，但下载带宽仍可能很大，且必须先用抽样验证预处理等价；当前尚未执行。不会在只有约 24 GiB 空间时自动下载整个图像集。

## 基线和评估器

| 组件 | 一手入口及本次状态 | 完整对齐仍需什么 |
|---|---|---|
| VirtualRect | 无相关 GitHub 搜索命中；arXiv 源包无代码；OpenReview 验证阻断 | 原作者补充定义、实现或完整配置 |
| RsCeR | CVF 正式论文可下载，页面无补充链接，未找到官方仓库 | 自实现关键基线、训练配方、检查点及 Perturbed SceneFlow |
| Efficient LoFTR | https://github.com/zju3dv/EfficientLoFTR 已克隆，训练/推理代码及权重入口存在 | 两层配置与预训练加载规则；本次未下载权重 |
| FloSR | https://github.com/anushl9o5/FloSR 已克隆；三组权重链接存在 | 移植 CUDA 设备假设、验证原始权重能下载并加载 |
| SIFT+MAGSAC | 本地 OpenCV 安装可提供对应算法 | 与论文相同阈值、内参/坐标约定和姿态消歧 |
| SP+SG / LoFTR | FloSR 含相应封装，FAR 作者链接 LoFTR 官方仓库 | 模型版本与评分参数；尚未实跑 |
| DirectionNet | 原始论文可读；未确认此次校正实验所用代码和权重 | 不能把别的姿态任务权重视作同一基线 |
| 8-point ViT / FAR | https://github.com/crockwell/rel_pose 与 https://github.com/crockwell/far | 原始方法代码存在不代表本任务的训练检查点可得 |
| TESO | https://github.com/moravecj/teso 已克隆，CPU Python 推理可读 | 数据与论文评估脚本闭环；尚未运行 |
| RAFT 评估器 | FloSR 源码使用 torchvision RAFT-Large，训练器选 C_T_SKHT_K_V1 | 默认类构造用 C_T_SKHT_V1，两者不可混用；还需确认缩放和掩码 |
| DLNR | https://github.com/David-Zhao-1997/High-frequency-Stereo-Matching-Network 代码和权重入口存在 | Middlebury 检查点、迭代数和 Apple GPU 路径未实测 |
| MonSter++ | https://github.com/Junda24/MonSter-plusplus 官方大模型与权重入口存在 | 不能用 RT 版本替代；README 有 CUDA/mmcv/PyTorch3D 依赖，实际推理必要部分须另核查 |
| HITNet | https://github.com/google-research/google-research/tree/master/hitnet 发布 TensorFlow 标准算子模型 | 有多个视差范围/数据集模型，原文确切版本待定；CPU 可移植性仍需实跑 |

“存在入口”“已下载”“已加载”“已跑正式评估”是不同状态。本次只对明确注明的代码、元数据和组件做了实际检查。

## 推进顺序与停止条件

1. 当前已完成：原文/源码阅读、已知公式实现、合成几何验证、官方资源审计、MPS 组件检查。
2. 下一阶段：取得补充材料或形成逐条可审阅的实现假设；尤其先解决权重映射、summary features、support 梯度和阶段配置。保留不能唯一复原的部分，不能称精确复现。
3. 对少量正式 Carla 样本验证图像尺寸、K 缩放、左右约定、SIFT+MAGSAC、匹配器和评估器。这个阶段是集成核验，不用趋势替代原表格。
4. 完成完整单步训练内存/时间实测后，再估算 16,000 步×多数据集×五种子×消融。若用梯度累积或冻结主干，必须记录训练定义变化；BatchNorm 和跨样本操作使累积不自动等价于 batch=16。
5. 全量训练需有足够存储/缓存空间、全数据和关键配置。最终依照 method.md 的七表清单对照，不把实验数达到预期写成数值匹配。

**当前没有运行任何正式训练或表格实验；没有发布新的单篇 GitHub 仓库。** 总览公开快照仅呈现这一可行性阶段及明确局限，不包含原始数据、论文文件或第三方权重。
