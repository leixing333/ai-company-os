# OPC 工作台完整开发规划 v5

> **版本说明：** 本文档基于 MateClaw 三张架构图（UI 导航截图、业务架构图、技术架构图）深度分析，结合 OPC 现有系统成果，整合用户补充的完整导航结构与设置模块，形成可直接指导开发的最终规划。

---

## 一、核心设计原则

OPC 工作台的核心定位是 **"一人公司的 AI 指挥中枢"**，而非通用的多智能体平台。这意味着它在完整复刻 MateClaw 功能体系的基础上，还需要承载 OPC 独有的业务语义：SOUL.md 人格体系、KAIROS 决策日志、四大团队工作区隔离，以及 CEO 对所有 Agent 行动的最终确认权。

设计上遵循三个原则：**深空操控台视觉风格**（暗色为主、亮色可切换）、**宏观委托与微观引导的交互范式**（CEO 发布意图，系统分解执行，关键节点回报确认），以及**移动端与桌面端功能对等**（响应式设计，核心操作在手机端同样可用）。

---

## 二、完整导航体系

参照 MateClaw 的分组逻辑，OPC 工作台的左侧导航分为六个层级组，并在此基础上增加 OPC 独有的"财务"分组。

### 导航结构总览

| 分组 | 菜单项 | 对应 OPC 功能 |
|---|---|---|
| **核心** | 仪表盘 | 指挥大盘：KPI 脉搏、活跃项目网格、硬停警报 |
| **核心** | 对话 | CEO 干预中心：@Agent 注入 SOUL.md，多会话并行 |
| **核心** | 数字员工 | 活体图谱：星系视图，20 个 Agent，SOUL 透视镜 |
| **核心** | 后台 | 任务管理：Kanban 看板，CEO 确认流，思考链展示 |
| **知识** | Wiki 知识库 | 结构化文档，双向链接，引用溯源，lazy 入库 |
| **记忆** | 记忆 | KAIROS 时空追溯：决策日志，正反合透镜 |
| **连接** | 渠道 | IM 渠道配置：微信、钉钉、飞书、Telegram、Discord |
| **连接** | 技能 | 技能矩阵：SKILL.md 管理，技能市场 |
| **连接** | 插件 | 插件管理：第三方工具集成，ClawHub 兼容 |
| **活动** | 活动记录 | 审计日志：操作历史，Token 消耗统计 |
| **财务（OPC 独有）** | 财务大盘 | MRR/ARR，成本分析，转化漏斗，交付记录 |
| **系统** | 设置 | 完整配置中心（见下方详细展开） |
| **系统** | 安全 | Tool Guard + 审批流 + RBAC 权限管理 |

### 设置（Settings）完整子菜单

设置模块是整个系统的神经中枢，分为四个子分组，覆盖所有多模态能力的接入配置。

**模型配置分组**涵盖 Chat 模型与 Embedding 模型的提供商管理（支持 OpenAI、Anthropic、DashScope、Gemini、Ollama 等 14+ 供应商，含健康追踪与自动 Failover），以及图片生成、语音合成（TTS）、语音识别（STT）、音乐生成、视频生成、3D 生成六类多模态能力的独立配置入口。每类能力均支持启用内置提供商或自定义提供商，并可进行连通性测试。

**WORKSPACE 分组**管理工作区隔离（对应 OPC 四大团队：公司层、战略层、市场层、生产层）、智能体上下文策略（短期窗口大小、长期记忆触发阈值）、成员管理（用户邀请、角色分配、权限矩阵），以及高级选项（日志级别、调试模式、实验性功能）。

**应用分组**包含定时任务（APScheduler 可视化管理，支持 Cron 表达式和间隔模式）、数据源（外部数据库连接配置）、MCP 连接（stdio/SSE/HTTP 三种协议，工具发现与注册）、工具目录（内置工具的启用/禁用管理）、ACP 端点（Agent Communication Protocol，对外暴露的 API 端点配置）、Token 统计（按 Agent/模型/时间维度的消耗分析）、功能开关（灰度发布控制），以及关于（版本信息、许可证、更新日志）。

---

## 三、业务架构

