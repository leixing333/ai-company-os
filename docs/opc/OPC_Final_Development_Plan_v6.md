# OPC 智能体操作平台 — 完整开发规划 v6（最终版）

> **文档性质**：本文档为路径C（完全自主开发）的最终执行蓝图，整合了 v4（完整技术选型、功能模块、API 端点）与 v5（完整导航体系、设置模块、多模态配置），新增智能体编排独立板块，以"项目"为核心串联全生命周期工作流。确认后可直接指导开发。
>
> **版本历史**：v1（初稿）→ v2（功能完整性）→ v3（前置更新）→ v4（技术选型+功能细节）→ v5（导航体系+设置模块）→ **v6（最终整合版）**

---

## 一、战略定位与核心原则

OPC 智能体操作平台（以下简称"OPC 工作台"）是一人公司的数字神经中枢，其核心定位是 **CEO 专属指挥舱**，而非通用 AI 助手。与 MateClaw 的最大差异在于：OPC 工作台深度融合了 SOUL.md 人格体系、KAIROS 决策日志、四大团队组织架构和 Escalation 审批机制，同时以"项目"为核心串联从前期商务到交付运营的完整业务闭环。

**六项核心设计原则**如下：

| 原则 | 说明 |
|---|---|
| 以项目为核心 | 所有工作（任务、对话、财务、日志）均可关联到具体项目，形成完整业务闭环 |
| 原样可视化 | 读取已有文件系统（SOUL.md、status.json、kairos_logs），不重建数据 |
| 深空主题延续 | 沿用 Phase 1 的深空操控台风格，支持暗色/亮色双模式切换 |
| 移动端优先响应式 | 所有页面在手机端可用，关键操作（审批、查看）在移动端完整支持 |
| LLM 多提供商容错 | 支持多个 LLM 提供商配置，按优先级排序，失败自动切换并保持上下文 |
| 公网部署就绪 | WebSocket/SSE 配置适配公网，JWT 认证，HTTPS + Docker Compose 支持 |

---

## 二、业务架构

OPC 工作台的业务架构以"智能体"为中枢，以"项目"为主线，形成六大业务域的协同闭环。

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用户触点层                                   │
│   Web 控制台（CEO 指挥舱）  │  移动端 H5  │  IM 渠道  │  REST API    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                         核心业务域                                    │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ 项目管理  │  │ 任务中心  │  │ 智能体   │  │ 对话干预  │           │
│  │ 全生命周期│  │ Kanban   │  │ 编排中心  │  │ @Agent   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ 知识系统  │  │ 记忆追溯  │  │ 财务大盘  │  │ 安全审批  │           │
│  │ Wiki+技能 │  │ KAIROS   │  │ MRR/成本  │  │ Tool Guard│           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                         智能体引擎层                                   │
│   ReAct Agent  │  Plan-Execute  │  A2A 协议  │  Tool Guard          │
│   SOUL.md 人格  │  KAIROS 日志   │  状态机     │  Escalation 审批     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                         模型与能力层                                   │
│  模型池·Failover  │  多模态（图/音/视）  │  MCP 工具  │  知识检索      │
│  LiteLLM 统一路由  │  TTS/STT/Image/Video │  APScheduler│  向量搜索    │
└─────────────────────────────────────────────────────────────────────┘
```

### 以项目为核心的全生命周期工作流

一人公司 OPC 的项目从前期到交付的完整流程如下，所有环节均在 OPC 工作台中有对应的功能模块：

```
[前期商务]          [规划设计]         [开发执行]         [交付运营]         [财务结算]
Scout 发现线索  →  CoS 制定方案  →  各 Agent 执行  →  Closer 交付  →  Finance 结算
     │                  │                  │                  │               │
  渠道管理           Wiki 知识库        任务 Kanban         项目归档        财务记录
  客户记录           Brief.md           思考链日志          交付物管理       MRR 统计
  对话记录           状态机流转          CEO 审批            客户反馈         成本分析
