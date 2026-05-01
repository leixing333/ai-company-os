# OPC 可视化管理工作台 PRD v3

## 1. 产品概述

### 1.1 产品定位
OPC (One Person Company) 可视化管理工作台是专为“一人公司”CEO 打造的**超级指挥中心 (Command Center)**。它不是一个传统的 CRUD 管理后台，也不是一个简单的聊天机器人集合，而是一个**上下文管理器**和**宏观调度台**。

### 1.2 核心原则
工作台的设计与开发必须严格遵循以下核心原则：
首先，**原样可视化**是基础。绝不引入新的数据库或第三方复杂工具（如 Dify、Flowise）。所有数据必须直接读取现有的文件系统，包括 `status.json`、`SOUL.md`、`kairos_logs` 和 `config.json`。
其次，**自主开发**是保障。采用 Next.js 配合 Tailwind CSS 和 FastAPI 架构，完全自主掌控代码，确保系统的轻量与高效。
再次，**宏观委托与微观引导**是交互范式。CEO 通过工作台进行宏观的任务分发和异常干预，而 Agent 在底层自主运行，实现人机协作的最佳平衡。
最后，**极速响应**是体验追求。采用 ⌘K 全局命令面板和键盘优先的设计，确保 CEO 能以最快速度获取信息和下达指令。

## 2. 需求架构与页面规划

工作台采用“深空黑 (Deep Space Black)”主题，极简设计，高信息密度。整体架构分为四大核心模块。

### 2.1 首页：全局指挥大盘 (Mission Control Center)
这是 CEO 登录后的默认视图，提供系统运行的全局脉搏。

| 模块名称 | 创新展示方式 | 数据来源与逻辑 |
|---|---|---|
| **系统脉搏 (System Pulse)** | 顶部横向展示，以心电图波形实时反映 20 个 Agent 的活跃度（如 Token 消耗、API 调用频率）。 | 实时解析 `kairos_logs` |
| **活跃空间 (Active Spaces)** | 采用网格布局展示当前所有活跃项目。每个卡片显示项目 ID、客户名称、当前所处状态机节点、负责 Agent 头像及进度条。 | 读取 `active_projects/*/status.json` |
| **硬停警报 (Aegis Gates)** | 右侧悬浮抽屉，实时拦截并高亮显示触发了硬停条件（如报价超额、生产超时）的事件，提供一键“Approve”或“Reject”操作。 | 匹配 `STATUS_MACHINE.json` 规则 |

### 2.2 组织架构：活体图谱 (Living Org Chart)
摒弃静态树状图，采用动态星系视图展示公司组织架构。

| 模块名称 | 创新展示方式 | 数据来源与逻辑 |
|---|---|---|
| **星系视图 (Galaxy View)** | 以 CoS（幕僚长）为中心恒星，四大团队（营销、策略、生产、运营）为行星轨道，20 个 Agent 为卫星。Agent 的发光强度实时反映其工作负载。 | 读取 `SOUL.md` 目录结构与日志 |
| **角色透视镜 (Role X-Ray)** | 点击任意 Agent，右侧滑出半透明面板，展示其核心定义（角色、目标、职责）。面板内嵌微型终端，实时滚动该 Agent 的最新 KAIROS 日志。 | 结合 `SOUL.md` 与 `kairos_logs` |

### 2.3 业务过程：时空追溯 (Time-Space Trace)
将底层的追加式日志转化为直观的业务时间线。

| 模块名称 | 创新展示方式 | 数据来源与逻辑 |
|---|---|---|
| **决策时间线 (Decision Timeline)** | 生成类似 Git 提交历史的垂直时间线。`DECISION` 节点以大圆点显示，`STATUS` 变更以小圆点显示。 | 读取 `memory/kairos_logs/` |
| **正反合透镜 (Dialectic Lens)** | 悬停在 `DECISION` 节点上，弹出对比视图，左侧显示“反（Alternatives）”，右侧显示“正（Reason）”，底部显示“合（Final Choice）”，完美还原 CoS 的决策过程。 | 解析 KAIROS 日志详情 |

### 2.4 知识资产：数字军械库 (Digital Armory)
集中管理公司的数字资产和配置。

| 模块名称 | 创新展示方式 | 数据来源与逻辑 |
|---|---|---|
| **技能矩阵 (Skill Matrix)** | 采用分栏视图展示所有技能文档，并根据调用次数展示熟练度徽章。 | 读取 `skills/` 目录下的 `SKILL.md` |
| **交付物橱窗 (Deliverables Showcase)** | 采用瀑布流布局展示已完成项目成果，支持一键打包下载。 | 读取 `4_operations/deliverables/` |
| **配置中心** | 提供可视化界面编辑全局配置，管理 API Key 和系统参数。 | 读写 `.opc/config.json` |