OPC 工作台的业务架构以 **Agent 智能体** 为核心，形成六大支撑系统的星形结构，与 MateClaw 业务架构完全对齐，并在每个维度上融入 OPC 的业务语义。

```
                    ┌─────────────────────────────────┐
                    │           用户触点层              │
                    │  Web 控制台 │ 移动端 │ REST API   │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │         OPC Agent 核心           │
                    │   LangGraph ReAct + Plan-Execute  │
                    │   20 个 SOUL.md 人格化 Agent      │
                    └──┬────┬────┬────┬────┬──────────┘
                       │    │    │    │    │
          ┌────────────┘    │    │    │    └────────────┐
          ▼                 ▼    ▼    ▼                  ▼
   ┌─────────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐
   │  知识系统    │  │工具与技能 │  │安全与审批 │  │  记忆系统   │
   │ Wiki KB     │  │MCP+Skills│  │ToolGuard │  │KAIROS Logs  │
   │ 双向链接    │  │ 插件市场  │  │ CEO 确认  │  │ 正反合透镜  │
   └─────────────┘  └──────────┘  └──────────┘  └─────────────┘
          ▲                                              ▲
          └──────────────────┬───────────────────────────┘
                             ▼
                   ┌──────────────────┐
                   │  模型池·Failover  │
                   │  LiteLLM 统一抽象 │
                   │  14+ 供应商自动切换│
                   └──────────────────┘
                             ▲
                   ┌──────────────────┐
                   │   多模态创作引擎  │
                   │ TTS/STT/图/音/视  │
                   └──────────────────┘
```

---

## 四、技术架构

OPC 工作台采用 Python + TypeScript 双栈方案，以 FastAPI 为后端核心，React 19 为前端框架，LangGraph 为 Agent 编排引擎，LiteLLM 为模型统一接入层。

### 技术栈分层

| 架构层 | 技术选型 | 对标 MateClaw | 说明 |
|---|---|---|---|
| **表现层** | React 19 + Tailwind 4 + shadcn/ui | Vue 3 + Element Plus | Web SPA，暗/亮双主题 |
| **实时通信** | SSE（FastAPI EventSourceResponse） | Spring MVC SSE | 流式对话 + 工具执行流 |
| **API 层** | FastAPI + OpenAPI 自动文档 | SpringDoc OpenAPI | REST + WebSocket |
| **Agent 引擎** | LangGraph（ReAct + Plan-Execute） | Spring AI Alibaba | 状态图，循环推理 |
| **模型接入** | LiteLLM（统一代理，Failover） | Spring AI 统一抽象 | 14+ 供应商，自动切换 |
| **认证授权** | JWT + RBAC（python-jose） | Spring Security | 滑动窗口续签 |
| **数据持久层** | SQLAlchemy + Alembic + PostgreSQL | MyBatis Plus + MySQL | ORM + 自动迁移 |
| **文件系统** | 本地文件系统（SOUL.md + kairos_logs） | 文件系统 | OPC 独有，原样读取 |
| **定时任务** | APScheduler（AsyncIOScheduler） | Spring Scheduling | Cron + 间隔模式 |
| **MCP 协议** | mcp-python-sdk（stdio/SSE/HTTP） | MCP 协议 | 工具发现与注册 |
| **多模态引擎** | 各供应商 API（通过 LiteLLM 路由） | 多模态引擎 | TTS/STT/图/音/视 |
| **部署** | Docker Compose（前端 + 后端 + DB） | Docker Compose | 一键公网部署 |
| **移动端** | 响应式 CSS + 底部 Tab 导航 | — | OPC 独有需求 |

---

## 五、数据库设计（完整 Schema）

### 5.1 用户与认证

**`users` 表**存储系统用户信息，字段包括 `id`（UUID 主键）、`username`（唯一用户名）、`email`（唯一邮箱）、`hashed_password`、`role`（枚举：super_admin / admin / member / viewer）、`avatar_url`、`is_active`、`last_login_at`、`created_at`、`updated_at`。

**`refresh_tokens` 表**管理 JWT 刷新令牌，字段包括 `id`、`user_id`（外键）、`token_hash`（哈希存储）、`expires_at`、`revoked`、`created_at`，支持多设备并发登录与强制下线。