```

---

## 三、技术架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OPC 工作台                                    │
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │  React 19    │    │  FastAPI     │    │  PostgreSQL           │  │
│  │  TypeScript  │◄──►│  Python 3.11 │◄──►│  (SQLite 开发)        │  │
│  │  Tailwind 4  │    │  SQLAlchemy  │    │  22 张核心表           │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│         │                   │                                       │
│         │ SSE/WebSocket      │ 文件系统读取                           │
│         │                   ▼                                       │
│         │         ┌──────────────────────┐                         │
│         │         │  ai-company-os/       │                         │
│         │         │  ├── SOUL.md (22个)   │                         │
│         │         │  ├── status.json      │                         │
│         │         │  ├── kairos_logs/     │                         │
│         │         │  └── finance_tracker  │                         │
│         │         └──────────────────────┘                         │
│         │                   │                                       │
│         ▼                   ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  LLM 多提供商路由层（LiteLLM）                 │   │
│  │  Claude Sonnet → GPT-4o → Gemini Pro → Ollama（按优先级）    │   │
│  │  健康检查 + 自动 Failover + 上下文保持                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  多模态能力层                                   │   │
│  │  图片生成 │ 语音合成(TTS) │ 语音识别(STT) │ 音乐 │ 视频 │ 3D  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 技术栈选型（完整版）

| 层级 | 技术选型 | 版本 | 选型理由 |
|---|---|---|---|
| **前端框架** | React | 19 | Phase 1 已有基础，生态成熟 |
| **前端语言** | TypeScript | 5.6 | 类型安全，与后端 Schema 对齐 |
| **前端路由** | Wouter | 3.x | 轻量，已集成 |
| **UI 组件库** | shadcn/ui + Radix UI | 最新 | 已集成，可高度定制，无样式锁定 |
| **样式系统** | Tailwind CSS | 4.x | 已集成，主题变量完整，OKLCH 色彩 |
| **图表库** | Recharts | 2.x | 已集成，支持响应式，声明式 API |
| **动画库** | Framer Motion | 12.x | 已集成，星系视图动效，流畅过渡 |
| **状态管理** | Zustand | 5.x | 轻量，适合中等复杂度，无样板代码 |
| **实时通信** | SSE（流式对话）+ WebSocket（状态推送） | — | SSE 适合单向流，WS 适合双向推送 |
| **Markdown 渲染** | Streamdown | 1.x | 已集成，支持流式渲染 |
| **代码高亮** | Shiki | 最新 | 高质量语法高亮，支持主题 |
| **命令面板** | cmdk | 1.x | 已集成，⌘K 面板基础 |
| **后端框架** | FastAPI | 0.115 | 与 kairos_daemon.py 同语言，异步支持好，自动 OpenAPI 文档 |
| **后端语言** | Python | 3.11 | 与现有 OPC 脚本同语言，AI 生态最佳 |
| **数据库（开发）** | SQLite | 3.x | 零配置，轻量启动 |
| **数据库（生产）** | PostgreSQL | 16 | 高并发，JSON 支持，全文搜索 |
| **ORM** | SQLAlchemy | 2.0 | 类型安全，异步支持，迁移管理 |
| **数据库迁移** | Alembic | 1.x | 与 SQLAlchemy 配套，版本化迁移 |
| **认证** | python-jose + bcrypt | — | JWT 标准方案，支持滑动续签 |
| **LLM 编排** | LangChain + LangGraph | 0.3 | Agent 状态图编排，ReAct + Plan-Execute |
| **LLM 路由** | LiteLLM | 1.x | 14+ 提供商统一接口，自动故障转移 |
| **任务调度** | APScheduler | 3.x | Cron 任务管理，与 kairos_daemon 兼容 |
| **向量数据库** | ChromaDB（本地）/ Qdrant（生产） | — | Wiki 语义搜索，记忆检索 |
| **文件存储** | 本地文件系统 + MinIO（可选） | — | 与 ai-company-os 目录直接集成 |
| **部署** | Docker Compose | — | 前后端一键启动，公网就绪 |
| **反向代理** | Nginx | — | HTTPS 终止，WebSocket 代理，静态文件服务 |

---

## 四、项目目录结构（详细版）

```
opc-dashboard/
│
├── client/                                  # React 前端（TypeScript）
│   ├── index.html                           # HTML 入口
│   └── src/
│       ├── main.tsx                         # React 入口
│       ├── App.tsx                          # 路由配置 + 全局 Provider
│       ├── index.css                        # 全局样式 + CSS 变量（暗/亮主题）
│       │
│       ├── pages/                           # 页面级组件（对应左侧导航）
│       │   ├── auth/
│       │   │   └── Login.tsx                # 登录页
│       │   ├── dashboard/
│       │   │   └── Dashboard.tsx            # 指挥大盘
│       │   ├── chat/
│       │   │   └── ChatConsole.tsx          # CEO 对话干预
│       │   ├── agents/
│       │   │   ├── AgentsPage.tsx           # 数字员工（活体图谱）
│       │   │   └── AgentDetail.tsx          # Agent 详情（路由参数）
│       │   ├── backstage/
│       │   │   ├── BackstagePage.tsx        # 后台（任务管理中心）
│       │   │   ├── ProjectDetail.tsx        # 项目详情
│       │   │   └── TaskDetail.tsx           # 任务详情
│       │   ├── orchestration/               # ★ 智能体编排（独立板块）
│       │   │   ├── OrchestrationPage.tsx    # 编排主页（工作流画布）
│       │   │   ├── WorkflowEditor.tsx       # 工作流编辑器
│       │   │   └── WorkflowRun.tsx          # 工作流执行监控
│       │   ├── wiki/
│       │   │   ├── WikiPage.tsx             # Wiki 知识库
│       │   │   └── WikiDoc.tsx              # 文档详情/编辑
│       │   ├── memory/
│       │   │   └── MemoryPage.tsx           # 记忆（KAIROS 时空追溯）
│       │   ├── channels/
│       │   │   └── ChannelsPage.tsx         # 渠道管理
│       │   ├── skills/
│       │   │   └── SkillsPage.tsx           # 技能管理
│       │   ├── plugins/
│       │   │   └── PluginsPage.tsx          # 插件管理
│       │   ├── activity/
│       │   │   └── ActivityPage.tsx         # 活动记录（审计日志）
│       │   ├── finance/
│       │   │   └── FinancePage.tsx          # 财务运营大盘
│       │   ├── settings/                    # 设置（多子页）
│       │   │   ├── SettingsLayout.tsx       # 设置布局（左侧二级导航）
│       │   │   ├── models/
│       │   │   │   └── ModelsPage.tsx       # 模型管理
│       │   │   ├── system/
│       │   │   │   └── SystemPage.tsx       # 系统设置
│       │   │   ├── multimodal/
│       │   │   │   ├── ImageGenPage.tsx     # 图片生成配置
│       │   │   │   ├── TTSPage.tsx          # 语音合成配置
│       │   │   │   ├── STTPage.tsx          # 语音识别配置
│       │   │   │   ├── MusicGenPage.tsx     # 音乐生成配置
│       │   │   │   ├── VideoGenPage.tsx     # 视频生成配置
│       │   │   │   └── ThreeDGenPage.tsx    # 3D 生成配置
│       │   │   ├── workspace/
│       │   │   │   ├── WorkspacePage.tsx    # 工作区管理
│       │   │   │   ├── AgentContextPage.tsx # 智能体上下文
│       │   │   │   ├── MembersPage.tsx      # 成员管理
│       │   │   │   └── AdvancedPage.tsx     # 高级选项
│       │   │   ├── apps/
│       │   │   │   ├── CronJobsPage.tsx     # 定时任务
│       │   │   │   ├── DatasourcesPage.tsx  # 数据源
│       │   │   │   ├── McpPage.tsx          # MCP 连接
│       │   │   │   ├── ToolsPage.tsx        # 工具目录
│       │   │   │   ├── AcpPage.tsx          # ACP 端点
│       │   │   │   ├── TokenUsagePage.tsx   # Token 统计
│       │   │   │   ├── FeatureFlagsPage.tsx # 功能开关
│       │   │   │   └── AboutPage.tsx        # 关于
│       │   └── security/
│       │       └── SecurityPage.tsx         # 安全（Tool Guard + 审批）
│       │
│       ├── components/                      # 复用组件
│       │   ├── layout/
│       │   │   ├── AppLayout.tsx            # 主布局（左导航 + 内容区）
│       │   │   ├── NavSidebar.tsx           # 左侧导航栏（图标 + 文字）
│       │   │   ├── MobileNav.tsx            # 移动端底部导航
│       │   │   └── SettingsLayout.tsx       # 设置页二级导航布局
│       │   ├── dashboard/
│       │   │   ├── KpiCard.tsx              # KPI 卡片
│       │   │   ├── ProjectGrid.tsx          # 活跃项目网格
│       │   │   ├── AgentWorkload.tsx        # Agent 工负排行
│       │   │   ├── ActivityFeed.tsx         # 最近活动流
│       │   │   └── AlertBanner.tsx          # 硬停警报横幅
│       │   ├── agent/
│       │   │   ├── GalaxyView.tsx           # 星系视图（Canvas/SVG）
│       │   │   ├── AgentCard.tsx            # Agent 卡片
│       │   │   ├── AgentDrawer.tsx          # SOUL.md 透视镜抽屉
│       │   │   └── AgentStatusDot.tsx       # 状态指示灯
│       │   ├── task/
│       │   │   ├── KanbanBoard.tsx          # Kanban 看板
│       │   │   ├── KanbanColumn.tsx         # 看板列
│       │   │   ├── TaskCard.tsx             # 任务卡片（可拖拽）
│       │   │   ├── TaskDrawer.tsx           # 任务详情抽屉
│       │   │   ├── ThinkingChain.tsx        # 思考链展示（折叠）
│       │   │   ├── NewTaskModal.tsx         # 新建任务弹窗
│       │   │   └── ProjectSidebar.tsx       # 项目列表侧边栏
│       │   ├── orchestration/
│       │   │   ├── FlowCanvas.tsx           # 工作流画布（基于 ReactFlow）
│       │   │   ├── AgentNode.tsx            # Agent 节点组件
│       │   │   ├── ConditionNode.tsx        # 条件判断节点
│       │   │   ├── TriggerNode.tsx          # 触发器节点
│       │   │   └── FlowToolbar.tsx          # 画布工具栏
│       │   ├── chat/
│       │   │   ├── ConversationList.tsx     # 会话列表
│       │   │   ├── MessageBubble.tsx        # 消息气泡（含 Markdown）
│       │   │   ├── ChatInput.tsx            # 输入框（@提及、文件拖拽）
│       │   │   ├── AgentMention.tsx         # @Agent 选择器
│       │   │   ├── ContextFiles.tsx         # 挂载上下文文件列表
│       │   │   └── ToolCallDisplay.tsx      # 工具调用展示
│       │   ├── finance/
│       │   │   ├── RevenueChart.tsx         # 月度营收趋势图
│       │   │   ├── CostPieChart.tsx         # 成本构成饼图
│       │   │   ├── FunnelChart.tsx          # 转化漏斗
│       │   │   └── FinanceTable.tsx         # 财务记录表格
│       │   ├── settings/
│       │   │   ├── ProviderCard.tsx         # LLM 提供商卡片
│       │   │   ├── ProviderModal.tsx        # 新增/编辑提供商弹窗
│       │   │   ├── McpModal.tsx             # MCP 连接弹窗
│       │   │   ├── TokenChart.tsx           # Token 消耗图表
│       │   │   └── FeatureToggle.tsx        # 功能开关行
│       │   ├── security/
│       │   │   ├── ApprovalCard.tsx         # 审批请求卡片
│       │   │   ├── RuleTable.tsx            # 安全规则表格
│       │   │   └── RuleModal.tsx            # 新增/编辑规则弹窗
│       │   └── shared/
│       │       ├── CommandPalette.tsx       # ⌘K 全局命令面板
│       │       ├── MarkdownEditor.tsx       # Markdown 编辑器（编辑/预览）
│       │       ├── FileTree.tsx             # 文件树组件
│       │       ├── StatusBadge.tsx          # 状态徽章
│       │       ├── PriorityBadge.tsx        # 优先级徽章
│       │       ├── ThemeToggle.tsx          # 暗色/亮色切换按钮
│       │       ├── EmptyState.tsx           # 空状态占位
│       │       └── ConfirmModal.tsx         # 确认对话框
│       │
│       ├── hooks/                           # 自定义 React Hook
│       │   ├── useAuth.ts                   # 认证状态管理
│       │   ├── useSSE.ts                    # SSE 流式数据订阅
│       │   ├── useWebSocket.ts              # WebSocket 连接管理
│       │   ├── useAgents.ts                 # Agent 数据获取
│       │   ├── useTasks.ts                  # 任务数据获取
│       │   ├── useConversation.ts           # 对话管理
│       │   ├── useCommandPalette.ts         # 命令面板状态
│       │   └── useTheme.ts                  # 主题切换
│       │
│       ├── stores/                          # Zustand 全局状态
│       │   ├── authStore.ts                 # 用户认证状态
│       │   ├── agentStore.ts                # Agent 状态（实时）
│       │   ├── taskStore.ts                 # 任务状态
│       │   ├── notificationStore.ts         # 通知/警报状态
│       │   └── themeStore.ts                # 主题偏好
│       │
│       └── lib/                             # 工具函数
│           ├── api.ts                       # Axios 实例 + 拦截器（JWT 自动刷新）
│           ├── opc-data.ts                  # OPC 数据类型定义
│           ├── soul-parser.ts               # SOUL.md YAML Frontmatter 解析
│           ├── kairos-parser.ts             # KAIROS 日志解析
│           └── utils.ts                     # 通用工具函数
│
├── server/                                  # FastAPI 后端（Python）
│   ├── main.py                              # FastAPI 入口 + 路由注册 + CORS
│   ├── requirements.txt                     # Python 依赖
│   │
│   ├── api/                                 # API 路由层
│   │   ├── v1/
│   │   │   ├── auth.py                      # 认证（登录/刷新/登出）
│   │   │   ├── dashboard.py                 # 仪表盘 KPI + 活动流
│   │   │   ├── agents.py                    # Agent 管理 CRUD
│   │   │   ├── projects.py                  # 项目管理 CRUD
│   │   │   ├── tasks.py                     # 任务管理 CRUD + 审批
│   │   │   ├── orchestration.py             # 智能体编排工作流
│   │   │   ├── chat.py                      # 对话（SSE 流式）
│   │   │   ├── timeline.py                  # KAIROS 日志时间线
│   │   │   ├── finance.py                   # 财务记录 CRUD
│   │   │   ├── wiki.py                      # Wiki 文档 CRUD
│   │   │   ├── memory.py                    # 记忆管理
│   │   │   ├── channels.py                  # 渠道配置 CRUD
│   │   │   ├── skills.py                    # 技能管理 CRUD
│   │   │   ├── plugins.py                   # 插件管理
│   │   │   ├── activity.py                  # 审计日志查询
│   │   │   ├── security.py                  # 安全规则 + 审批队列
│   │   │   ├── settings/
│   │   │   │   ├── models.py                # LLM 提供商管理
│   │   │   │   ├── system.py                # 系统配置
│   │   │   │   ├── multimodal.py            # 多模态配置
│   │   │   │   ├── workspace.py             # 工作区配置
│   │   │   │   ├── cron.py                  # 定时任务管理
│   │   │   │   ├── datasources.py           # 数据源管理
│   │   │   │   ├── mcp.py                   # MCP 连接管理
│   │   │   │   ├── tools.py                 # 工具目录
│   │   │   │   ├── acp.py                   # ACP 端点
│   │   │   │   ├── token_usage.py           # Token 统计
│   │   │   │   └── features.py              # 功能开关
│   │   │   └── ws.py                        # WebSocket 端点
│   │
│   ├── models/                              # SQLAlchemy ORM 模型（对应数据库表）
│   │   ├── user.py                          # users + refresh_tokens
│   │   ├── agent.py                         # agents + agent_tools + agent_stats
│   │   ├── project.py                       # projects
│   │   ├── task.py                          # tasks + task_comments
│   │   ├── orchestration.py                 # workflows + workflow_runs
│   │   ├── conversation.py                  # conversations + messages
│   │   ├── approval.py                      # approvals + security_rules
│   │   ├── cron.py                          # cron_jobs + cron_run_history
│   │   ├── finance.py                       # finance_records
│   │   ├── wiki.py                          # wiki_docs
│   │   ├── memory.py                        # memory_entries
│   │   ├── channel.py                       # channels
│   │   ├── skill.py                         # skills + agent_skills
│   │   ├── plugin.py                        # plugins
│   │   ├── audit.py                         # audit_logs
│   │   └── settings.py                      # llm_providers + system_config + token_usage
│   │
│   ├── schemas/                             # Pydantic 请求/响应模式
│   │   ├── auth.py
│   │   ├── agent.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── orchestration.py
│   │   ├── chat.py
│   │   └── ...（与 models/ 一一对应）
│   │
│   ├── services/                            # 业务逻辑层
│   │   ├── llm_router.py                    # LiteLLM 多提供商路由 + Failover
│   │   ├── agent_executor.py                # LangGraph Agent 执行引擎
│   │   ├── workflow_engine.py               # 工作流编排执行引擎
│   │   ├── file_reader.py                   # 文件系统读取（SOUL.md、status.json）
│   │   ├── soul_parser.py                   # SOUL.md YAML Frontmatter 解析
│   │   ├── kairos_parser.py                 # KAIROS 日志解析（JSON Lines）
│   │   ├── finance_sync.py                  # finance_tracker.csv 双向同步
│   │   ├── memory_service.py                # 记忆存储与检索（ChromaDB）
│   │   ├── tool_guard.py                    # Tool Guard 规则引擎
│   │   ├── cron_scheduler.py                # APScheduler 调度器
│   │   ├── channel_router.py                # IM 渠道消息路由
│   │   └── notification.py                  # WebSocket 通知推送
│   │
│   ├── core/                                # 核心配置
│   │   ├── config.py                        # 环境变量配置（Pydantic Settings）
│   │   ├── database.py                      # 数据库连接 + Session 管理
│   │   ├── security.py                      # JWT 工具函数
│   │   └── dependencies.py                  # FastAPI 依赖注入（get_db、get_current_user）
│   │
│   └── migrations/                          # Alembic 数据库迁移
│       ├── env.py
│       ├── versions/
│       │   └── 001_initial_schema.py        # 初始建表迁移
│       └── alembic.ini
│
├── docker-compose.yml                       # 生产部署（前端+后端+PostgreSQL+Nginx）
├── docker-compose.dev.yml                   # 开发环境（热重载）
├── Dockerfile.client                        # 前端 Docker 镜像
├── Dockerfile.server                        # 后端 Docker 镜像
├── nginx.conf                               # Nginx 反向代理配置（HTTPS + WebSocket）
└── .env.example                             # 环境变量示例
```

---

## 五、左侧导航体系（完整版）

参考 MateClaw 的三级导航结构，OPC 工作台的左侧导航按功能域分组，共 15 个主菜单项：

```
OPC 工作台
│
├── 核心
│   ├── 仪表盘          /dashboard          指挥大盘（KPI + 项目网格 + 警报）
│   ├── 对话            /chat               CEO 对话干预（@Agent + 上下文挂载）
│   ├── 数字员工        /agents             活体图谱（星系视图 + SOUL 透视镜）
│   ├── 后台            /backstage          任务管理中心（Kanban + 项目管理）
│   └── 编排            /orchestration      ★ 智能体编排（工作流画布）
│
├── 知识与记忆
│   ├── Wiki 知识库      /wiki               文档管理（文件树 + Markdown 编辑）
│   └── 记忆            /memory             KAIROS 时空追溯（决策时间线）
│
├── 连接
│   ├── 渠道            /channels           IM 渠道管理（微信/钉钉/Telegram 等）
│   ├── 技能            /skills             SKILL.md 技能矩阵
│   └── 插件            /plugins            第三方插件管理
│
├── 运营
│   ├── 活动记录        /activity           审计日志（全系统操作记录）
│   └── 财务大盘        /finance            营收/成本/转化漏斗（OPC 独有）
│
└── 系统
    ├── 设置            /settings           配置中心（二级导航，见下方）
    └── 安全            /security           Tool Guard + 审批队列
