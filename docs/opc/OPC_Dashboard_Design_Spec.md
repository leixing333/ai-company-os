# OPC 可视化管理工作台：页面规划与创新交互设计方案

## 1. 设计理念与范式转变

在评估了开源社区中如 Mission Control、AgentRails 等项目，并结合了业界关于 Agent 编排 UI 的最新探讨（如 LukeW 的 Intent 概念）后，我们为 OPC 可视化管理工作台确立了全新的设计理念。

传统的 AI 管理后台往往陷入“更花哨的聊天界面”或“过度复杂的拖拽式节点图”的误区。OPC 工作台将摒弃这些老套的展示方式，转而采用**“宏观委托与微观引导”（Macro Delegation & Micro Steering）**的交互范式。

工作台的核心不再是简单的 CRUD（增删改查）或静态的 Kanban 看板，而是**上下文管理（Context Management）**与**统一工作流（Unified Workflow）**。我们将采用类似 Linear 的极简深色主题（Dark Mode Minimal），结合 Raycast 的命令面板（Command Palette）模式，打造一个高信息密度、键盘优先、极速响应的“指挥中心”（Command Center）。

## 2. 核心页面规划

### 2.1 首页：全局指挥大盘 (Mission Control Center)

首页是 CEO 的上帝视角，摒弃传统的仪表盘堆砌，采用“太空任务控制中心”的视觉隐喻，聚焦于系统的实时脉搏。

| 模块 | 创新展示方式 | 数据来源 |
|---|---|---|
| **系统脉搏 (System Pulse)** | 顶部横向的实时心电图式波形，展示 20 个 Agent 的活跃度（Token 消耗速率、API 调用频率）。 | `kairos_logs` 实时解析 |
| **活跃空间 (Active Spaces)** | 摒弃传统列表，采用类似 Vercel 部署卡片的网格布局。每个卡片代表一个活跃项目，显示当前所处状态机节点、负责 Agent 头像及进度条。 | `active_projects/*/status.json` |
| **硬停警报 (Aegis Gates)** | 屏幕右侧的悬浮抽屉，高亮显示触发了硬停条件（如报价超额、生产超时）的事件，提供一键“Approve”或“Reject”的快速操作。 | `STATUS_MACHINE.json` 规则匹配 |

### 2.2 组织架构与角色：活体图谱 (Living Org Chart)

不再使用静态的树状图，而是构建一个动态的“活体图谱”。

| 模块 | 创新展示方式 | 数据来源 |
|---|---|---|
| **星系视图 (Galaxy View)** | 以 CoS（幕僚长）为中心恒星，四大团队（营销、策略、生产、运营）为行星轨道，20 个 Agent 为卫星。Agent 的发光强度代表其当前的工作负载。 | `SOUL.md` 目录结构 |
| **角色透视镜 (Role X-Ray)** | 点击任意 Agent 星球，右侧滑出半透明面板，展示其 `SOUL.md` 的核心定义。面板内嵌一个微型终端，实时滚动该 Agent 的最新 KAIROS 日志。 | `SOUL.md` & `kairos_logs` |

### 2.3 业务过程记录：时空追溯 (Time-Space Trace)

将 KAIROS 追加式日志转化为可交互的时间线。

| 模块 | 创新展示方式 | 数据来源 |
|---|---|---|
| **决策时间线 (Decision Timeline)** | 类似 Git 提交历史的垂直时间线。`DECISION` 节点显示为大圆点，`STATUS` 变更显示为小圆点。支持通过鼠标滚轮快速穿梭时间。 | `memory/kairos_logs/` |
| **正反合透镜 (Dialectic Lens)** | 当悬停在 `DECISION` 节点上时，弹出类似代码 Diff 的对比视图，左侧显示“反（Alternatives）”，右侧显示“正（Reason）”，底部显示“合（Final Choice）”。 | KAIROS 日志详情 |

### 2.4 知识资产：数字军械库 (Digital Armory)

集中展示公司的数字资产，采用类似 macOS Finder 的分栏视图（Column View）。

| 模块 | 创新展示方式 | 数据来源 |
|---|---|---|
| **技能矩阵 (Skill Matrix)** | 左侧栏列出所有 `SKILL.md`，右侧栏展示技能详情。引入“熟练度”概念，根据该技能被调用的次数展示不同的徽章。 | `skills/` 目录 |
| **交付物橱窗 (Deliverables Showcase)** | 采用类似 Dribbble 的瀑布流布局，展示已完成项目的设计图、代码包预览。支持一键打包下载。 | `4_operations/deliverables/` |

## 3. 创新交互逻辑

### 3.1 ⌘K 全局命令面板 (Omni-Command Palette)

这是 OPC 工作台的灵魂交互。CEO 无需在复杂的菜单中寻找功能，只需按下 `⌘K`（或 `Ctrl+K`），即可唤出全局命令面板。

- **快速跳转**：输入 `go to scout` 直接打开小探的详情页。
- **极速干预**：输入 `approve P-001` 直接通过项目 P-001 的硬停审批。
- **自然语言调度**：输入 `tell closer to pause emails`，系统自动解析意图并向小销下达指令。

### 3.2 空间隔离与上下文挂载 (Isolated Spaces & Context Mounting)

借鉴 Intent by Augment 的理念，当 CEO 需要与 Agent 深入交互时，系统会创建一个临时的“空间（Space）”。

- **上下文拖拽**：CEO 可以从左侧边栏将某个 `brief.md` 或 `status.json` 拖拽到对话窗口中，系统会自动将其作为上下文挂载（Context Mounting）。
- **并行工作区**：支持同时打开多个 Space 标签页，CEO 可以在指导设计团队（Space A）的同时，监控营销团队的线索抓取（Space B）。

### 3.3 终端融合 (Terminal Fusion)

为了满足高级操作需求，工作台在底部保留了一个可随时唤出的终端抽屉（类似 VS Code 的终端）。

- **无缝切换**：CEO 可以在图形界面操作和命令行输入之间无缝切换。图形界面的某些操作（如修改配置）会在终端中回显对应的底层命令，帮助 CEO 了解系统运作原理。

## 4. 视觉风格定义

- **主题基调**：深空黑（Deep Space Black）背景，配合高对比度的霓虹强调色（如赛博朋克蓝、荧光绿），营造未来科技感。
- **排版排布**：采用 Inter 或 Roboto 等无衬线字体，追求极致的清晰度和可读性。大量使用留白（Negative Space）来区分信息层级，避免视觉拥挤。
- **动效设计**：引入微动效（Micro-interactions），如按钮悬停时的微妙发光、状态切换时的平滑过渡，增强操作的反馈感和沉浸感。

## 5. 参考文献

[1] builderz-labs. Mission Control: Self-hosted AI agent orchestration platform. GitHub. https://github.com/builderz-labs/mission-control
[2] rforgeon. AgentRails: A modern dashboard for managing and monitoring your AI agents. GitHub. https://github.com/rforgeon/AgentRails
[3] Luke Wroblewski. Agent Orchestration UI. https://www.lukew.com/ff/entry.asp?2141