## 3. 创新交互设计

### 3.1 ⌘K 全局命令面板 (Omni-Command Palette)
这是工作台的灵魂交互。按下 `⌘K` 即可唤出，支持多种极速操作。
CEO 可以通过输入 `go to scout` 实现**快速跳转**，直接打开小探详情页。
在遇到紧急情况时，输入 `approve P-001` 即可实现**极速干预**，直接通过项目 P-001 的硬停审批。
此外，面板还支持**自然语言调度**，例如输入 `tell closer to pause emails`，系统会自动解析意图并向小销下达指令。

### 3.2 空间隔离与上下文挂载 (Isolated Spaces & Context Mounting)
当 CEO 需要与 Agent 深入交互时，系统会创建一个临时的“Space”。
通过**上下文拖拽**功能，CEO 可将左侧边栏的 `brief.md` 或 `status.json` 拖拽到对话窗口，系统自动将其作为上下文挂载。
系统支持**并行工作区**，允许打开多个标签页，CEO 可同时指导设计团队（Space A）和监控营销团队（Space B）。

### 3.3 终端融合 (Terminal Fusion)
工作台底部保留了一个可随时唤出的终端抽屉（基于 xterm.js）。图形界面的操作会在终端中回显底层命令，实现 GUI 与 CLI 的无缝切换，满足高级操作需求。

## 4. 系统文件前置更新清单

为了支持上述可视化需求，现有的底层文件系统需要进行以下前置更新和规范化：

| 涉及文件/目录 | 当前状态 | 需要进行的更新/规范化 |
|---|---|---|
| `1_company/agents/` | 目录缺失 | 需要创建该目录，并将 CoS、CTO 等核心管理层 Agent 的 `SOUL.md` 移入或链接至此，以符合四大团队架构。 |
| `2_strategy/agents/` | 目录缺失 | 需要创建该目录，并补充策略层 Agent 的 `SOUL.md`。 |
| `SOUL.md` (所有 Agent) | 格式不统一 | 必须统一包含 YAML Frontmatter（如 `role`, `team`, `model`），以便前端解析和展示。 |
| `kairos_logs/` | 分散在不同目录 | 需要统一日志格式（JSON Lines），确保包含 `timestamp`, `agent`, `action_type` (DECISION/STATUS/ESCALATION), `details` 字段。 |
| `status.json` | 存在模板 | 确保所有活跃项目严格遵循 `STATUS_MACHINE.json` 中定义的状态码，禁止使用未定义状态。 |
| `.opc/config.json` | 已存在 | 补充前端 UI 所需的配置项（如主题色偏好、刷新频率）。 |

## 5. 分层级开发计划

开发工作将分为四个阶段（Phases），逐步实现从只读展示到深度交互的完整闭环。

### Phase 1: 基础设施与只读大盘 (Week 1)
本阶段的目标是搭建前后端框架，实现核心数据的只读可视化。
在后端（FastAPI）方面，需要实现文件系统读取 API，用于读取 `config.json`、`status.json` 和 `SOUL.md`。同时，实现目录监听（Watchdog），当文件变更时通过 WebSocket 推送更新。
在前端（Next.js）方面，搭建基于 Tailwind CSS 的深色主题 UI 框架。实现“活跃空间”网格视图以读取项目状态，并构建“星系视图”雏形以静态读取 Agent 列表。

### Phase 2: 动态图谱与时空追溯 (Week 2)
本阶段的目标是实现 KAIROS 日志的解析与可视化，完善组织架构图谱。
后端需要实现 `kairos_logs` 解析 API，提取决策和状态变更事件。
前端则需完善“星系视图”，根据日志数据动态调整 Agent 发光强度。同时，实现“角色透视镜”侧边栏，并开发“决策时间线”和“正反合透镜”组件。

### Phase 3: 交互干预与命令面板 (Week 3)
本阶段的目标是引入 ⌘K 命令面板，实现 CEO 对系统的极速干预。
后端需要实现状态修改 API，例如审批 Escalation 和更新 `status.json`。此外，集成 LLM API，用于解析自然语言命令。
前端将开发 ⌘K 全局命令面板组件，实现硬停警报（Aegis Gates）抽屉及一键审批功能，并集成底部终端抽屉（xterm.js）。

### Phase 4: 空间隔离与资产管理 (Week 4)
本阶段的目标是实现高级的上下文管理和数字资产展示，完成系统闭环。
后端需要实现文件打包下载 API，并完善配置文件读写 API。
前端将开发“空间 (Space)”多标签页系统，实现拖拽式上下文挂载功能。同时，开发“技能矩阵”和“交付物橱窗”视图，并进行全链路 UI/UX 一致性打磨和性能优化。