**`workspaces` 表**管理工作区隔离，字段包括 `id`、`name`（如"公司层"/"市场层"）、`slug`（URL 标识）、`description`、`icon`、`owner_id`、`settings_json`（工作区级别配置）、`created_at`。

**`workspace_members` 表**管理工作区成员关系，字段包括 `id`、`workspace_id`、`user_id`、`role`（枚举：owner / admin / member / viewer）、`joined_at`。

### 5.2 Agent 管理

**`agents` 表**是系统核心表，存储所有数字员工信息，字段包括 `id`（UUID）、`name`（Agent 名称，如"CoS"）、`slug`（唯一标识，如"cos"）、`workspace_id`（所属工作区）、`soul_md_path`（SOUL.md 文件路径）、`soul_content`（缓存的 SOUL.md 内容）、`role`（角色定位）、`team`（团队：company/strategy/marketing/production）、`layer`（层级：company/strategy/execution）、`status`（枚举：idle/thinking/executing/waiting/error/offline）、`current_task_id`（当前执行的任务）、`model_config_json`（Agent 级别的模型配置覆盖）、`tool_permissions_json`（允许使用的工具列表）、`max_tokens_per_run`、`avatar_url`、`is_active`、`last_active_at`、`created_at`、`updated_at`。

**`agent_stats` 表**记录 Agent 运行统计，字段包括 `id`、`agent_id`、`date`（统计日期）、`tasks_completed`、`tasks_failed`、`total_tokens_used`、`total_api_calls`、`avg_response_time_ms`、`uptime_seconds`。

**`agent_tools` 表**管理 Agent 与工具的关联，字段包括 `id`、`agent_id`、`tool_name`、`tool_type`（枚举：builtin/mcp/skill/plugin）、`is_enabled`、`requires_approval`（是否需要 CEO 审批）、`config_json`。

### 5.3 任务管理

**`projects` 表**存储项目信息，字段包括 `id`（UUID）、`title`、`description`、`workspace_id`、`owner_agent_id`（负责 Agent）、`status`（枚举：draft/planning/active/paused/completed/archived）、`priority`（枚举：critical/high/medium/low）、`brief_md_path`（brief.md 文件路径）、`start_date`、`due_date`、`completed_at`、`tags_json`、`metadata_json`、`created_by`、`created_at`、`updated_at`。

**`tasks` 表**存储任务详情，字段包括 `id`（UUID）、`project_id`（外键）、`title`、`description`、`assignee_agent_id`（执行 Agent）、`reviewer_agent_id`（审核 Agent）、`status`（12 状态机：draft/pending_ceo_approval/approved/planning/executing/tool_call_pending/tool_call_approved/tool_call_rejected/reviewing/completed/failed/cancelled）、`priority`、`parent_task_id`（支持子任务树）、`depends_on_json`（依赖任务 ID 列表）、`plan_json`（Plan-Execute 生成的执行计划）、`result_json`（执行结果）、`error_message`、`estimated_tokens`、`actual_tokens`、`due_date`、`started_at`、`completed_at`、`created_by`、`created_at`、`updated_at`。

**`task_comments` 表**存储任务评论与 CEO 批注，字段包括 `id`、`task_id`、`author_type`（枚举：ceo/agent/system）、`author_id`、`content`、`comment_type`（枚举：comment/approval/rejection/note）、`created_at`。

**`task_thinking_chains` 表**存储 Agent 思考链（对标 MateClaw 后台的 Thought 展示），字段包括 `id`、`task_id`、`agent_id`、`step_index`、`step_type`（枚举：think/act/observe/plan/result）、`content`、`tool_name`、`tool_input_json`、`tool_output_json`、`tokens_used`、`created_at`。

### 5.4 对话系统

**`conversations` 表**存储对话会话，字段包括 `id`（UUID）、`title`（自动生成或手动命名）、`user_id`、`agent_id`（对话的 Agent，NULL 表示全局对话）、`workspace_id`、`context_files_json`（挂载的上下文文件路径列表）、`model_override`（会话级别模型覆盖）、`system_prompt_override`（覆盖 SOUL.md 的自定义 System Prompt）、`is_pinned`、`is_archived`、`message_count`、`last_message_at`、`created_at`、`updated_at`。

