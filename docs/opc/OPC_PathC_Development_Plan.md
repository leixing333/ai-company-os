# OPC 工作台 路径C 完整功能开发计划

**版本：** v1.0  
**日期：** 2026-05-05  
**策略：** 完全自主开发 + 参考 MateClaw 设计蓝图  
**技术栈：** React 19 + TypeScript + FastAPI（Python）+ SQLite/PostgreSQL

---

## 一、MateClaw 功能全景分析

通过对 MateClaw 15 个核心页面源码的完整分析，其功能体系可归纳为以下六大模块：

| 模块 | MateClaw 页面 | 核心价值 |
|---|---|---|
| **运行监控** | Dashboard、Backstage | 实时数据概览、Agent 任务运行状态 |
| **Agent 管理** | Agents、AgentContext | 创建/编辑 Agent、上下文文件管理 |
| **对话系统** | ChatConsole、Sessions、Channels | 多 Agent 对话、会话管理、渠道接入 |
| **任务调度** | CronJobs | 定时任务创建、启停、立即执行 |
| **安全审批** | Security（ToolGuard、FileGuard、AuditLogs、Members、Workspaces） | 工具防护、文件防护、审计日志、成员权限 |
| **能力扩展** | SkillMarket、Plugins、McpServers、Datasources | 技能库、插件、MCP 服务器、数据源 |

MateClaw 的设计哲学是**"Agentic, but not autonomous"**——Agent 有能力，但关键决策必须经人审批。这与 OPC 的"执行前需 CEO 确认"完全一致。

---

## 二、OPC 工作台功能完整规划

在 MateClaw 功能蓝图的基础上，结合 OPC 系统的独特特性（SOUL.md 体系、KAIROS 日志、四大团队架构、CEO 审批机制），规划以下 **10 大功能模块**：

### 模块 1：身份认证与工作区

**对应 MateClaw：** Login.vue + Security/Workspaces + Security/Members

OPC 工作台采用 JWT 认证，CEO 为唯一管理员账号。工作区对应 OPC 四大团队（生产研发、市场营销、设计团队、客户运营），每个工作区有独立的 Agent 集合和权限边界。

| 功能点 | 描述 |
|---|---|
| CEO 登录 | 用户名+密码，JWT Token，滑动续签 |
| 工作区切换 | 顶部导航切换四大团队视图 |
| 成员管理 | 未来扩展：邀请协作者，设置只读/编辑权限 |

### 模块 2：指挥大盘（Dashboard）

**对应 MateClaw：** Dashboard.vue

OPC 指挥大盘在 MateClaw 数据概览的基础上，增加 OPC 特有的业务指标：

| 区块 | 数据来源 | 内容 |
|---|---|---|
| 系统脉搏 | 实时 API | 今日对话数、任务数、Token 消耗、API 费用 |
| 活跃项目网格 | `status.json` | 所有项目的 12 状态看板，支持快速跳转 |
| 硬停警报 | Escalation 队列 | 待 CEO 审批的请求，红色醒目展示 |
| 7 天趋势图 | 历史记录 | 消息量、Token 消耗、任务完成率趋势 |
| 最近活动流 | KAIROS 日志 | 最近 20 条 Agent 活动记录 |
| 财务快照 | `finance_tracker.csv` | 本月 MRR、成本、利润率 |

### 模块 3：活体图谱（Agent 星系视图）

**对应 MateClaw：** Agents.vue（增强版）

MateClaw 的 Agent 列表是表格+卡片形式，OPC 将其升级为**星系视图**——以 CoS 为中心，四大团队为轨道，Agent 的发光强度实时反映工作负载。

| 功能点 | 描述 |
|---|---|
| 星系视图 | Canvas/SVG 动态渲染，Agent 节点按团队分轨道 |
| 实时状态 | idle（暗）/ running（亮）/ waiting_approval（橙色脉冲）/ error（红色） |
| 角色透视镜 | 点击 Agent 节点，右侧展开 SOUL.md 详情侧边栏 |
| Agent 管理 | 创建、编辑、删除、启用/禁用 Agent |
| 上下文文件 | 对应 AgentContext.vue，管理 Agent 关联的 Markdown 文件 |

### 模块 4：任务管理中心

**对应 MateClaw：** Backstage.vue（核心功能，OPC 最重要的补充）

这是 OPC Phase 1 最缺失的模块。参考 MateClaw Backstage 的设计：