```

### 设置模块二级导航（完整版）

```
设置 /settings
│
├── 模型配置
│   ├── 模型管理        /settings/models    LLM 提供商 + Failover 优先级 + Embedding
│   ├── 图片生成        /settings/image-gen  图片生成提供商配置（DALL-E/Stable Diffusion）
│   ├── 语音合成        /settings/tts        TTS 提供商配置（OpenAI TTS/Azure/本地）
│   ├── 语音识别        /settings/stt        STT 提供商配置（Whisper/Azure）
│   ├── 音乐生成        /settings/music-gen  音乐生成配置（Suno/Udio API）
│   ├── 视频生成        /settings/video-gen  视频生成配置（Runway/Kling API）
│   └── 3D 生成         /settings/3d-gen     3D 生成配置
│
├── WORKSPACE
│   ├── 工作区          /settings/workspace  工作区基本信息 + 四大团队配置
│   ├── 智能体上下文    /settings/agent-ctx  Agent 上下文文件编辑器（SOUL.md/MEMORY.md）
│   ├── 成员管理        /settings/members    用户邀请 + 角色权限（CEO/Observer）
│   └── 高级            /settings/advanced   数据清理 + 导入导出 + 危险操作
│
└── 应用
    ├── 定时任务        /settings/cron        Cron 任务管理 + 执行历史
    ├── 数据源          /settings/datasources 数据库/API 数据源连接
    ├── MCP 连接        /settings/mcp         MCP 服务器管理（stdio/SSE/HTTP）
    ├── 工具目录        /settings/tools       内置工具启用/禁用
    ├── ACP 端点        /settings/acp         ACP 协议端点配置
    ├── Token 统计      /settings/tokens      消耗分析（按 Agent/模型/日期）
    ├── 功能开关        /settings/features    实验性功能开关
    ├── 系统设置        /settings/system      基础系统配置（语言/时区/通知）
    └── 关于            /settings/about       版本信息 + 更新日志