**`messages` 表**存储对话消息，字段包括 `id`（UUID）、`conversation_id`、`role`（枚举：user/assistant/system/tool）、`content`（文本内容）、`content_type`（枚举：text/markdown/image/audio/video/file）、`attachments_json`（附件信息）、`tool_calls_json`（工具调用详情）、`model_used`（实际使用的模型）、`tokens_input`、`tokens_output`、`latency_ms`、`is_streaming_complete`、`created_at`。

### 5.5 安全与审批

**`approvals` 表**存储所有需要 CEO 审批的事项，字段包括 `id`（UUID）、`type`（枚举：task_start/tool_call/agent_action/budget_exceed/escalation）、`agent_id`（发起审批的 Agent）、`task_id`（关联任务）、`title`（审批标题）、`description`（详细说明）、`context_json`（完整上下文，包含 Agent 的推理过程）、`options_json`（可选的操作选项）、`status`（枚举：pending/approved/rejected/expired）、`reviewer_id`（审批人）、`reviewer_comment`、`decided_at`、`expires_at`、`created_at`。

**`security_rules` 表**存储 Tool Guard 规则，字段包括 `id`、`name`（规则名称）、`description`、`rule_type`（枚举：allow/deny/require_approval）、`scope`（枚举：global/workspace/agent）、`scope_id`（对应 workspace_id 或 agent_id）、`condition_json`（触发条件，如工具名称、参数模式）、`action_json`（触发后的动作）、`priority`（规则优先级）、`is_active`、`created_by`、`created_at`、`updated_at`。

**`audit_logs` 表**存储完整审计日志，字段包括 `id`（UUID）、`event_type`（事件类型）、`actor_type`（枚举：user/agent/system）、`actor_id`、`resource_type`（操作的资源类型）、`resource_id`、`action`（执行的操作）、`before_json`（操作前状态）、`after_json`（操作后状态）、`ip_address`、`user_agent`、`created_at`。

### 5.6 LLM 与模型管理

**`llm_providers` 表**存储模型提供商配置，字段包括 `id`、`name`（提供商名称）、`provider_type`（枚举：openai/anthropic/dashscope/gemini/ollama/custom）、`base_url`、`api_key_encrypted`（加密存储）、`models_json`（支持的模型列表）、`is_active`、`is_default`、`health_status`（枚举：healthy/degraded/down）、`last_health_check_at`、`priority`（Failover 优先级）、`config_json`（额外配置）、`created_at`、`updated_at`。

**`multimodal_providers` 表**存储多模态能力提供商，字段包括 `id`、`capability_type`（枚举：image_gen/tts/stt/music_gen/video_gen/3d_gen）、`provider_name`、`api_key_encrypted`、`config_json`、`is_active`、`is_default`、`created_at`。

**`token_usage` 表**记录 Token 消耗，字段包括 `id`、`date`（统计日期）、`agent_id`、`conversation_id`、`task_id`、`model_name`、`provider_name`、`tokens_input`、`tokens_output`、`cost_usd`（估算成本）、`created_at`。

### 5.7 知识与记忆

**`wiki_docs` 表**存储知识库文档，字段包括 `id`（UUID）、`workspace_id`、`title`、`content`（Markdown 内容）、`content_vector`（Embedding 向量，用于语义搜索）、`parent_id`（支持树形结构）、`path`（文档路径，如"/产品/功能规划"）、`tags_json`、`source_type`（枚举：manual/agent_generated/imported）、`source_agent_id`、`is_published`、`view_count`、`created_by`、`created_at`、`updated_at`。

**`memory_entries` 表**存储 Agent 记忆（对应 KAIROS 日志），字段包括 `id`（UUID）、`agent_id`、`task_id`、`memory_type`（枚举：episodic/semantic/procedural）、`content`（记忆内容）、`importance_score`（重要性评分，用于长期记忆筛选）、`thesis`（正：最终决策）、`antithesis`（反：备选方案）、`synthesis`（合：综合考量）、`tags_json`、`expires_at`（短期记忆过期时间）、`created_at`。

### 5.8 连接与集成

**`channels` 表**存储 IM 渠道配置，字段包括 `id`、`name`（渠道名称）、`channel_type`（枚举：wechat/dingtalk/feishu/telegram/discord/slack/qq/weibo）、`config_json`（渠道特定配置，如 Token、AppID）、`webhook_url`、`is_active`、`agent_id`（绑定的 Agent）、`created_at`、`updated_at`。