| 功能点 | 描述 |
|---|---|
| 任务发布 | CEO 向 CoS 发布任务，支持优先级、截止日期、上下文附件 |
| 任务看板 | 按状态分列：待处理 / 进行中 / 待审批 / 已完成 / 失败 |
| 任务详情 | 展开查看 Agent 的思考链（Thought）、工具调用（Action）、结果（Result） |
| 子任务树 | CoS 委派给其他 Agent 的子任务，树状展示 |
| 任务干预 | CEO 可暂停、取消、重启任务 |
| 实时刷新 | WebSocket 推送，任务状态变化实时更新 |

### 模块 5：CEO 对话与干预中心

**对应 MateClaw：** ChatConsole.vue（深度定制版）

MateClaw 的 ChatConsole 是通用对话界面，OPC 将其改造为 CEO 专属的**上下文感知对话**：

| 功能点 | 描述 |
|---|---|
| @Agent 选择 | 输入 `@CoS`、`@Scout` 等，自动注入对应 SOUL.md 作为 System Prompt |
| 上下文挂载 | 拖拽 `brief.md`、`status.json` 到对话框，作为附加上下文 |
| 多会话管理 | 左侧会话列表，支持命名、归档、删除 |
| 流式输出 | SSE 流式渲染 Agent 回复，支持 Markdown 格式 |
| 审批内嵌 | 对话中出现审批请求时，直接在消息气泡中显示 Approve/Reject 按钮 |
| 渠道接入 | 对应 Channels.vue，支持 Slack/飞书/企业微信消息推送 |

### 模块 6：时空追溯（KAIROS 日志）

**对应 MateClaw：** 无直接对应（OPC 独有）

将 KAIROS 追加式日志转化为可视化的决策时间线：

| 功能点 | 描述 |
|---|---|
| 垂直时间线 | 按日期分组，每条记录显示 Agent、操作类型、摘要 |
| 正反合透镜 | 悬停展开：显示 CoS 的备选方案（正）、风险评估（反）、最终决策（合） |
| 类型过滤 | 按 Agent、操作类型、项目、日期范围过滤 |
| 全文搜索 | 搜索日志内容 |
| 导出 | 导出为 Markdown 或 CSV |

### 模块 7：安全审批中心

**对应 MateClaw：** Security.vue（ToolGuard + AuditLogs + Members）

| 功能点 | 描述 |
|---|---|
| 审批队列 | 所有待 CEO 审批的请求，支持批量处理 |
| 审批详情 | 展示 Agent 的请求原因、执行计划、风险评估 |
| 工具防护 | 配置哪些工具需要审批（如：发送邮件、写入文件、调用外部 API） |
| 审计日志 | 所有操作的完整记录，不可删除 |
| 成员权限 | 未来扩展：邀请协作者，设置操作权限 |

### 模块 8：定时任务管理

**对应 MateClaw：** CronJobs.vue（完整复刻）

| 功能点 | 描述 |
|---|---|
| 任务列表 | 显示所有定时任务，状态、下次执行时间 |
| 创建任务 | Cron 表达式 + 目标 Agent + 任务内容 |
| 立即执行 | 手动触发一次性执行 |
| 执行历史 | 查看每次执行的结果和日志 |
| 启用/禁用 | 开关控制任务激活状态 |

**OPC 预置定时任务：**

| 任务名称 | Agent | Cron | 内容 |
|---|---|---|---|
| Scout 每日线索挖掘 | Scout | 0 9 * * 1-5 | 从 PH/LinkedIn/HN 抓取今日高质量线索 |
| CoS 每日晨报 | CoS | 0 8 * * 1-5 | 汇总昨日进展，生成今日工作建议 |
| 财务周报 | CoS | 0 9 * * 1 | 生成上周财务数据摘要 |
| KO 知识沉淀 | KO | 0 18 * * 5 | 整理本周知识资产，更新技能库 |

### 模块 9：知识与能力管理

**对应 MateClaw：** SkillMarket.vue + Plugins.vue + McpServers.vue + Datasources.vue

| 功能点 | 描述 |
|---|---|
| 技能矩阵 | 展示所有 Agent 的技能（SKILL.md），支持搜索、分类、启用/禁用 |
| 交付物橱窗 | 浏览 `deliverables/` 目录，预览 Markdown/PDF 文件 |
| MCP 服务器 | 管理 MCP 工具服务器，测试连接，查看可用工具列表 |
| 数据源管理 | 配置外部数据库、API 数据源 |
| 插件管理 | 管理已安装的 Agent 插件，启用/禁用 |

### 模块 10：财务与运营大盘

**对应 MateClaw：** 无直接对应（OPC 独有）