```

---

## 六、数据库设计（完整版，22 张表）

### 6.1 用户与认证（2 张表）

```sql
-- 用户表（仅 CEO 一人，保留多用户扩展能力）
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(20) DEFAULT 'ceo',     -- ceo | observer
    display_name    VARCHAR(100),
    avatar_url      TEXT,
    preferences_json JSONB DEFAULT '{}',           -- 主题偏好、语言等
    is_active       BOOLEAN DEFAULT TRUE,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- JWT 刷新令牌表（支持滑动续签）
CREATE TABLE refresh_tokens (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_hash  VARCHAR(255) UNIQUE NOT NULL,
    device_info TEXT,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    revoked     BOOLEAN DEFAULT FALSE
);
```

### 6.2 Agent 管理（3 张表）

```sql
-- Agent 主表（与文件系统 SOUL.md 双向同步）
CREATE TABLE agents (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(50) UNIQUE NOT NULL,   -- cos, scout, closer
    name            VARCHAR(100) NOT NULL,          -- CoS 首席参谋长
    team            VARCHAR(50) NOT NULL,           -- company | marketing | product | operations
    layer           VARCHAR(50) NOT NULL,           -- company | strategy | execution
    role_title      VARCHAR(200),
    soul_md_path    TEXT,
    soul_md_content TEXT,
    soul_md_hash    VARCHAR(64),
    status          VARCHAR(20) DEFAULT 'idle',    -- idle | active | busy | error | offline
    is_enabled      BOOLEAN DEFAULT TRUE,
    workload_score  REAL DEFAULT 0.0,
    last_active_at  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Agent 工具权限表
CREATE TABLE agent_tools (
    id                  SERIAL PRIMARY KEY,
    agent_id            INTEGER REFERENCES agents(id) ON DELETE CASCADE,
    tool_name           VARCHAR(100) NOT NULL,
    is_enabled          BOOLEAN DEFAULT TRUE,
    requires_approval   BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_id, tool_name)
);