**`mcp_connections` 表**存储 MCP 连接配置，字段包括 `id`、`name`、`protocol`（枚举：stdio/sse/http）、`endpoint`（连接地址或命令）、`config_json`、`discovered_tools_json`（自动发现的工具列表）、`is_active`、`last_connected_at`、`created_at`。

**`skills` 表**存储技能定义，字段包括 `id`、`name`、`slug`、`description`、`skill_md_path`（SKILL.md 文件路径）、`skill_content`（缓存内容）、`category`、`version`、`is_active`、`usage_count`、`created_at`、`updated_at`。

**`cron_jobs` 表**存储定时任务，字段包括 `id`、`name`、`description`、`job_type`（枚举：agent_task/report/cleanup/sync）、`schedule_type`（枚举：cron/interval）、`cron_expression`、`interval_seconds`、`agent_id`（执行 Agent）、`payload_json`（任务参数）、`is_active`、`next_run_at`、`last_run_at`、`last_run_status`、`run_count`、`created_at`、`updated_at`。

**`cron_run_history` 表**存储定时任务执行历史，字段包括 `id`、`cron_job_id`、`started_at`、`completed_at`、`status`（枚举：running/success/failed）、`result_json`、`error_message`、`tokens_used`。

### 5.9 财务管理（OPC 独有）

**`finance_records` 表**存储财务记录，字段包括 `id`（UUID）、`record_type`（枚举：revenue/cost/refund）、`category`（收入类别或成本类别）、`amount`（金额，单位：分，避免浮点精度问题）、`currency`（默认 CNY）、`description`、`client_name`、`project_id`（关联项目）、`invoice_url`、`record_date`、`created_by`、`created_at`、`updated_at`。

---

## 六、功能模块详细规划

### 6.1 仪表盘（Dashboard）

仪表盘是 CEO 每日开机后首先看到的页面，需要在 5 秒内传达系统的整体健康状态。页面分为四个区域：顶部 KPI 脉搏条（显示今日活跃 Agent 数、进行中任务数、待审批事项数、本月 MRR）；中部活跃项目网格（每个项目卡片显示名称、负责 Agent、进度条、最近活动时间）；右侧硬停警报抽屉（当有 `status=pending` 的 Approval 记录时，自动展开显示审批队列）；底部 Agent 工负排行（按当日 Token 消耗排序，展示前 5 名 Agent 的工作强度）。

**API 端点：**
- `GET /api/v1/dashboard/summary` — 获取 KPI 汇总数据
- `GET /api/v1/dashboard/active-projects` — 获取活跃项目列表（分页）
- `GET /api/v1/dashboard/agent-workload` — 获取 Agent 工负排行
- `GET /api/v1/approvals?status=pending` — 获取待审批列表
- `SSE /api/v1/dashboard/stream` — 实时推送状态变更

### 6.2 对话（Chat）

对话模块是 CEO 与 Agent 进行实时交互的核心入口。左侧为会话列表（支持搜索、置顶、归档、删除），右侧为对话主区域（支持 Markdown 渲染、代码高亮、流式输出）。

**核心功能：**
- `@Agent名称` 语法：在对话框中输入 `@CoS` 即自动将该 Agent 的 SOUL.md 注入为 System Prompt，实现人格化对话
- **上下文挂载**：拖拽文件（brief.md、status.json 等）到对话框，作为附加上下文
- **多会话并行**：支持同时与多个 Agent 开启独立会话，Tab 切换
- **模型覆盖**：每个会话可独立选择使用的模型，不受全局配置影响
- **会话导出**：将对话内容导出为 Markdown 文件

**API 端点：**
- `POST /api/v1/conversations` — 创建新会话
- `GET /api/v1/conversations` — 获取会话列表（分页、搜索）
- `GET /api/v1/conversations/{id}/messages` — 获取消息历史
- `POST /api/v1/conversations/{id}/messages` — 发送消息（返回 SSE 流）
- `PUT /api/v1/conversations/{id}` — 更新会话配置（标题、置顶、归档）
- `DELETE /api/v1/conversations/{id}` — 删除会话
- `POST /api/v1/conversations/{id}/upload` — 上传上下文文件