| 功能点 | 描述 |
|---|---|
| 营收看板 | MRR/ARR 趋势图，读取 `finance_tracker.csv` |
| 成本分析 | API 费用、工具费用、运营成本分解 |
| 转化漏斗 | 线索 → 跟进 → 提案 → 成交 |
| 交付记录 | 已完成项目列表，含金额、时间、客户 |
| ⌘K 命令面板 | 全局快捷命令，支持导航、发布任务、搜索 Agent |

---

## 三、技术架构

### 前端（React 19 + TypeScript）

```
client/src/
├── pages/
│   ├── Login.tsx              # 登录页
│   ├── Dashboard.tsx          # 指挥大盘
│   ├── GalaxyView.tsx         # 活体图谱
│   ├── TaskCenter.tsx         # 任务管理中心
│   ├── ChatConsole.tsx        # 对话干预中心
│   ├── TimelineView.tsx       # 时空追溯
│   ├── SecurityCenter.tsx     # 安全审批中心
│   ├── CronJobs.tsx           # 定时任务
│   ├── KnowledgeBase.tsx      # 知识能力管理
│   └── FinanceDashboard.tsx   # 财务大盘
├── components/
│   ├── CommandPalette.tsx     # ⌘K 命令面板
│   ├── NavSidebar.tsx         # 左侧导航栏
│   ├── AgentCard.tsx          # Agent 卡片
│   ├── TaskCard.tsx           # 任务卡片
│   ├── ApprovalDrawer.tsx     # 审批抽屉
│   └── ChatMessage.tsx        # 消息气泡
├── lib/
│   ├── api.ts                 # API 客户端（封装 fetch）
│   ├── websocket.ts           # WebSocket 实时推送
│   └── types.ts               # 全局类型定义
└── contexts/
    ├── AuthContext.tsx         # 认证状态
    └── WorkspaceContext.tsx    # 工作区状态
```

### 后端（FastAPI + Python）

```
server/
├── main.py                    # FastAPI 入口
├── routers/
│   ├── auth.py                # JWT 认证
│   ├── agents.py              # Agent CRUD + 状态
│   ├── tasks.py               # 任务管理
│   ├── approvals.py           # 审批流
│   ├── chat.py                # 对话（SSE 流式）
│   ├── kairos.py              # KAIROS 日志读取
│   ├── cron.py                # 定时任务
│   ├── finance.py             # 财务数据
│   ├── skills.py              # 技能库
│   └── config.py              # 配置中心
├── core/
│   ├── soul_parser.py         # 解析 SOUL.md YAML Frontmatter
│   ├── kairos_parser.py       # 解析 JSONL 日志
│   ├── file_watcher.py        # 文件系统监听（inotify）
│   └── llm_client.py          # LLM API 调用（Anthropic/OpenAI）
├── models/
│   ├── agent.py               # Agent 数据模型
│   ├── task.py                # 任务数据模型
│   └── approval.py            # 审批数据模型
└── db/
    └── database.py            # SQLite 数据库连接
```

### 数据流设计

```
ai-company-os/ (文件系统)
    ↕ 实时读写（soul_parser, kairos_parser, file_watcher）
FastAPI 后端
    ↕ REST API + WebSocket
React 前端
    ↕ 用户操作
CEO（你）
```

---

## 四、分阶段开发计划

### Phase 1（已完成）：基础框架 + 静态可视化

**状态：✅ 已完成（checkpoint: 92c014e3）**

已实现：指挥大盘、活体图谱、时空追溯、财务大盘、终端、配置中心、⌘K 命令面板（均为 mock 数据）。

---

### Phase 2（Week 1-2）：后端接入 + 真实数据

**目标：** 升级为全栈项目，FastAPI 后端读取真实文件系统数据，替换所有 mock 数据。

| 任务 | 优先级 | 工作量 |
|---|---|---|
| 升级为 web-db-user 全栈项目 | P0 | 0.5天 |
| FastAPI 后端：SOUL.md 解析 API | P0 | 1天 |
| FastAPI 后端：status.json 读取 API | P0 | 0.5天 |
| FastAPI 后端：KAIROS 日志解析 API | P0 | 1天 |
| FastAPI 后端：finance_tracker.csv API | P1 | 0.5天 |
| 前端：替换 mock 数据为真实 API 调用 | P0 | 1天 |
| JWT 认证：CEO 登录页 + Token 管理 | P0 | 1天 |
| WebSocket：实时状态推送 | P1 | 1天 |

**交付物：** 登录后可看到真实的 Agent 状态、真实的项目进度、真实的 KAIROS 日志。

---

### Phase 3（Week 3）：任务管理中心