-- Agent 运行统计表
CREATE TABLE agent_stats (
    id              SERIAL PRIMARY KEY,
    agent_id        INTEGER REFERENCES agents(id) ON DELETE CASCADE,
    date            DATE NOT NULL,
    token_input     INTEGER DEFAULT 0,
    token_output    INTEGER DEFAULT 0,
    api_calls       INTEGER DEFAULT 0,
    tasks_completed INTEGER DEFAULT 0,
    avg_response_ms REAL DEFAULT 0.0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_id, date)
);
```

### 6.3 项目与任务管理（3 张表）

```sql
-- 项目表（以项目为核心的业务主线）
CREATE TABLE projects (
    id              SERIAL PRIMARY KEY,
    project_id      VARCHAR(20) UNIQUE NOT NULL,   -- P-001
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    client          VARCHAR(200),
    status          VARCHAR(30) DEFAULT 'briefing',
    -- 状态机：briefing | planning | in_progress | review | approved | delivered | archived | cancelled
    phase           VARCHAR(30) DEFAULT 'presale',
    -- 阶段：presale（前期商务）| planning（规划设计）| execution（开发执行）| delivery（交付运营）| settled（财务结算）
    priority        VARCHAR(20) DEFAULT 'medium',
    brief_md_path   TEXT,
    status_json_path TEXT,
    assigned_agents JSONB DEFAULT '[]',
    deadline        DATE,
    budget          DECIMAL(12,2),
    revenue         DECIMAL(12,2),
    tags            JSONB DEFAULT '[]',
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 任务表（项目下的具体执行单元）
CREATE TABLE tasks (
    id              SERIAL PRIMARY KEY,
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    task_id         VARCHAR(30) UNIQUE NOT NULL,   -- T-001-01
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    status          VARCHAR(30) DEFAULT 'pending',
    -- 状态机（12状态）：
    -- pending | pending_ceo_approval | approved | planning | executing
    -- tool_call_pending | tool_call_approved | tool_call_rejected
    -- reviewing | completed | failed | cancelled
    priority        VARCHAR(20) DEFAULT 'medium',
    assigned_agent  VARCHAR(50),                   -- Agent slug
    parent_task_id  INTEGER REFERENCES tasks(id),
    plan_steps      JSONB DEFAULT '[]',
    thinking_log    TEXT,                          -- JSON Lines 格式
    tool_calls      JSONB DEFAULT '[]',
    result          TEXT,
    requires_ceo_approval BOOLEAN DEFAULT TRUE,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 任务评论表
CREATE TABLE task_comments (
    id          SERIAL PRIMARY KEY,
    task_id     INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    author      VARCHAR(50) NOT NULL,              -- 'ceo' 或 Agent slug
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.4 智能体编排（2 张表）

```sql
-- 工作流定义表
CREATE TABLE workflows (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    trigger_type    VARCHAR(30) DEFAULT 'manual',  -- manual | cron | event | webhook
    trigger_config  JSONB DEFAULT '{}',
    graph_json      JSONB NOT NULL,                -- ReactFlow 节点和边的完整定义
    is_enabled      BOOLEAN DEFAULT TRUE,
    last_run_at     TIMESTAMPTZ,
    run_count       INTEGER DEFAULT 0,
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 工作流执行历史表
CREATE TABLE workflow_runs (
    id              SERIAL PRIMARY KEY,
    workflow_id     INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    status          VARCHAR(20) DEFAULT 'running', -- running | completed | failed | cancelled
    input_data      JSONB DEFAULT '{}',
    output_data     JSONB DEFAULT '{}',
    execution_log   TEXT,                          -- JSON Lines 格式
    error_message   TEXT,
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);
```

### 6.5 对话系统（2 张表）

```sql
-- 对话会话表
CREATE TABLE conversations (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(500),
    agent_slug      VARCHAR(50),
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    context_files   JSONB DEFAULT '[]',
    llm_provider    VARCHAR(50),
    llm_model       VARCHAR(100),
    system_prompt   TEXT,
    total_tokens    INTEGER DEFAULT 0,
    is_archived     BOOLEAN DEFAULT FALSE,
    is_pinned       BOOLEAN DEFAULT FALSE,
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 消息表
CREATE TABLE messages (
    id              SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role            VARCHAR(20) NOT NULL,           -- user | assistant | system | tool
    content         TEXT NOT NULL,
    thinking        TEXT,                           -- Claude Thinking 内容
    tool_calls      JSONB DEFAULT '[]',
    token_count     INTEGER DEFAULT 0,
    llm_provider    VARCHAR(50),
    llm_model       VARCHAR(100),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.6 安全与审批（2 张表）

```sql
-- 审批请求表
CREATE TABLE approvals (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    requester_agent VARCHAR(50) NOT NULL,
    type            VARCHAR(30) NOT NULL,           -- tool_call | file_access | external_api | escalation
    priority        VARCHAR(20) DEFAULT 'medium',  -- low | medium | high | critical
    status          VARCHAR(20) DEFAULT 'pending', -- pending | approved | rejected | expired
    request_data    JSONB DEFAULT '{}',
    response_note   TEXT,
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    task_id         INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    expires_at      TIMESTAMPTZ,
    resolved_by     INTEGER REFERENCES users(id),
    resolved_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 安全规则表（Tool Guard）
CREATE TABLE security_rules (
    id              SERIAL PRIMARY KEY,
    rule_id         VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    pattern         TEXT NOT NULL,                 -- 正则表达式
    severity        VARCHAR(20) DEFAULT 'medium',  -- low | medium | high | critical
    category        VARCHAR(50),
    action          VARCHAR(20) DEFAULT 'block',   -- block | warn | approve
    target_tools    JSONB DEFAULT '[]',
    priority        INTEGER DEFAULT 100,
    is_enabled      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.7 定时任务（2 张表）

```sql
-- 定时任务表
CREATE TABLE cron_jobs (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    cron_expression VARCHAR(100) NOT NULL,
    agent_slug      VARCHAR(50),
    task_template   TEXT,                          -- Markdown 格式的任务描述模板
    is_enabled      BOOLEAN DEFAULT TRUE,
    last_run_at     TIMESTAMPTZ,
    next_run_at     TIMESTAMPTZ,
    run_count       INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 定时任务执行历史
CREATE TABLE cron_run_history (
    id              SERIAL PRIMARY KEY,
    cron_job_id     INTEGER REFERENCES cron_jobs(id) ON DELETE CASCADE,
    status          VARCHAR(20) DEFAULT 'running', -- running | completed | failed
    output          TEXT,
    error_message   TEXT,
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);
```

### 6.8 财务管理（1 张表）

```sql
-- 财务记录表
CREATE TABLE finance_records (
    id              SERIAL PRIMARY KEY,
    record_type     VARCHAR(20) NOT NULL,           -- income | expense
    category        VARCHAR(50) NOT NULL,
    -- income: project_payment | retainer | consulting
    -- expense: llm_api | tool_subscription | labor | marketing | other
    amount          DECIMAL(12,2) NOT NULL,
    currency        VARCHAR(10) DEFAULT 'CNY',
    description     TEXT,
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    record_date     DATE NOT NULL,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.9 知识与记忆（2 张表）

```sql
-- Wiki 文档表
CREATE TABLE wiki_docs (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(500) NOT NULL,
    content         TEXT,
    parent_id       INTEGER REFERENCES wiki_docs(id) ON DELETE SET NULL,
    doc_type        VARCHAR(20) DEFAULT 'document', -- document | folder
    file_path       TEXT,                           -- 对应文件系统路径（可选）
    tags            JSONB DEFAULT '[]',
    version         INTEGER DEFAULT 1,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_by      INTEGER REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 记忆条目表（KAIROS 日志的结构化存储）
CREATE TABLE memory_entries (
    id              SERIAL PRIMARY KEY,
    agent_slug      VARCHAR(50),
    project_id      INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    entry_type      VARCHAR(30) NOT NULL,           -- decision | observation | reflection | escalation
    summary         TEXT NOT NULL,
    content         TEXT,
    thesis          TEXT,                           -- 正（最终决策）
    antithesis      TEXT,                           -- 反（被否定的备选）
    synthesis       TEXT,                           -- 合（综合考量）
    source_file     TEXT,                           -- 来源 kairos_logs 文件路径
    source_line     INTEGER,
    embedding       VECTOR(1536),                   -- 向量嵌入（pgvector）
    recorded_at     TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 6.10 连接与能力（3 张表）

```sql
-- IM 渠道表
CREATE TABLE channels (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    channel_type    VARCHAR(30) NOT NULL,           -- wechat | dingtalk | feishu | telegram | discord | slack
    credentials     JSONB DEFAULT '{}',             -- 加密存储 API Token/AppID 等
    webhook_url     TEXT,
    bound_agent     VARCHAR(50),
    is_enabled      BOOLEAN DEFAULT TRUE,
    message_filter  JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 技能表
CREATE TABLE skills (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    category        VARCHAR(50),
    skill_md_path   TEXT,
    skill_md_content TEXT,
    is_enabled      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Agent-技能关联表（多对多）
CREATE TABLE agent_skills (
    agent_id    INTEGER REFERENCES agents(id) ON DELETE CASCADE,
    skill_id    INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (agent_id, skill_id)
);
```

### 6.11 系统配置（3 张表）

```sql
-- LLM 提供商配置表
CREATE TABLE llm_providers (
    id              SERIAL PRIMARY KEY,
    provider_id     VARCHAR(50) UNIQUE NOT NULL,   -- openai | anthropic | gemini | custom
    name            VARCHAR(100) NOT NULL,
    base_url        TEXT,
    api_key_encrypted TEXT,                        -- AES 加密存储
    models          JSONB DEFAULT '[]',
    priority        INTEGER DEFAULT 100,
    is_enabled      BOOLEAN DEFAULT TRUE,
    health_status   VARCHAR(20) DEFAULT 'unknown', -- healthy | degraded | down | unknown
    last_check_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 系统配置表（键值对）
CREATE TABLE system_config (
    key             VARCHAR(100) PRIMARY KEY,
    value           TEXT,
    description     TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Token 消耗统计表
CREATE TABLE token_usage (
    id              SERIAL PRIMARY KEY,
    agent_slug      VARCHAR(50),
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE SET NULL,
    task_id         INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    provider_id     VARCHAR(50),
    model           VARCHAR(100),
    token_input     INTEGER DEFAULT 0,
    token_output    INTEGER DEFAULT 0,
    cost_usd        DECIMAL(10,6) DEFAULT 0,
    recorded_at     TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 七、功能模块详细设计（15 个模块）

### 7.1 仪表盘（Dashboard）

**页面布局**：顶部 KPI 脉搏条（4个卡片）+ 中部两栏（左：活跃项目网格，右：系统脉搏心电图）+ 底部两栏（左：Agent 工负排行，右：最近活动流）。当有待审批事项时，顶部显示红色硬停警报横幅。

**数据来源**：聚合 `tasks`、`token_usage`、`approvals`、`projects` 表，以及 `kairos_logs` 文件。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/dashboard/kpi` | 今日/本周/本月 KPI 汇总 |
| GET | `/api/v1/dashboard/projects` | 活跃项目列表（含进度） |
| GET | `/api/v1/dashboard/activity-feed` | 最近 50 条活动记录 |
| WS | `/ws/dashboard` | Agent 状态实时推送（每 5 秒） |

---

### 7.2 对话（ChatConsole）

**页面布局**：左侧会话列表（可折叠）+ 中间对话区（Markdown 渲染 + 流式输出）+ 右侧 Agent 信息面板（可折叠）。

**核心功能**：`@Agent名称` 自动注入 SOUL.md 为 System Prompt；拖拽文件挂载上下文；Claude Thinking 模式折叠展示；工具调用实时展示；多会话 Tab 并行；会话导出 Markdown。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/conversations` | 会话列表（分页、搜索） |
| POST | `/api/v1/conversations` | 新建会话 |
| PUT | `/api/v1/conversations/{id}` | 更新会话（标题、置顶、归档） |
| DELETE | `/api/v1/conversations/{id}` | 删除会话 |
| GET | `/api/v1/conversations/{id}/messages` | 消息历史 |
| SSE | `/api/v1/conversations/{id}/chat` | 流式对话（含工具调用流） |
| POST | `/api/v1/conversations/{id}/context` | 添加上下文文件 |
| DELETE | `/api/v1/conversations/{id}/context/{file}` | 移除上下文文件 |

---

### 7.3 数字员工（Agents）

**页面布局**：顶部视图切换（星系视图/卡片视图/列表视图）+ 主体内容区 + 右侧 SOUL 透视镜抽屉。

**星系视图**：以 CoS 为中心，四大团队为同心轨道，节点大小反映工负分数，发光强度反映实时活跃度，连线表示 A2A 协作关系。

**增删改查**：增（上传 SOUL.md 创建新 Agent）；删（仅禁用，不物理删除）；改（名称、状态、工具权限、SOUL.md 内容）；查（按团队/状态/工负筛选）。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/agents` | Agent 列表（含状态） |
| GET | `/api/v1/agents/{slug}` | Agent 详情（含 SOUL.md） |
| POST | `/api/v1/agents` | 创建 Agent（上传 SOUL.md） |
| PUT | `/api/v1/agents/{slug}` | 更新 Agent 配置 |
| POST | `/api/v1/agents/{slug}/sync-soul` | 从文件系统重新同步 SOUL.md |
| GET | `/api/v1/agents/{slug}/stats` | Agent 运行统计 |
| GET | `/api/v1/agents/graph` | A2A 协作关系图数据 |
| SSE | `/api/v1/agents/stream` | Agent 状态变更实时流 |

---

### 7.4 后台（Backstage）— 任务管理中心

这是 OPC 工作台中最核心的功能模块，解决"如何发布任务、如何执行任务、如何管理任务"的问题，以项目为主线串联所有任务。

**页面布局**：左侧项目列表（按阶段分组）+ 中间 Kanban 看板（12 状态列）+ 右侧任务详情抽屉。

**12 状态机看板**：

| 状态 | 含义 | 操作者 |
|---|---|---|
| pending | 草稿，尚未提交 | CEO |
| pending_ceo_approval | 等待 CEO 确认执行 | CEO |
| approved | CEO 已批准，等待 Agent 接收 | 系统 |
| planning | Agent 正在制定执行计划 | Agent |
| executing | Agent 正在执行 | Agent |
| tool_call_pending | 工具调用等待 CEO 审批 | CEO |
| tool_call_approved | 工具调用已批准 | 系统 |
| tool_call_rejected | 工具调用被拒绝 | 系统 |
| reviewing | Agent 正在审核执行结果 | Agent |
| completed | 已完成 | 系统 |
| failed | 执行失败（含错误信息） | 系统 |
| cancelled | 已取消 | CEO |

**CEO 确认流程**：新建任务 → 进入 `pending_ceo_approval` → 仪表盘顶部显示待确认徽章 → CEO 查看 Agent 执行计划后 Approve → 状态变为 `approved` → WebSocket 通知 Agent 开始执行。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/projects` | 项目列表（按阶段/状态筛选） |
| POST | `/api/v1/projects` | 新建项目 |
| PUT | `/api/v1/projects/{id}` | 更新项目 |
| DELETE | `/api/v1/projects/{id}` | 归档项目（软删除） |
| GET | `/api/v1/tasks` | 任务列表（支持多维筛选） |
| POST | `/api/v1/tasks` | 新建任务 |
| GET | `/api/v1/tasks/{id}` | 任务详情 |
| PUT | `/api/v1/tasks/{id}` | 更新任务（状态/指派/优先级） |
| DELETE | `/api/v1/tasks/{id}` | 取消任务（软删除） |
| POST | `/api/v1/tasks/{id}/approve` | CEO 批准任务执行 |
| POST | `/api/v1/tasks/{id}/reject` | CEO 拒绝任务 |
| POST | `/api/v1/tasks/{id}/stop` | 停止执行中的任务 |
| GET | `/api/v1/tasks/{id}/thinking-log` | 获取思考链日志 |
| SSE | `/api/v1/tasks/{id}/stream` | 任务执行实时进度流 |
| POST | `/api/v1/tasks/{id}/comments` | 添加评论 |

---

### 7.5 ★ 智能体编排（Orchestration）— 独立板块

这是 OPC 工作台的核心创新模块，提供可视化的多智能体工作流编排能力，让 CEO 无需编写代码即可定义复杂的 Agent 协作流程。

**页面布局**：左侧工作流列表 + 中间画布编辑区（ReactFlow）+ 右侧节点配置面板。

**工作流画布**：基于 ReactFlow 实现，支持以下节点类型：

| 节点类型 | 图标 | 功能 |
|---|---|---|
| 触发器节点 | ⚡ | 定义工作流启动条件（手动/Cron/事件/Webhook） |
| Agent 节点 | 🤖 | 指定执行 Agent + 任务描述 + 输入/输出变量 |
| 条件节点 | ◇ | 基于上一步输出的条件分支（if/else） |
| 并行节点 | ⊞ | 多个 Agent 并行执行，等待全部完成 |
| 合并节点 | ⊟ | 汇总并行节点的输出 |
| 审批节点 | ✋ | 暂停工作流，等待 CEO 审批后继续 |
| 工具节点 | 🔧 | 直接调用特定工具（API/数据库/文件操作） |
| 结束节点 | ⬛ | 定义工作流输出和结束条件 |

**预置 OPC 工作流模板**：
- **新客户接入流程**：Scout 收集信息 → CoS 评估 → CEO 审批 → Closer 跟进
- **项目启动流程**：CoS 制定计划 → CEO 确认 → 各 Agent 并行执行
- **每日晨报流程**：CoS 汇总 → 财务快照 → 推送给 CEO
- **交付审核流程**：Agent 自检 → CoS 审核 → CEO 最终确认 → Closer 交付

**增删改查**：增（从模板创建或空白画布创建）；删（软删除）；改（画布编辑，节点配置，触发器设置）；查（按状态/触发类型筛选，查看执行历史）。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/orchestration/workflows` | 工作流列表 |
| POST | `/api/v1/orchestration/workflows` | 创建工作流 |
| GET | `/api/v1/orchestration/workflows/{id}` | 工作流详情（含 graph_json） |
| PUT | `/api/v1/orchestration/workflows/{id}` | 更新工作流（保存画布） |
| DELETE | `/api/v1/orchestration/workflows/{id}` | 删除工作流 |
| POST | `/api/v1/orchestration/workflows/{id}/run` | 手动触发执行 |
| PUT | `/api/v1/orchestration/workflows/{id}/toggle` | 启用/禁用 |
| GET | `/api/v1/orchestration/workflows/{id}/runs` | 执行历史列表 |
| GET | `/api/v1/orchestration/runs/{run_id}` | 执行详情（含实时日志） |
| SSE | `/api/v1/orchestration/runs/{run_id}/stream` | 执行实时进度流 |
| GET | `/api/v1/orchestration/templates` | 预置模板列表 |

---

### 7.6 Wiki 知识库

**页面布局**：左侧文件树（支持文件夹嵌套，拖拽排序）+ 右侧 Markdown 编辑器（编辑/预览/分屏三模式）。

**增删改查**：增（新建文档/文件夹，支持模板）；删（软删除，保留 30 天）；改（在线 Markdown 编辑，自动版本快照）；查（全文搜索 + 语义搜索，支持双向链接 `[[文档名]]`）。

---

### 7.7 记忆（KAIROS 时空追溯）

**页面布局**：顶部筛选栏（Agent/项目/类型/日期范围）+ 主体垂直时间线 + 悬浮正反合透镜。

**正反合透镜**（OPC 独有）：每条决策日志展开后显示三段式分析（正：最终决策；反：被否定的备选方案；合：综合考量的权衡过程）。

---

### 7.8 渠道（Channels）

**增删改查**：增（选择渠道类型，填写凭证，测试连通性）；删（停用后删除）；改（编辑凭证，切换绑定 Agent，调整消息过滤规则）；查（查看消息历史，按渠道/时间筛选）。

支持国内 5 个渠道（微信、钉钉、飞书、企业微信、QQ）和海外 3 个渠道（Telegram、Discord、Slack）。

---

### 7.9 技能（Skills）

**增删改查**：增（上传 SKILL.md 文件）；删（停用后删除）；改（编辑描述，分配给 Agent）；查（技能矩阵卡片视图，按类别分组，查看使用统计）。

---

### 7.10 插件（Plugins）

**增删改查**：增（从插件市场安装或手动上传）；删（卸载）；改（配置插件参数，授权给特定 Agent）；查（按状态/类别筛选，查看版本信息）。

---

### 7.11 活动记录

全系统操作的审计日志，支持按操作者（用户/Agent/系统）、资源类型、操作类型、时间范围过滤。每条记录显示时间、操作者、操作内容、资源、前后状态 diff 视图。支持导出 CSV。

---

### 7.12 财务大盘（OPC 独有）

**页面布局**：顶部 KPI（MRR/ARR/本月收入/本月成本/AI 成本占比）+ 中部图表区（月度趋势折线图 + 成本构成饼图）+ 底部（转化漏斗 + 项目收入排行 + 财务记录表）。

**增删改查**：增（新建财务记录弹窗：日期/类型/分类/金额/描述/关联项目）；删（软删除）；改（编辑记录）；查（按日期范围/类型/分类筛选，支持导入 CSV 和导出报表）。

---

### 7.13 设置（Settings）

设置模块按照三级导航结构组织（见第五章），每个子页面遵循"配置项 + 测试按钮 + 保存按钮"的统一布局模式。

**模型管理核心交互**：点击"启用提供商" → 从内置目录选择或自定义 → 填写 API Key → 点击"测试连通性" → 测试通过后保存 → 设置 Failover 优先级（拖拽排序）。

**多模态配置**（图片/语音/音乐/视频/3D）：每类能力可配置多个提供商，设置默认值，测试连通性。

**MCP 连接**：支持 stdio/SSE/HTTP 三种协议，连接成功后自动发现可用工具，可选择性启用/禁用。

**Token 统计**：按 Agent/模型/日期多维分析，显示估算 USD 成本，支持自定义时间范围。

---

### 7.14 安全（Security）

**子页面**：Tool Guard 规则管理 / 审批队列 / 审计日志。

**审批队列**：待审批列表按优先级排序（critical 置顶），点击展开完整请求详情，CEO 可批准/拒绝并填写备注，操作后通过 WebSocket 实时通知对应 Agent。

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/approvals` | 审批列表（状态筛选） |
| POST | `/api/v1/approvals/{id}/approve` | 批准 |
| POST | `/api/v1/approvals/{id}/reject` | 拒绝 |
| GET | `/api/v1/security/rules` | 安全规则列表 |
| POST | `/api/v1/security/rules` | 新建规则 |
| PUT | `/api/v1/security/rules/{id}` | 更新规则 |
| DELETE | `/api/v1/security/rules/{id}` | 删除规则 |
| GET | `/api/v1/audit-logs` | 审计日志（分页、筛选） |

---

## 八、⌘K 全局命令面板

按下 `Ctrl+K`（Windows）或 `⌘K`（Mac）唤起，支持以下命令类型：

| 命令模式 | 示例 | 动作 |
|---|---|---|
| 导航 | `go dashboard` | 跳转到指挥大盘 |
| Agent 对话 | `chat cos` | 打开与 CoS 的对话 |
| 任务操作 | `new task` | 打开新建任务弹窗 |
| 审批操作 | `approve APR-001` | 直接批准审批请求 |
| 项目跳转 | `project P-001` | 跳转到项目详情 |
| 工作流触发 | `run workflow 晨报` | 立即触发指定工作流 |
| 搜索 | `search 用户画像` | 全局搜索（任务/文档/对话） |
| 配置 | `settings models` | 跳转到模型配置 |

---

## 九、移动端适配方案

移动端采用底部 Tab 导航（5 个主要入口：仪表盘、对话、后台、通知、更多），隐藏左侧导航栏。

| 页面 | 桌面端 | 移动端 |
|---|---|---|
| 指挥大盘 | 多栏网格 | 单列滚动，KPI 卡片 2×2 |
| 数字员工 | 星系视图 + 抽屉 | 列表视图，点击展开详情 |
| 任务管理 | Kanban 看板 | 单列列表，状态标签筛选 |
| 对话干预 | 三栏布局 | 全屏对话，底部输入框 |
| 智能体编排 | 全屏画布 | 只读查看，不支持编辑 |
| 审批中心 | 表格 + 详情 | 卡片列表，滑动操作 |

---

## 十、暗色/亮色主题方案

主题切换通过 CSS 变量实现，用户偏好存储在 `localStorage` 和 `users.preferences_json` 中，实现跨设备同步。

**暗色主题**（默认）：深空黑底色 `#080C14`，电青 `#00D4FF` 为主强调色，Space Grotesk + JetBrains Mono 字体组合，适合长时间工作的 CEO 指挥舱场景。

**亮色主题**：参考 MateClaw 的暖米色/沙漠棕风格，`#FAF8F5` 底色，`#C85C3A`（砖红）为主强调色，保持与暗色主题相同的字体体系，适合日间演示和汇报场景。

---

## 十一、MateClaw UI 可直接借鉴的组件模式

| 组件/模式 | MateClaw 来源 | OPC 应用位置 |
|---|---|---|
| 三栏布局（导航+内容+抽屉） | MainLayout.vue | 所有主页面 |
| Agent 卡片网格 | Agents.vue | 活体图谱列表视图 |
| Kanban 看板 + 状态拖拽 | Backstage.vue | 任务管理中心 |
| 思考链折叠展示 | ChatConsole.vue | 任务详情 + 对话界面 |
| 模型提供商弹窗 | Settings/Models.vue | 配置中心模型管理 |
| 安全规则表格 + 新增弹窗 | Security/ToolGuard.vue | 安全审批中心 |
| MCP 连接管理弹窗 | McpServers.vue | 配置中心 MCP 管理 |
| 工具目录启用/禁用开关 | Tools.vue | Agent 工具权限管理 |
| Agent 上下文文件编辑器 | AgentContext.vue | 配置中心 Agent 上下文 |
| Token 统计日期范围图表 | TokenUsage.vue | 配置中心 Token 统计 |
| 功能开关列表 | FeatureFlags.vue | 配置中心功能开关 |
| 登录页（用户名/密码） | Login.vue | 登录页 |
| Cron 任务表格 + 立即运行 | CronJobs.vue | 定时任务管理 |
| 数据源连接测试弹窗 | Datasources.vue | MCP/工具连接测试 |

---

## 十二、六阶段开发路线图

| 阶段 | 时间 | 核心交付 | 关键里程碑 |
|---|---|---|---|
| Phase 1 | 已完成 | 基础框架 + 静态可视化（6 个视图，mock 数据） | ✅ 工作台可访问 |
| Phase 2 | Week 1-2 | 全栈化：FastAPI + PostgreSQL + JWT 登录 + 真实数据 | 真实 SOUL.md 数据上屏，可登录 |
| Phase 3 | Week 3 | 任务管理中心：Kanban + CEO 确认流 + 思考链 | 第一个任务从发布到完成闭环 |
| Phase 4 | Week 4 | 对话干预 + 审批流 + 智能体编排（画布） | CEO 可与 Agent 对话，工作流可视化 |
| Phase 5 | Week 5 | 设置中心：模型管理 + LiteLLM + 多模态 + MCP | 多模型切换，MCP 工具可用 |
| Phase 6 | Week 6 | 财务大盘 + Wiki + 渠道 + 移动端 + Docker 部署 | 公网可访问，移动端可用，完整闭环 |

---

## 十三、Phase 2 开发前置清单

在启动 Phase 2 之前，需要完成以下准备工作：

1. 执行 `webdev_add_feature web-db-user`，获得 PostgreSQL 数据库和后端服务器能力
2. 运行 Alembic 迁移脚本，创建上述 22 张数据表
3. 配置环境变量：`DATABASE_URL`、`JWT_SECRET`、至少一个 `LLM_API_KEY`
4. 运行初始化脚本，将 22 个 SOUL.md 文件导入 `agents` 表
5. 配置 CORS，允许前端域名访问后端 API
6. 安装前端新依赖：`reactflow`（工作流画布）、`zustand`（状态管理）、`shiki`（代码高亮）

---

*文档版本：v6.0（最终版）| 最后更新：2026-05-05 | 整合自 v4 + v5，新增智能体编排板块和详细目录架构*