### 6.3 数字员工（Agents）

数字员工模块以"活体图谱"的形式展示所有 20 个 Agent，采用星系视图：以 CoS（参谋长）为中心，四大团队（公司层、战略层、市场层、生产层）分布在四条轨道上，Agent 节点的发光强度实时反映其工作负载。

**核心功能：**
- **星系视图**：基于 Canvas 或 SVG 实现，节点可拖拽，支持缩放
- **SOUL 透视镜**：点击任意 Agent 节点，右侧展开 SOUL.md 详情面板（角色定位、核心能力、工具权限、当前状态、历史任务统计）
- **状态实时更新**：通过 SSE 订阅 Agent 状态变更，节点颜色和动效实时响应
- **增删改查**：管理员可新增 Agent（上传 SOUL.md）、编辑配置、停用/启用、删除

**API 端点：**
- `GET /api/v1/agents` — 获取所有 Agent 列表（含状态）
- `GET /api/v1/agents/{id}` — 获取单个 Agent 详情（含 SOUL.md 内容）
- `POST /api/v1/agents` — 创建新 Agent（上传 SOUL.md）
- `PUT /api/v1/agents/{id}` — 更新 Agent 配置
- `DELETE /api/v1/agents/{id}` — 删除 Agent
- `GET /api/v1/agents/{id}/stats` — 获取 Agent 统计数据
- `SSE /api/v1/agents/stream` — 订阅所有 Agent 状态变更流

### 6.4 后台（Backstage）— 任务管理中心

后台模块是 OPC 工作台中最核心的补充，解决"如何发布任务、如何执行任务、如何管理任务"的问题。页面采用三栏布局：左侧为项目列表，中间为 Kanban 看板（按 12 状态机分列），右侧为任务详情面板（含思考链展示）。

**12 状态机看板列：**

| 状态 | 含义 | 负责人 |
|---|---|---|
| draft | 草稿，尚未提交 | CEO |
| pending_ceo_approval | 等待 CEO 确认 | CEO |
| approved | CEO 已批准 | — |
| planning | Agent 正在制定计划 | Agent |
| executing | Agent 正在执行 | Agent |
| tool_call_pending | 工具调用待审批 | CEO |
| tool_call_approved | 工具调用已批准 | — |
| tool_call_rejected | 工具调用被拒绝 | — |
| reviewing | 结果审核中 | Agent |
| completed | 已完成 | — |
| failed | 执行失败 | — |
| cancelled | 已取消 | CEO |

**核心功能：**
- **任务发布**：CEO 填写任务标题、描述、优先级、截止日期，选择执行 Agent，提交后进入 `pending_ceo_approval` 状态
- **CEO 确认流**：任务进入 `pending_ceo_approval` 后，仪表盘顶部显示审批提示，CEO 可查看 Agent 生成的执行计划后 Approve/Reject
- **思考链展示**：任务执行过程中，右侧面板实时展示 Agent 的 Think/Act/Observe 步骤，类似 MateClaw 后台的 Thought 展示
- **子任务树**：支持任务分解为子任务，树形展示依赖关系
- **批量操作**：支持批量修改状态、批量分配 Agent、批量设置优先级

**API 端点：**
- `GET /api/v1/projects` — 获取项目列表
- `POST /api/v1/projects` — 创建项目
- `PUT /api/v1/projects/{id}` — 更新项目
- `DELETE /api/v1/projects/{id}` — 删除项目（软删除）
- `GET /api/v1/tasks?project_id={id}&status={status}` — 获取任务列表
- `POST /api/v1/tasks` — 创建任务
- `PUT /api/v1/tasks/{id}` — 更新任务（含状态流转）
- `POST /api/v1/tasks/{id}/approve` — CEO 批准任务
- `POST /api/v1/tasks/{id}/reject` — CEO 拒绝任务
- `GET /api/v1/tasks/{id}/thinking-chain` — 获取思考链
- `SSE /api/v1/tasks/{id}/stream` — 订阅任务执行实时流

### 6.5 Wiki 知识库

Wiki 模块提供结构化知识管理，支持树形目录、Markdown 编辑、双向链接（`[[文档名]]` 语法自动创建链接）、引用溯源（显示哪些 Agent 引用了该文档）。