**目标：** 实现完整的任务发布、追踪、干预闭环。

| 任务 | 优先级 | 工作量 |
|---|---|---|
| 任务数据模型设计（SQLite） | P0 | 0.5天 |
| 任务发布 API（POST /tasks） | P0 | 1天 |
| 任务看板 UI（Kanban 视图） | P0 | 1.5天 |
| 任务详情侧边栏（思考链展示） | P1 | 1天 |
| 子任务树视图 | P1 | 1天 |
| 任务干预（暂停/取消/重启） | P0 | 0.5天 |
| ⌘K 命令面板：发布任务命令 | P1 | 0.5天 |

**交付物：** CEO 可以通过 Dashboard 或 ⌘K 向 CoS 发布任务，实时看到任务执行进度。

---

### Phase 4（Week 4）：CEO 对话干预 + 审批流

**目标：** 实现 @Agent 对话、上下文挂载、审批弹窗。

| 任务 | 优先级 | 工作量 |
|---|---|---|
| LLM API 接入（Anthropic/OpenAI） | P0 | 1天 |
| @Agent 注入 SOUL.md System Prompt | P0 | 1天 |
| SSE 流式输出 | P0 | 1天 |
| 上下文文件拖拽挂载 | P1 | 1天 |
| 审批队列 UI + 审批弹窗 | P0 | 1天 |
| 工具防护配置（ToolGuard） | P1 | 0.5天 |
| 审计日志页面 | P1 | 0.5天 |

**交付物：** CEO 可以直接与任意 Agent 对话，审批请求出现时可在界面上一键 Approve/Reject。

---

### Phase 5（Week 5）：定时任务 + 能力管理

**目标：** 实现 Cron 调度、技能库、MCP 服务器管理。

| 任务 | 优先级 | 工作量 |
|---|---|---|
| Cron 任务管理 UI + API | P0 | 1.5天 |
| 预置 4 个 OPC 定时任务 | P0 | 0.5天 |
| 技能矩阵 UI（读取 SKILL.md） | P1 | 1天 |
| 交付物橱窗（浏览 deliverables/） | P1 | 1天 |
| MCP 服务器管理 | P2 | 1天 |
| 数据源管理 | P2 | 1天 |

**交付物：** Scout 每日线索挖掘、CoS 每日晨报等定时任务自动运行，CEO 可在界面查看执行结果。

---

### Phase 6（Week 6）：财务大盘 + 运营闭环

**目标：** 实现真实财务数据可视化，完成完整的业务闭环。

| 任务 | 优先级 | 工作量 |
|---|---|---|
| 财务数据 API（读取 finance_tracker.csv） | P0 | 0.5天 |
| 营收/成本趋势图（Recharts） | P0 | 1天 |
| 转化漏斗可视化 | P1 | 1天 |
| 交付记录表 | P1 | 0.5天 |
| 系统健康检查（Doctor 页面） | P2 | 1天 |
| 移动端响应式适配 | P2 | 1天 |
| 性能优化 + 错误边界 | P1 | 1天 |

**交付物：** 完整可用的 OPC 工作台，所有功能模块上线，真实数据驱动。

---

## 五、与 MateClaw 的关键差异

| 维度 | MateClaw | OPC 工作台 |
|---|---|---|
| 定位 | 通用多智能体平台 | CEO 专属指挥中心 |
| 用户 | 多用户、多工作区 | 单 CEO + 22 个 Agent |
| Agent 定义 | 界面配置 | 读取 SOUL.md 文件 |
| 日志系统 | 通用运行日志 | KAIROS 正反合决策日志 |
| 对话模式 | 通用聊天 | @Agent 上下文注入 |
| 财务模块 | 无 | 完整财务大盘 |
| 视觉风格 | 通用 SaaS | 深空操控台（CEO 专属） |
| 技术栈 | Java + Vue 3 | Python + React 19 |

---

## 六、等待补充的设计资料

在正式启动 Phase 2 开发前，以下内容需要你补充：

1. **界面偏好**：是否有参考的 UI 风格（如 Linear、Vercel、Raycast 等）？
2. **功能优先级调整**：以上 10 个模块中，哪些是 Phase 2 必须有的？
3. **LLM 配置**：使用 Anthropic Claude 还是 OpenAI？API Key 如何管理？
4. **部署方式**：本地运行还是需要公网访问（影响 WebSocket 和 SSE 的配置）？
5. **移动端需求**：是否需要手机端访问？

---

*文档生成时间：2026-05-05 | 基于 MateClaw 15 个页面源码分析 + OPC 系统现有成果*