**增删改查：**
- 创建文档（支持模板）、编辑（在线 Markdown 编辑器）、删除（软删除，保留 30 天）、搜索（全文搜索 + 语义搜索）
- 文档版本历史（每次保存自动创建版本快照）
- 文档权限（公开/工作区内/仅自己）
- 从 Agent 对话中一键保存内容到 Wiki

### 6.6 记忆（KAIROS 时空追溯）

记忆模块将 KAIROS 追加式日志转化为可交互的决策时间线，是 OPC 系统独有的功能，在 MateClaw 中没有对应模块。

**核心交互：**
- **垂直时间线**：按日期分组，每条记录显示 Agent 名称、决策类型、简要描述
- **正反合透镜**：悬停或点击任意记录，展开三段式分析（正：最终决策；反：被否定的备选方案；合：综合考量的权衡过程）
- **过滤器**：按 Agent、项目、决策类型、日期范围多维过滤
- **搜索**：全文搜索决策内容
- **导出**：将时间线导出为 PDF 报告

### 6.7 渠道（Channels）

渠道模块管理所有 IM 渠道的接入配置，支持国内 5 个（微信、钉钉、飞书、企业微信、QQ）和海外 3 个（Telegram、Discord、Slack）渠道。

每个渠道的配置项包括：渠道名称、渠道类型、API Token/AppID/AppSecret（加密存储）、Webhook URL（用于接收消息）、绑定的 Agent（哪个 Agent 负责回复该渠道的消息）、是否启用、消息过滤规则（白名单/黑名单）。

**增删改查：** 添加渠道（选择类型，填写凭证，测试连通性）、编辑配置、停用/启用、删除、查看消息历史。

### 6.8 技能（Skills）

技能模块管理所有 SKILL.md 技能文件，提供技能矩阵视图（按类别分组的卡片布局）和技能详情（SKILL.md 内容渲染）。

**增删改查：** 上传新技能（上传 SKILL.md 文件）、编辑技能描述、分配给 Agent（多对多关联）、停用/启用、删除、查看使用统计（哪些 Agent 使用了该技能，使用频率）。

### 6.9 插件（Plugins）

插件模块管理第三方工具集成，兼容 ClawHub 插件格式。每个插件包含名称、描述、版本、作者、安装状态、配置项（API Key 等）、权限要求（需要访问哪些系统资源）。

**增删改查：** 从插件市场安装、手动上传安装包、配置插件参数、授权给特定 Agent 使用、更新版本、卸载。

### 6.10 活动记录

活动记录模块展示系统中所有操作的审计日志，支持按操作者（用户/Agent/系统）、资源类型、操作类型、时间范围过滤。每条记录显示时间、操作者、操作内容、资源、操作前后状态对比（diff 视图）。支持导出为 CSV 文件。

### 6.11 财务大盘（OPC 独有）

财务大盘展示公司的财务健康状况，分为四个区域：顶部 KPI（本月 MRR、ARR、净利润、AI 成本占比）；中部月度趋势图（营收与成本的折线图，使用 Recharts）；左下角成本构成饼图（LLM API 成本、人力成本、工具订阅费用等）；右下角转化漏斗（潜在客户→意向客户→成交客户→复购客户）。

**增删改查：** 手动录入财务记录（类型、金额、日期、描述）、编辑记录、删除记录、导入 CSV、导出报表。

### 6.12 设置（Settings）

设置模块按照前述的三级导航结构组织，每个子页面均遵循"配置项 + 测试按钮 + 保存按钮"的统一布局模式。

**模型管理**的核心交互是：点击"启用提供商"→ 从内置目录选择或自定义 → 填写 API Key → 点击"测试连通性"→ 测试通过后保存 → 设置为默认或调整 Failover 优先级。Embedding 模型单独管理，与 Chat 模型共享 Provider 的 API Key。

**多模态配置**（图片生成、语音合成等）的交互模式与模型管理一致，每类能力可配置多个提供商并设置默认值。

**MCP 连接**支持三种协议：stdio（本地进程，填写命令行）、SSE（远程服务，填写 URL）、HTTP（REST 接口，填写 URL）。连接成功后自动发现并列出可用工具，管理员可选择性地启用/禁用工具。

**Token 统计**提供多维度的消耗分析：按 Agent 分组、按模型分组、按日期分组，支持自定义时间范围，并显示估算的 USD 成本。

### 6.13 安全（Security）

安全模块分为三个子页面：Tool Guard 规则管理（可视化规则编辑器，支持条件组合）、审批流管理（查看所有待审批/已审批/已拒绝的事项，支持批量操作）、用户与权限管理（RBAC 角色配置，用户邀请与权限分配）。

---

## 七、⌘K 全局命令面板

⌘K 命令面板是贯穿整个工作台的极速操作入口，按下 `Ctrl+K`（Windows）或 `⌘K`（Mac）即可唤起。支持的命令类型包括：

| 命令模式 | 示例 | 功能 |
|---|---|---|
| 导航 | `go dashboard` | 跳转到指定页面 |
| Agent 操作 | `@CoS` | 打开与 CoS 的对话 |
| 任务操作 | `approve P-001` | 批准指定任务 |
| 项目跳转 | `project 网站改版` | 跳转到指定项目 |
| 快速创建 | `new task` | 打开新建任务对话框 |
| 搜索 | `search 用户画像` | 全局搜索 |

---

## 八、移动端适配方案

移动端采用底部 Tab 导航（5 个主要入口：仪表盘、对话、后台、通知、我），隐藏左侧导航栏。核心操作（审批、任务查看、对话）在移动端完整支持，配置类操作（设置、安全规则编辑）引导用户使用桌面端。

---

## 九、暗色/亮色主题方案

主题切换通过 CSS 变量实现，在 `client/src/index.css` 中定义 `:root`（亮色）和 `.dark`（暗色）两套完整的颜色变量。用户的主题偏好存储在 `localStorage` 中，并同步到 `users` 表的 `preferences_json` 字段，实现跨设备同步。

**暗色主题**（默认）：深空黑底色 `#080C14`，电青 `#00D4FF` 为主强调色，Space Grotesk + JetBrains Mono 字体。

**亮色主题**：参考 MateClaw 的暖米色/沙漠棕风格，`#FAF8F5` 底色，`#C85C3A`（砖红）为主强调色，保持与暗色主题相同的字体体系。

---

## 十、六阶段开发路线图

| 阶段 | 时间 | 核心交付 | 关键里程碑 |
|---|---|---|---|
| Phase 1 | 已完成 | 基础框架 + 静态可视化（6 个视图，mock 数据） | ✅ 工作台可访问 |
| Phase 2 | Week 1-2 | 全栈化：FastAPI 后端 + PostgreSQL + JWT 登录 + 真实数据替换 mock | 真实 SOUL.md 数据上屏 |
| Phase 3 | Week 3 | 任务管理中心：Kanban 看板 + CEO 确认流 + 思考链展示 | 第一个任务从发布到完成 |
| Phase 4 | Week 4 | 对话干预：@Agent 注入 SOUL.md + SSE 流式输出 + 审批流 | CEO 可与 Agent 实时对话 |
| Phase 5 | Week 5 | 设置中心：模型管理 + LiteLLM Failover + 多模态配置 + MCP 连接 | 多模型切换正常运行 |
| Phase 6 | Week 6 | 财务大盘 + Wiki + 渠道 + 移动端 + Docker Compose 一键部署 | 公网可访问，移动端可用 |

---

## 十一、Phase 2 开发前置清单

在启动 Phase 2 之前，需要完成以下准备工作：

1. **升级为全栈项目**：执行 `webdev_add_feature web-db-user`，获得 PostgreSQL 数据库和后端服务器能力
2. **初始化数据库**：运行 Alembic 迁移脚本，创建上述所有数据表
3. **配置环境变量**：设置 `DATABASE_URL`、`JWT_SECRET`、`LLM_API_KEY`（至少一个）
4. **导入 SOUL.md 数据**：运行初始化脚本，将 22 个 SOUL.md 文件导入 `agents` 表
5. **配置 CORS**：允许前端域名访问后端 API

---

*文档版本：v5.0 | 最后更新：2026-05-05 | 基于 MateClaw v1.2.0-SNAPSHOT 架构分析*
