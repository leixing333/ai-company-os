# OPC Dashboard 分阶段开发 TODO 清单

> **文档说明**：本清单基于 `OPC_Final_Development_Plan_v6.md`（整合 v4+v5 全部内容）生成，细化到具体文件创建/修改、API 端点实现、UI 组件开发、数据库迁移等粒度。确认后即可指导 Phase 2 开发启动。
>
> **图例**：✅ 已完成 | ⬜ 待完成 | 🔴 阻塞项 | ⭐ 核心里程碑

---

## Phase 0：前置准备（Phase 2 启动前必须完成）

### P0.1 项目升级
- ⬜ 执行 `webdev_add_feature web-db-user`，获得 PostgreSQL + 后端服务器能力
- ⬜ 确认升级后 `server/` 目录结构（FastAPI 入口、数据库配置等）
- ⬜ 验证开发服务器正常启动（前端 + 后端均可访问）

### P0.2 后端依赖安装
- ⬜ 创建 `server/requirements.txt`，包含以下依赖：
  ```
  fastapi==0.115.0
  uvicorn[standard]==0.32.0
  sqlalchemy==2.0.36
  alembic==1.14.0
  psycopg2-binary==2.9.10
  python-jose[cryptography]==3.3.0
  passlib[bcrypt]==1.7.4
  python-multipart==0.0.12
  pydantic-settings==2.6.0
  litellm==1.52.0
  langchain==0.3.7
  langgraph==0.2.50
  apscheduler==3.10.4
  mcp==1.2.0
  chromadb==0.5.23
  httpx==0.28.0
  python-dotenv==1.0.1
  aiofiles==24.1.0
  ```
- ⬜ 执行 `pip install -r server/requirements.txt`

### P0.3 前端新依赖安装
- ⬜ 安装 `reactflow`（智能体编排画布）：`pnpm add @xyflow/react`
- ⬜ 安装 `zustand`（全局状态管理）：`pnpm add zustand`
- ⬜ 安装 `shiki`（代码高亮）：`pnpm add shiki`
- ⬜ 安装 `axios`（HTTP 客户端）：`pnpm add axios`
- ⬜ 安装 `@dnd-kit/core @dnd-kit/sortable`（Kanban 拖拽）：`pnpm add @dnd-kit/core @dnd-kit/sortable`
- ⬜ 安装 `react-markdown`（Markdown 渲染）：`pnpm add react-markdown remark-gfm`
- ⬜ 安装 `date-fns`（日期处理）：`pnpm add date-fns`
- ⬜ 安装 `react-hot-toast`（Toast 通知）：`pnpm add react-hot-toast`

### P0.4 环境变量配置
- ⬜ 创建 `.env.example` 文件，包含以下变量：
  ```env
  # 数据库
  DATABASE_URL=postgresql://opc:password@localhost:5432/opc_db
  
  # JWT
  JWT_SECRET=your-super-secret-key-min-32-chars
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=15
  REFRESH_TOKEN_EXPIRE_DAYS=30
  
  # OPC 文件系统路径
  OPC_BASE_PATH=/home/ubuntu/ai-company-os
  SOULS_BASE_PATH=/home/ubuntu/ai-company-os/1_company/agents
  KAIROS_LOGS_PATH=/home/ubuntu/ai-company-os/kairos_logs
  FINANCE_CSV_PATH=/home/ubuntu/ai-company-os/finance_tracker.csv
  STATUS_JSON_PATH=/home/ubuntu/ai-company-os/status.json
  
  # LLM（至少配置一个）
  ANTHROPIC_API_KEY=sk-ant-...
  OPENAI_API_KEY=sk-...
  
  # 加密密钥（API Key 存储加密）
  ENCRYPTION_KEY=your-32-byte-encryption-key
  
  # 前端
  VITE_API_BASE_URL=http://localhost:8000
  VITE_WS_BASE_URL=ws://localhost:8000
  ```
- ⬜ 复制 `.env.example` 为 `.env` 并填入实际值

### P0.5 数据库初始化
- ⬜ 创建 `server/core/database.py`（SQLAlchemy 连接 + Session 管理）
- ⬜ 创建 `server/migrations/alembic.ini`
- ⬜ 创建 `server/migrations/env.py`（Alembic 迁移环境）
- ⬜ 创建 `server/migrations/versions/001_initial_schema.py`（22 张表完整建表迁移）
- ⬜ 执行 `alembic upgrade head` 完成建表
- ⬜ 创建 `server/scripts/seed_agents.py`（从 SOUL.md 文件系统导入 22 个 Agent）
- ⬜ 执行 seed 脚本，验证 `agents` 表有 22 条记录

### P0.6 初始用户创建
- ⬜ 创建 `server/scripts/create_admin.py`（创建 CEO 账户）
- ⬜ 执行脚本，创建初始 CEO 用户（用户名：`ceo`，密码通过环境变量注入）

---

## Phase 1：基础框架（已完成）✅

### P1 已完成内容
- ✅ 项目初始化：`/home/ubuntu/opc-dashboard`（React 19 + Tailwind 4 + shadcn/ui）
- ✅ 深空操控台主题（`#080C14` 背景，`#00D4FF` 强调色）
- ✅ 左侧导航栏（`client/src/components/NavSidebar.tsx`）
- ✅ 指挥大盘视图（`client/src/components/DashboardView.tsx`，mock 数据）
- ✅ 活体图谱星系视图（`client/src/components/GalaxyView.tsx`，mock 数据）
- ✅ 时空追溯时间线（`client/src/components/TimelineView.tsx`，mock 数据）
- ✅ 财务大盘（`client/src/components/FinanceView.tsx`，mock 数据）
- ✅ 终端视图（`client/src/components/TerminalView.tsx`）
- ✅ 配置中心（`client/src/components/SettingsView.tsx`）
- ✅ ⌘K 全局命令面板（`client/src/components/CommandPalette.tsx`）
- ✅ OPC 数据类型定义（`client/src/lib/opc-data.ts`）
- ✅ 主路由和状态管理（`client/src/App.tsx`）
- ✅ Checkpoint 保存（版本：`92c014e3`）

---

## Phase 2：全栈化 + JWT 登录 + 真实数据（Week 1-2）⭐

**目标**：将 Phase 1 静态 mock 数据替换为真实文件系统数据，建立完整前后端通信，实现可登录的工作台。

### P2.1 后端框架搭建（Week 1，Day 1-2）

#### 核心文件创建
- ⬜ 创建 `server/main.py`：FastAPI 应用入口，注册所有路由，配置 CORS（允许前端域名），挂载静态文件
- ⬜ 创建 `server/core/config.py`：Pydantic Settings，从 `.env` 读取所有环境变量
- ⬜ 创建 `server/core/security.py`：JWT 工具函数（生成 Access Token、Refresh Token，验证 Token）
- ⬜ 创建 `server/core/dependencies.py`：FastAPI 依赖注入（`get_db`、`get_current_user`、`require_ceo`）

#### 数据模型层
- ⬜ 创建 `server/models/user.py`：`User`、`RefreshToken` SQLAlchemy ORM 模型
- ⬜ 创建 `server/models/agent.py`：`Agent`、`AgentTool`、`AgentStat` ORM 模型
- ⬜ 创建 `server/models/project.py`：`Project` ORM 模型
- ⬜ 创建 `server/models/task.py`：`Task`、`TaskComment` ORM 模型
- ⬜ 创建 `server/models/conversation.py`：`Conversation`、`Message` ORM 模型
- ⬜ 创建 `server/models/approval.py`：`Approval`、`SecurityRule` ORM 模型
- ⬜ 创建 `server/models/cron.py`：`CronJob`、`CronRunHistory` ORM 模型
- ⬜ 创建 `server/models/finance.py`：`FinanceRecord` ORM 模型
- ⬜ 创建 `server/models/wiki.py`：`WikiDoc` ORM 模型
- ⬜ 创建 `server/models/memory.py`：`MemoryEntry` ORM 模型
- ⬜ 创建 `server/models/channel.py`：`Channel` ORM 模型
- ⬜ 创建 `server/models/skill.py`：`Skill`、`AgentSkill` ORM 模型
- ⬜ 创建 `server/models/orchestration.py`：`Workflow`、`WorkflowRun` ORM 模型
- ⬜ 创建 `server/models/settings.py`：`LlmProvider`、`SystemConfig`、`TokenUsage` ORM 模型
- ⬜ 创建 `server/models/audit.py`：`AuditLog` ORM 模型

#### Pydantic Schema 层
- ⬜ 创建 `server/schemas/auth.py`：`LoginRequest`、`TokenResponse`、`UserResponse`
- ⬜ 创建 `server/schemas/agent.py`：`AgentResponse`、`AgentUpdate`、`AgentStatResponse`
- ⬜ 创建 `server/schemas/project.py`：`ProjectCreate`、`ProjectResponse`、`ProjectUpdate`
- ⬜ 创建 `server/schemas/task.py`：`TaskCreate`、`TaskResponse`、`TaskUpdate`、`TaskComment`
- ⬜ 创建 `server/schemas/conversation.py`：`ConversationCreate`、`MessageResponse`
- ⬜ 创建 `server/schemas/common.py`：分页响应 `PaginatedResponse`、错误响应 `ErrorResponse`

### P2.2 认证系统（Week 1，Day 2-3）

#### 后端 API
- ⬜ 创建 `server/api/v1/auth.py`，实现以下端点：
  - `POST /api/v1/auth/login`：验证用户名/密码（bcrypt），返回 Access Token + Refresh Token
  - `POST /api/v1/auth/refresh`：用 Refresh Token 换取新 Access Token（滑动续签）
  - `POST /api/v1/auth/logout`：撤销 Refresh Token
  - `GET /api/v1/auth/me`：返回当前用户信息

#### 前端登录页
- ⬜ 创建 `client/src/pages/auth/Login.tsx`：
  - 深空主题登录卡片（居中，OPC Logo，用户名/密码输入框）
  - 提交后调用 `/api/v1/auth/login`
  - 成功后将 Access Token 存入 Zustand，Refresh Token 存入 HttpOnly Cookie
  - 失败显示错误提示（密码错误、账户锁定等）
- ⬜ 创建 `client/src/stores/authStore.ts`：Zustand 认证状态（user、accessToken、isAuthenticated）
- ⬜ 创建 `client/src/hooks/useAuth.ts`：封装登录/登出/刷新 Token 逻辑
- ⬜ 创建 `client/src/lib/api.ts`：Axios 实例，配置 JWT 请求拦截器（自动携带 Token，过期前 5 分钟静默刷新）
- ⬜ 修改 `client/src/App.tsx`：添加路由守卫，未登录跳转 `/login`

### P2.3 文件系统读取服务（Week 1，Day 3-4）

#### 后端服务
- ⬜ 创建 `server/services/file_reader.py`：
  - `read_soul_md(agent_slug)` → 读取对应 SOUL.md 文件内容
  - `read_status_json()` → 读取 `status.json`，返回系统状态
  - `list_all_agents()` → 扫描 agents 目录，返回所有 SOUL.md 路径列表
  - `read_config_json()` → 读取 `.opc/config.json`
- ⬜ 创建 `server/services/soul_parser.py`：
  - `parse_soul_md(content)` → 解析 YAML Frontmatter（name、role、team、layer、tools 等字段）
  - `extract_soul_sections(content)` → 提取 SOUL.md 各章节（核心职责、工具权限、协作关系等）
- ⬜ 创建 `server/services/kairos_parser.py`：
  - `parse_kairos_log(file_path)` → 解析 JSONL 格式的 KAIROS 日志文件
  - `get_recent_entries(n=50)` → 获取最近 N 条日志条目
  - `get_entries_by_agent(agent_slug)` → 按 Agent 过滤日志
  - `get_entries_by_date_range(start, end)` → 按日期范围过滤
- ⬜ 创建 `server/services/finance_sync.py`：
  - `read_csv_records()` → 读取 `finance_tracker.csv`，返回结构化记录列表
  - `sync_csv_to_db()` → 将 CSV 记录同步到 `finance_records` 表（幂等操作）
  - `export_to_csv()` → 将数据库记录导出为 CSV 格式

### P2.4 Agent 管理 API（Week 1，Day 4-5）

- ⬜ 创建 `server/api/v1/agents.py`，实现以下端点：
  - `GET /api/v1/agents`：返回所有 Agent 列表（含状态、工负分数、最近活跃时间）
  - `GET /api/v1/agents/{slug}`：返回单个 Agent 详情（含 SOUL.md 内容、工具列表、统计数据）
  - `POST /api/v1/agents`：创建新 Agent（上传 SOUL.md，解析后入库）
  - `PUT /api/v1/agents/{slug}`：更新 Agent 配置（名称、状态、工具权限）
  - `POST /api/v1/agents/{slug}/sync-soul`：从文件系统重新读取 SOUL.md 并更新数据库
  - `GET /api/v1/agents/{slug}/stats`：返回 Agent 运行统计（Token 消耗、任务数、7 日趋势）
  - `GET /api/v1/agents/graph`：返回 A2A 协作关系图数据（节点 + 边，用于星系视图渲染）

### P2.5 仪表盘 API（Week 1，Day 5）

- ⬜ 创建 `server/api/v1/dashboard.py`，实现以下端点：
  - `GET /api/v1/dashboard/kpi`：返回 KPI 数据（今日任务数/完成率、本月收入、AI 成本、活跃 Agent 数）
  - `GET /api/v1/dashboard/projects`：返回活跃项目列表（含进度百分比、负责 Agent）
  - `GET /api/v1/dashboard/activity-feed`：返回最近 50 条活动记录（聚合 audit_logs + kairos_logs）

### P2.6 WebSocket 实时推送（Week 2，Day 1）

- ⬜ 创建 `server/api/v1/ws.py`：
  - `WS /ws/dashboard`：每 5 秒推送 Agent 状态快照（所有 Agent 的 status + workload_score）
  - `WS /ws/notifications`：推送系统通知（新审批请求、任务状态变更、硬停警报）
- ⬜ 创建 `server/services/notification.py`：WebSocket 连接管理器（维护连接池，广播消息）
- ⬜ 创建 `client/src/hooks/useWebSocket.ts`：前端 WebSocket 连接管理（自动重连，心跳检测）
- ⬜ 创建 `client/src/stores/agentStore.ts`：Zustand Agent 状态（实时更新，来自 WebSocket）
- ⬜ 创建 `client/src/stores/notificationStore.ts`：通知状态（待审批数量徽章）

### P2.7 前端真实数据替换（Week 2，Day 2-4）

#### 指挥大盘
- ⬜ 修改 `client/src/components/DashboardView.tsx`（或迁移到 `client/src/pages/dashboard/Dashboard.tsx`）：
  - 替换 KPI 卡片 mock 数据 → 调用 `GET /api/v1/dashboard/kpi`
  - 替换活跃项目 mock 数据 → 调用 `GET /api/v1/dashboard/projects`
  - 替换活动流 mock 数据 → 调用 `GET /api/v1/dashboard/activity-feed`
  - 接入 WebSocket → 实时更新 Agent 状态指示灯
  - 新增 `AlertBanner.tsx`：当有 `pending + critical` 审批时显示红色横幅

#### 活体图谱
- ⬜ 修改 `client/src/components/GalaxyView.tsx`（或迁移到 `client/src/pages/agents/AgentsPage.tsx`）：
  - 替换 Agent 节点 mock 数据 → 调用 `GET /api/v1/agents`
  - 替换协作关系 mock 数据 → 调用 `GET /api/v1/agents/graph`
  - 接入 WebSocket → Agent 节点发光强度实时变化
- ⬜ 创建 `client/src/components/agent/AgentDrawer.tsx`：
  - 点击 Agent 节点展开右侧抽屉
  - 显示 SOUL.md 全文（Markdown 渲染）
  - 显示工具列表（可启用/禁用）
  - 显示 7 日 Token 消耗趋势图（Recharts）
  - 显示最近 3 条任务
  - "直接对话"按钮（跳转 `/chat?agent={slug}`）

#### 时空追溯
- ⬜ 修改 `client/src/components/TimelineView.tsx`（或迁移到 `client/src/pages/memory/MemoryPage.tsx`）：
  - 替换时间线 mock 数据 → 调用 `GET /api/v1/timeline`
  - 实现筛选栏（Agent/项目/类型/日期范围）
  - 实现正反合透镜展开（点击条目展开三段式分析）

### P2.8 页面路由重构（Week 2，Day 4-5）

- ⬜ 重构 `client/src/App.tsx`：
  - 添加认证路由守卫（`ProtectedRoute` 组件）
  - 将所有视图从组件切换模式改为 Wouter 路由（`/dashboard`、`/agents`、`/memory` 等）
  - 添加登录路由 `/login`（无需认证）
- ⬜ 创建 `client/src/components/layout/AppLayout.tsx`：主布局（左导航 + 内容区 + 移动端底部导航）
- ⬜ 创建 `client/src/components/layout/MobileNav.tsx`：移动端底部 Tab 导航（仪表盘/对话/后台/通知/更多）
- ⬜ 创建 `client/src/components/shared/ThemeToggle.tsx`：暗色/亮色切换按钮（右上角）

### P2.9 Phase 2 验收标准 ⭐
- ⬜ 访问 `/login` 可正常登录（JWT 认证）
- ⬜ 仪表盘显示真实 KPI 数据（来自文件系统 + 数据库）
- ⬜ 活体图谱显示 22 个真实 Agent（来自 SOUL.md）
- ⬜ 时空追溯显示真实 KAIROS 日志
- ⬜ Agent 状态指示灯实时更新（WebSocket）
- ⬜ 移动端底部导航可用
- ⬜ 暗色/亮色主题切换正常

---

## Phase 3：任务管理中心（Week 3）⭐

**目标**：实现完整的任务发布、管理、执行监控闭环，以项目为主线串联所有任务。

### P3.1 项目管理 API

- ⬜ 创建 `server/api/v1/projects.py`，实现以下端点：
  - `GET /api/v1/projects`：项目列表（支持按阶段/状态/优先级筛选，分页）
  - `POST /api/v1/projects`：新建项目（标题/描述/客户/截止日期/预算/负责 Agent）
  - `GET /api/v1/projects/{id}`：项目详情（含关联任务列表、财务记录）
  - `PUT /api/v1/projects/{id}`：更新项目（状态机流转、基本信息）
  - `DELETE /api/v1/projects/{id}`：归档项目（软删除，`status=archived`）

### P3.2 任务管理 API

- ⬜ 创建 `server/api/v1/tasks.py`，实现以下端点：
  - `GET /api/v1/tasks`：任务列表（支持按状态/Agent/项目/优先级/日期范围多维筛选，分页）
  - `POST /api/v1/tasks`：新建任务（含 CEO 确认开关，默认开启）
  - `GET /api/v1/tasks/{id}`：任务详情（含 Plan 步骤、思考链、工具调用记录）
  - `PUT /api/v1/tasks/{id}`：更新任务（状态/指派/优先级/截止日期）
  - `DELETE /api/v1/tasks/{id}`：取消任务（软删除，`status=cancelled`）
  - `POST /api/v1/tasks/{id}/approve`：CEO 批准任务执行（`pending_ceo_approval` → `approved`）
  - `POST /api/v1/tasks/{id}/reject`：CEO 拒绝任务（→ `cancelled`，附带拒绝原因）
  - `POST /api/v1/tasks/{id}/stop`：停止执行中的任务（→ `cancelled`）
  - `GET /api/v1/tasks/{id}/thinking-log`：获取思考链日志（JSON Lines 解析后返回）
  - `SSE /api/v1/tasks/{id}/stream`：任务执行实时进度流（思考链 + 工具调用 + 状态变更）
  - `POST /api/v1/tasks/{id}/comments`：添加 CEO 评论/批注
  - `GET /api/v1/tasks/{id}/comments`：获取任务评论列表

### P3.3 Kanban 看板 UI

- ⬜ 创建 `client/src/pages/backstage/BackstagePage.tsx`：
  - 左侧项目列表侧边栏（按阶段分组：前期商务/规划设计/开发执行/交付运营/财务结算）
  - 中间 Kanban 看板（12 状态列，横向滚动）
  - 顶部工具栏（新建任务按钮、筛选器、视图切换：看板/列表）
- ⬜ 创建 `client/src/components/task/KanbanBoard.tsx`：
  - 基于 `@dnd-kit` 实现拖拽移动（改变任务状态）
  - 每列显示任务数量统计
  - 列标题颜色区分（待确认=橙色、执行中=蓝色、已完成=绿色、失败=红色）
- ⬜ 创建 `client/src/components/task/KanbanColumn.tsx`：
  - 可滚动的任务卡片列表
  - 拖拽目标区域高亮
- ⬜ 创建 `client/src/components/task/TaskCard.tsx`：
  - 任务标题 + 指派 Agent 头像 + 优先级标签 + 截止日期 + 进度条
  - 点击展开任务详情抽屉
  - 拖拽手柄
- ⬜ 创建 `client/src/hooks/useTasks.ts`：封装任务数据获取、状态更新、乐观更新逻辑

### P3.4 新建任务弹窗

- ⬜ 创建 `client/src/components/task/NewTaskModal.tsx`：
  - 任务标题（必填）
  - 任务描述（Markdown 编辑器，支持编辑/预览切换）
  - 关联项目（下拉选择，显示项目状态）
  - 指派 Agent（下拉，显示 Agent 当前工负分数）
  - 优先级（低/中/高/紧急，颜色区分）
  - 截止日期（日期选择器）
  - 执行前需 CEO 确认（开关，默认开启，附带说明文字）
  - 提交后调用 `POST /api/v1/tasks`

### P3.5 任务详情抽屉

- ⬜ 创建 `client/src/components/task/TaskDrawer.tsx`：
  - 任务基本信息（标题/描述/优先级/截止日期/状态）
  - 指派 Agent 选择器（下拉，可重新指派）
  - Plan 步骤列表（可勾选，显示完成进度，来自 `plan_steps` JSON）
  - 思考链日志（折叠展示，实时 SSE 流式更新）
  - 工具调用记录（展开/折叠，显示工具名/参数/结果）
  - 子任务列表（支持嵌套，可新建子任务）
  - 评论/备注区域（CEO 可添加批注）
  - 操作按钮：批准执行（绿色）/ 拒绝（红色）/ 暂停 / 重新指派
- ⬜ 创建 `client/src/components/task/ThinkingChain.tsx`：
  - 折叠/展开控制
  - 步骤类型图标（think/act/observe/plan/result 各有不同图标）
  - 工具调用详情（工具名 + 参数 JSON + 结果 JSON，代码块高亮）
  - SSE 实时追加新步骤（流式渲染）
- ⬜ 创建 `client/src/hooks/useSSE.ts`：封装 SSE 连接管理（自动重连，事件解析）

### P3.6 项目侧边栏

- ⬜ 创建 `client/src/components/task/ProjectSidebar.tsx`：
  - 项目列表按阶段分组（可折叠）
  - 每个项目显示：名称/状态/进度条/任务数
  - 点击项目过滤右侧 Kanban
  - "新建项目"按钮（展开新建项目抽屉）
- ⬜ 创建 `client/src/pages/backstage/ProjectDetail.tsx`：项目详情页（项目信息 + 关联任务 + 财务记录）

### P3.7 CEO 确认流程集成

- ⬜ 修改 `client/src/stores/notificationStore.ts`：添加待确认任务数量徽章
- ⬜ 修改 `client/src/components/layout/NavSidebar.tsx`：在"后台"菜单项显示待确认数量徽章
- ⬜ 修改 `client/src/components/dashboard/AlertBanner.tsx`：当有待确认任务时显示橙色提示横幅

### P3.8 Phase 3 验收标准 ⭐
- ⬜ 可新建项目（5 个阶段状态机）
- ⬜ 可新建任务（含 CEO 确认开关）
- ⬜ Kanban 看板显示 12 状态列，支持拖拽移动
- ⬜ CEO 可批准/拒绝待确认任务
- ⬜ 任务详情抽屉显示 Plan 步骤和思考链
- ⬜ 仪表盘顶部显示待确认任务数量徽章

---

## Phase 4：对话干预 + 审批流 + 智能体编排（Week 4）⭐

**目标**：实现 CEO 与 Agent 的直接对话，完整安全审批机制，以及可视化工作流编排画布。

### P4.1 LLM 多提供商路由服务

- ⬜ 创建 `server/services/llm_router.py`：
  - 基于 LiteLLM 封装统一调用接口
  - 从数据库读取 `llm_providers` 表，按 `priority` 排序
  - 实现 Failover 逻辑：首选提供商失败 → 自动切换到下一个（保持完整对话历史上下文）
  - 健康检查：定期 ping 每个提供商，更新 `health_status`
  - 支持 SSE 流式输出（`stream=True`）
  - 支持 Claude Thinking 模式（`thinking` 参数）
  - Token 消耗记录（写入 `token_usage` 表）

### P4.2 对话 API

- ⬜ 创建 `server/api/v1/chat.py`，实现以下端点：
  - `GET /api/v1/conversations`：会话列表（分页、搜索、按 Agent 筛选）
  - `POST /api/v1/conversations`：新建会话（指定 Agent、关联项目、初始 System Prompt）
  - `PUT /api/v1/conversations/{id}`：更新会话（标题、置顶、归档）
  - `DELETE /api/v1/conversations/{id}`：删除会话
  - `GET /api/v1/conversations/{id}/messages`：消息历史（分页，最新在底部）
  - `SSE /api/v1/conversations/{id}/chat`：流式对话（接收用户消息，返回 SSE 流）
    - 支持 `@Agent名称` 语法，自动注入对应 SOUL.md 为 System Prompt
    - 支持上下文文件挂载（从 `context_files` 字段读取，注入为 `<context>` 标签）
    - 支持工具调用流式展示（`tool_call` 事件类型）
    - 支持 Claude Thinking 流式展示（`thinking` 事件类型）
  - `POST /api/v1/conversations/{id}/context`：添加上下文文件（SOUL.md/brief.md/status.json 等）
  - `DELETE /api/v1/conversations/{id}/context/{file}`：移除上下文文件

### P4.3 对话 UI（ChatConsole）

- ⬜ 创建 `client/src/pages/chat/ChatConsole.tsx`：
  - 三栏布局：左侧会话列表（可折叠）+ 中间对话区 + 右侧 Agent 信息面板（可折叠）
  - 支持 URL 参数 `?agent={slug}` 预设 Agent
- ⬜ 创建 `client/src/components/chat/ConversationList.tsx`：
  - 会话列表（按最近消息时间排序）
  - 置顶会话置顶显示
  - 右键菜单（重命名/置顶/归档/删除）
  - "新建会话"按钮
- ⬜ 创建 `client/src/components/chat/MessageBubble.tsx`：
  - 用户消息（右对齐，深空蓝背景）
  - AI 消息（左对齐，深空灰背景）
  - Markdown 渲染（代码块高亮、表格、列表）
  - 思考链折叠展示（`<details>` 风格，点击展开）
  - 工具调用展示（工具名 + 参数 + 结果，可折叠）
  - 消息操作（复制、重新生成）
- ⬜ 创建 `client/src/components/chat/ChatInput.tsx`：
  - 多行输入框（Shift+Enter 换行，Enter 发送）
  - `@` 触发 Agent 选择器弹窗
  - 文件拖拽区域（拖入文件自动挂载为上下文）
  - 底部状态栏（当前使用的提供商/模型，Token 计数）
  - 发送按钮（发送中显示停止按钮）
- ⬜ 创建 `client/src/components/chat/AgentMention.tsx`：
  - 输入 `@` 后弹出 Agent 选择器
  - 显示 Agent 名称、团队、当前状态
  - 选择后自动注入 Agent slug
- ⬜ 创建 `client/src/components/chat/ContextFiles.tsx`：
  - 已挂载上下文文件列表（文件名 + 类型图标）
  - 点击文件名预览内容
  - 删除按钮（移除挂载）
  - "添加文件"按钮（从文件系统选择）
- ⬜ 创建 `client/src/components/chat/ToolCallDisplay.tsx`：
  - 工具调用卡片（工具名 + 状态图标：调用中/成功/失败）
  - 展开显示参数 JSON（代码高亮）
  - 展开显示结果 JSON（代码高亮）
- ⬜ 创建 `client/src/hooks/useConversation.ts`：封装对话逻辑（SSE 连接、消息追加、流式渲染）

### P4.4 安全审批 API

- ⬜ 创建 `server/api/v1/security.py`，实现以下端点：
  - `GET /api/v1/approvals`：审批列表（按状态筛选，`critical` 优先级置顶）
  - `GET /api/v1/approvals/{id}`：审批详情（含完整请求数据和上下文）
  - `POST /api/v1/approvals/{id}/approve`：批准（附带备注，通过 WebSocket 通知 Agent）
  - `POST /api/v1/approvals/{id}/reject`：拒绝（附带拒绝原因，通过 WebSocket 通知 Agent）
  - `GET /api/v1/security/rules`：安全规则列表
  - `POST /api/v1/security/rules`：新建安全规则
  - `PUT /api/v1/security/rules/{id}`：更新规则（含启用/禁用）
  - `DELETE /api/v1/security/rules/{id}`：删除规则
  - `GET /api/v1/audit-logs`：审计日志（支持按操作者/资源/时间范围筛选，分页）
- ⬜ 创建 `server/services/tool_guard.py`：
  - 加载所有启用的安全规则
  - `check_tool_call(tool_name, args)` → 返回 `allow/warn/block`
  - 触发 `block` 时自动创建审批请求（写入 `approvals` 表）
  - 触发 `warn` 时记录审计日志

### P4.5 安全审批 UI

- ⬜ 创建 `client/src/pages/security/SecurityPage.tsx`：
  - 三个 Tab：Tool Guard 规则 / 审批队列 / 审计日志
- ⬜ 创建 `client/src/components/security/ApprovalCard.tsx`：
  - 审批请求卡片（标题/请求方 Agent/类型/优先级/创建时间/过期时间）
  - 展开详情（完整请求数据 JSON，相关上下文）
  - 批准按钮（绿色）+ 拒绝按钮（红色）+ 备注输入框
  - `critical` 优先级显示红色边框和闪烁动效
- ⬜ 创建 `client/src/components/security/RuleTable.tsx`：安全规则表格（规则名/正则/严重级别/处置方式/启用开关）
- ⬜ 创建 `client/src/components/security/RuleModal.tsx`：新增/编辑规则弹窗

### P4.6 智能体编排（工作流画布）

- ⬜ 创建 `server/api/v1/orchestration.py`，实现以下端点：
  - `GET /api/v1/orchestration/workflows`：工作流列表（含最近执行状态）
  - `POST /api/v1/orchestration/workflows`：创建工作流（从模板或空白）
  - `GET /api/v1/orchestration/workflows/{id}`：工作流详情（含完整 `graph_json`）
  - `PUT /api/v1/orchestration/workflows/{id}`：保存工作流（更新 `graph_json`）
  - `DELETE /api/v1/orchestration/workflows/{id}`：删除工作流（软删除）
  - `POST /api/v1/orchestration/workflows/{id}/run`：手动触发执行
  - `PUT /api/v1/orchestration/workflows/{id}/toggle`：启用/禁用
  - `GET /api/v1/orchestration/workflows/{id}/runs`：执行历史列表
  - `GET /api/v1/orchestration/runs/{run_id}`：执行详情（含节点执行状态）
  - `SSE /api/v1/orchestration/runs/{run_id}/stream`：执行实时进度流
  - `GET /api/v1/orchestration/templates`：预置模板列表（4 个 OPC 工作流模板）
- ⬜ 创建 `server/services/workflow_engine.py`：
  - 解析 `graph_json`（ReactFlow 节点和边）为可执行的 LangGraph 状态图
  - 按节点类型分发执行（Agent 节点调用 LangGraph，条件节点评估表达式，审批节点暂停等待）
  - 执行日志写入 `workflow_runs.execution_log`（JSON Lines 格式）
  - 通过 SSE 推送实时进度
- ⬜ 创建 `client/src/pages/orchestration/OrchestrationPage.tsx`：
  - 左侧工作流列表（含状态/最近执行时间/运行次数）
  - 中间画布编辑区（ReactFlow）
  - 右侧节点配置面板（点击节点展开配置）
  - 顶部工具栏（保存/运行/启用/禁用/删除）
- ⬜ 创建 `client/src/components/orchestration/FlowCanvas.tsx`：
  - 基于 `@xyflow/react` 实现
  - 支持节点拖拽、连线、缩放、全屏
  - 深空主题（深色背景，电青连线）
  - 执行时节点高亮（当前执行节点发光）
- ⬜ 创建 `client/src/components/orchestration/AgentNode.tsx`：Agent 节点（头像 + 名称 + 任务描述预览）
- ⬜ 创建 `client/src/components/orchestration/ConditionNode.tsx`：条件节点（菱形，条件表达式）
- ⬜ 创建 `client/src/components/orchestration/TriggerNode.tsx`：触发器节点（闪电图标 + 触发类型）
- ⬜ 创建 `client/src/components/orchestration/FlowToolbar.tsx`：画布工具栏（节点类型面板，拖拽到画布添加）
- ⬜ 预置 4 个 OPC 工作流模板（写入数据库 seed 脚本）：
  - 新客户接入流程（Scout → CoS → CEO 审批 → Closer）
  - 项目启动流程（CoS 制定计划 → CEO 确认 → 并行执行）
  - 每日晨报流程（CoS 汇总 → 财务快照 → 推送）
  - 交付审核流程（Agent 自检 → CoS 审核 → CEO 确认 → Closer 交付）

### P4.7 Phase 4 验收标准 ⭐
- ⬜ 可与任意 Agent 对话（SSE 流式输出）
- ⬜ `@Agent名称` 自动注入 SOUL.md 为 System Prompt
- ⬜ LLM 提供商故障时自动切换（Failover 有效）
- ⬜ 审批队列可正常批准/拒绝
- ⬜ 工作流画布可创建节点和连线
- ⬜ 可手动触发工作流执行并查看实时进度

---

## Phase 5：设置中心 + 定时任务 + 模型管理（Week 5）

**目标**：实现完整的系统配置管理，包括 LLM 提供商管理、多模态配置、MCP 连接、定时任务调度。

### P5.1 设置模块布局

- ⬜ 创建 `client/src/pages/settings/SettingsLayout.tsx`：
  - 左侧二级导航（三个分组：模型配置/WORKSPACE/应用）
  - 右侧内容区（根据路由渲染对应子页面）
  - 支持移动端折叠（二级导航变为顶部 Tab）

### P5.2 模型管理（LLM 提供商）

- ⬜ 创建 `server/api/v1/settings/models.py`，实现以下端点：
  - `GET /api/v1/settings/llm-providers`：提供商列表（含健康状态）
  - `POST /api/v1/settings/llm-providers`：新增提供商（API Key AES 加密存储）
  - `PUT /api/v1/settings/llm-providers/{id}`：更新提供商（含优先级调整）
  - `DELETE /api/v1/settings/llm-providers/{id}`：删除提供商
  - `POST /api/v1/settings/llm-providers/{id}/test`：测试连通性（发送测试请求，返回延迟和状态）
  - `PUT /api/v1/settings/llm-providers/reorder`：拖拽排序（批量更新 priority）
- ⬜ 创建 `client/src/pages/settings/models/ModelsPage.tsx`：
  - 已配置提供商列表（表格：名称/类型/状态/优先级/操作）
  - 拖拽排序（调整 Failover 优先级）
  - 健康状态实时显示（绿色/黄色/红色指示灯）
- ⬜ 创建 `client/src/components/settings/ProviderCard.tsx`：提供商卡片（名称/状态/优先级/测试按钮）
- ⬜ 创建 `client/src/components/settings/ProviderModal.tsx`：
  - 新增/编辑提供商弹窗
  - 提供商类型选择（内置目录：OpenAI/Anthropic/Gemini/DashScope/Ollama 等）
  - Base URL 输入（自定义提供商）
  - API Key 输入（密码框，不显示明文）
  - 模型列表（JSON 数组，支持手动添加）
  - "测试连通性"按钮（实时验证）

### P5.3 多模态配置

- ⬜ 创建 `server/api/v1/settings/multimodal.py`：图片/TTS/STT/音乐/视频/3D 提供商配置 CRUD
- ⬜ 创建 `client/src/pages/settings/multimodal/ImageGenPage.tsx`：图片生成提供商配置
- ⬜ 创建 `client/src/pages/settings/multimodal/TTSPage.tsx`：语音合成提供商配置
- ⬜ 创建 `client/src/pages/settings/multimodal/STTPage.tsx`：语音识别提供商配置
- ⬜ 创建 `client/src/pages/settings/multimodal/MusicGenPage.tsx`：音乐生成配置
- ⬜ 创建 `client/src/pages/settings/multimodal/VideoGenPage.tsx`：视频生成配置
- ⬜ 创建 `client/src/pages/settings/multimodal/ThreeDGenPage.tsx`：3D 生成配置

### P5.4 Agent 上下文编辑器

- ⬜ 创建 `server/api/v1/settings/workspace.py`，实现以下端点：
  - `GET /api/v1/settings/agent-context/{slug}`：获取 Agent 上下文文件列表（SOUL.md/MEMORY.md/AGENTS.md 等）
  - `GET /api/v1/settings/agent-context/{slug}/{file}`：获取文件内容
  - `PUT /api/v1/settings/agent-context/{slug}/{file}`：保存文件内容（写入文件系统 + 更新数据库缓存）
  - `POST /api/v1/settings/agent-context/{slug}/{file}`：新建文件
  - `DELETE /api/v1/settings/agent-context/{slug}/{file}`：删除文件
- ⬜ 创建 `client/src/pages/settings/workspace/AgentContextPage.tsx`：
  - Agent 选择下拉（显示所有 22 个 Agent）
  - 上下文文件列表（可启用/禁用）
  - Markdown 编辑器（编辑/预览/分屏三模式）
  - 保存/重置/删除按钮
- ⬜ 创建 `client/src/components/shared/MarkdownEditor.tsx`：
  - 编辑/预览/分屏三模式切换
  - 工具栏（加粗/斜体/代码/链接/图片等）
  - 实时预览（Markdown 渲染）
  - 自动保存（防抖 2 秒）

### P5.5 MCP 连接管理

- ⬜ 创建 `server/api/v1/settings/mcp.py`，实现以下端点：
  - `GET /api/v1/settings/mcp`：MCP 连接列表（含状态）
  - `POST /api/v1/settings/mcp`：新增 MCP 连接（stdio/SSE/HTTP 三种协议）
  - `PUT /api/v1/settings/mcp/{id}`：更新连接配置
  - `DELETE /api/v1/settings/mcp/{id}`：删除连接
  - `POST /api/v1/settings/mcp/{id}/test`：测试连接（发现可用工具列表）
  - `GET /api/v1/settings/mcp/{id}/tools`：获取已发现的工具列表
- ⬜ 创建 `client/src/pages/settings/apps/McpPage.tsx`：MCP 连接管理页面
- ⬜ 创建 `client/src/components/settings/McpModal.tsx`：新增/编辑 MCP 连接弹窗（协议选择/命令/参数/环境变量/超时配置）

### P5.6 定时任务管理

- ⬜ 创建 `server/services/cron_scheduler.py`：
  - 基于 APScheduler `AsyncIOScheduler` 实现
  - 应用启动时从数据库加载所有启用的 Cron 任务
  - 执行时创建 Task 记录，调用 Agent 执行引擎
  - 执行结果写入 `cron_run_history` 表
  - 支持动态增删改（无需重启）
- ⬜ 创建 `server/api/v1/settings/cron.py`，实现以下端点：
  - `GET /api/v1/cron-jobs`：定时任务列表（含下次执行时间）
  - `POST /api/v1/cron-jobs`：新建定时任务（含 Cron 表达式可视化解释）
  - `PUT /api/v1/cron-jobs/{id}`：更新任务
  - `DELETE /api/v1/cron-jobs/{id}`：删除任务
  - `POST /api/v1/cron-jobs/{id}/run`：立即执行一次
  - `PUT /api/v1/cron-jobs/{id}/toggle`：启用/禁用
  - `GET /api/v1/cron-jobs/{id}/history`：执行历史（最近 50 次）
- ⬜ 创建 `client/src/pages/settings/apps/CronJobsPage.tsx`：定时任务管理页面（表格 + 新建/编辑弹窗 + 执行历史抽屉）
- ⬜ 预置 4 个 OPC 定时任务（写入数据库 seed 脚本）：
  - 每日晨报（周一至周五 9:00，CoS 执行）
  - 每周复盘（周五 17:00，CoS 执行）
  - 财务月报（每月 1 日 10:00，Finance Agent 执行）
  - 客户跟进提醒（每日 10:00，Scout 执行）

### P5.7 Token 统计

- ⬜ 创建 `server/api/v1/settings/token_usage.py`：
  - `GET /api/v1/settings/token-usage`：Token 消耗统计（按 Agent/模型/日期多维聚合，支持自定义时间范围）
  - `GET /api/v1/settings/token-usage/summary`：汇总数据（总消耗/估算成本/最活跃 Agent）
- ⬜ 创建 `client/src/pages/settings/apps/TokenUsagePage.tsx`：
  - 时间范围选择器（今日/本周/本月/自定义）
  - 按 Agent 分组的 Token 消耗柱状图
  - 按模型分组的消耗饼图
  - 估算 USD 成本（基于各提供商定价）
  - 详细记录表格（可导出 CSV）
- ⬜ 创建 `client/src/components/settings/TokenChart.tsx`：Token 消耗图表组件

### P5.8 其他设置子页面

- ⬜ 创建 `client/src/pages/settings/workspace/WorkspacePage.tsx`：工作区基本信息 + 四大团队配置
- ⬜ 创建 `client/src/pages/settings/workspace/MembersPage.tsx`：成员管理（用户邀请/角色分配）
- ⬜ 创建 `client/src/pages/settings/workspace/AdvancedPage.tsx`：高级选项（数据清理/导入导出/危险操作）
- ⬜ 创建 `client/src/pages/settings/apps/ToolsPage.tsx`：工具目录（内置工具启用/禁用）
- ⬜ 创建 `client/src/pages/settings/apps/DatasourcesPage.tsx`：数据源连接配置
- ⬜ 创建 `client/src/pages/settings/apps/AcpPage.tsx`：ACP 端点配置
- ⬜ 创建 `client/src/pages/settings/apps/FeatureFlagsPage.tsx`：功能开关列表
- ⬜ 创建 `client/src/pages/settings/apps/AboutPage.tsx`：版本信息 + 更新日志
- ⬜ 创建 `server/api/v1/settings/system.py`：系统配置 CRUD（语言/时区/通知等键值对）
- ⬜ 创建 `client/src/pages/settings/apps/SystemPage.tsx`：系统设置页面

### P5.9 Phase 5 验收标准
- ⬜ 可在 UI 中添加/删除 LLM 提供商（API Key 加密存储）
- ⬜ 可测试 LLM 提供商连通性
- ⬜ 可拖拽调整 Failover 优先级
- ⬜ 可编辑 Agent 的 SOUL.md 文件（写入文件系统）
- ⬜ 可添加/测试 MCP 连接
- ⬜ 定时任务可新建/启用/立即执行
- ⬜ Token 统计图表正常显示

---

## Phase 6：财务大盘 + Wiki + 渠道 + 移动端 + Docker 部署（Week 6）⭐

**目标**：完成所有功能模块，优化移动端体验，完成完整闭环，实现公网可访问的 Docker 部署。

### P6.1 财务运营大盘

- ⬜ 创建 `server/api/v1/finance.py`，实现以下端点：
  - `GET /api/v1/finance/kpi`：财务 KPI（MRR/ARR/本月收入/本月成本/AI 成本占比）
  - `GET /api/v1/finance/records`：财务记录列表（按日期范围/类型/分类筛选，分页）
  - `POST /api/v1/finance/records`：新建财务记录
  - `PUT /api/v1/finance/records/{id}`：更新财务记录
  - `DELETE /api/v1/finance/records/{id}`：软删除
  - `GET /api/v1/finance/export`：导出 CSV（支持日期范围过滤）
  - `POST /api/v1/finance/import`：从 CSV 导入（`finance_tracker.csv` 同步）
  - `GET /api/v1/finance/charts/monthly`：月度收入/成本趋势数据（12 个月）
  - `GET /api/v1/finance/charts/cost-breakdown`：成本构成数据（LLM/工具/其他）
  - `GET /api/v1/finance/charts/funnel`：转化漏斗数据（线索→商机→成交）
- ⬜ 修改 `client/src/pages/finance/FinancePage.tsx`（替换 mock 数据）：
  - 顶部 KPI 卡片（MRR/ARR/本月收入/本月成本/AI 成本占比）
  - 月度趋势折线图（12 个月，收入/成本双线）
  - 成本构成饼图（LLM API/工具订阅/其他）
  - 转化漏斗（线索→商机→成交，转化率显示）
  - 项目收入排行榜（Top 5）
  - 财务记录表格（分页，支持筛选和导出）
  - "新建记录"按钮 + 弹窗
- ⬜ 创建 `client/src/components/finance/RevenueChart.tsx`：月度营收趋势图
- ⬜ 创建 `client/src/components/finance/CostPieChart.tsx`：成本构成饼图
- ⬜ 创建 `client/src/components/finance/FunnelChart.tsx`：转化漏斗图
- ⬜ 创建 `client/src/components/finance/FinanceTable.tsx`：财务记录表格（含新建/编辑/删除）

### P6.2 Wiki 知识库

- ⬜ 创建 `server/api/v1/wiki.py`，实现以下端点：
  - `GET /api/v1/wiki/docs`：文档树（嵌套结构，含文件夹）
  - `POST /api/v1/wiki/docs`：新建文档/文件夹
  - `GET /api/v1/wiki/docs/{id}`：文档详情（含 Markdown 内容）
  - `PUT /api/v1/wiki/docs/{id}`：更新文档（自动版本快照）
  - `DELETE /api/v1/wiki/docs/{id}`：软删除（保留 30 天）
  - `GET /api/v1/wiki/search`：全文搜索（标题 + 内容）
- ⬜ 创建 `client/src/pages/wiki/WikiPage.tsx`：
  - 左侧文件树（支持文件夹嵌套，拖拽排序）
  - 右侧 Markdown 编辑器（复用 `MarkdownEditor.tsx`）
  - 顶部面包屑导航
  - 搜索框（全文搜索）
- ⬜ 创建 `client/src/components/shared/FileTree.tsx`：可折叠文件树组件（支持文件/文件夹图标，右键菜单）

### P6.3 渠道管理

- ⬜ 创建 `server/api/v1/channels.py`：IM 渠道 CRUD + 连通性测试
- ⬜ 创建 `client/src/pages/channels/ChannelsPage.tsx`：
  - 渠道类型选择（微信/钉钉/飞书/企业微信/QQ/Telegram/Discord/Slack）
  - 渠道配置表单（Webhook URL/API Token/AppID 等，按类型动态渲染）
  - 连通性测试按钮
  - 绑定 Agent 选择器
  - 消息过滤规则配置

### P6.4 技能管理

- ⬜ 创建 `server/api/v1/skills.py`：技能 CRUD + Agent 分配
- ⬜ 创建 `client/src/pages/skills/SkillsPage.tsx`：
  - 技能矩阵卡片视图（按类别分组）
  - 上传 SKILL.md 文件创建技能
  - 分配给 Agent（多选）
  - 使用统计（被哪些 Agent 使用，调用次数）

### P6.5 插件管理

- ⬜ 创建 `server/api/v1/plugins.py`：插件 CRUD
- ⬜ 创建 `client/src/pages/plugins/PluginsPage.tsx`：
  - 已安装插件列表（名称/版本/状态/授权 Agent）
  - 插件市场入口（占位，Phase 7 实现）
  - 手动上传安装（ZIP 包）

### P6.6 活动记录

- ⬜ 创建 `server/api/v1/activity.py`：审计日志查询（多维筛选，分页）
- ⬜ 创建 `client/src/pages/activity/ActivityPage.tsx`：
  - 操作历史时间线（按时间倒序）
  - 筛选栏（操作者/资源类型/操作类型/时间范围）
  - 每条记录显示：时间/操作者/操作内容/资源/前后状态 diff
  - 导出 CSV 按钮

### P6.7 移动端全面优化

- ⬜ 修改 `client/src/components/layout/MobileNav.tsx`：底部 5 个 Tab（仪表盘/对话/后台/通知/更多）
- ⬜ 修改 `client/src/pages/dashboard/Dashboard.tsx`：移动端单列滚动，KPI 卡片 2×2 网格
- ⬜ 修改 `client/src/pages/agents/AgentsPage.tsx`：移动端切换为列表视图（隐藏星系视图）
- ⬜ 修改 `client/src/pages/backstage/BackstagePage.tsx`：移动端单列列表，状态标签筛选（隐藏 Kanban）
- ⬜ 修改 `client/src/pages/chat/ChatConsole.tsx`：移动端全屏对话，底部输入框，隐藏侧边栏
- ⬜ 修改 `client/src/pages/security/SecurityPage.tsx`：移动端卡片列表，滑动操作（批准/拒绝）
- ⬜ 全局响应式断点检查：确保所有页面在 375px 宽度下可用
- ⬜ 移动端触摸优化：增大点击目标（最小 44×44px），禁用悬停效果

### P6.8 ⌘K 命令面板完整实现

- ⬜ 修改 `client/src/components/shared/CommandPalette.tsx`，接入真实数据：
  - 导航命令：`go {page}` → 跳转对应路由
  - Agent 对话：`chat {agent}` → 打开对话（动态加载 Agent 列表）
  - 任务操作：`new task` → 打开新建任务弹窗
  - 审批操作：`approve {id}` → 直接批准审批请求（调用 API）
  - 项目跳转：`project {id}` → 跳转项目详情
  - 工作流触发：`run workflow {name}` → 触发指定工作流
  - 全局搜索：`search {keyword}` → 搜索任务/文档/对话
  - 配置跳转：`settings {page}` → 跳转设置子页面

### P6.9 性能优化

- ⬜ 前端虚拟列表：对任务列表、消息列表、日志列表使用 `react-virtual`（超过 100 条时启用）
- ⬜ 懒加载：路由级别代码分割（`React.lazy` + `Suspense`）
- ⬜ 图片懒加载：Agent 头像、Wiki 图片
- ⬜ API 缓存：使用 `stale-while-revalidate` 策略（SWR 或 React Query 可选）
- ⬜ 后端分页：所有列表接口确保支持 `page`/`page_size` 参数

### P6.10 Docker 部署配置

- ⬜ 创建 `Dockerfile.client`：多阶段构建（Node.js 构建 + Nginx 静态文件服务）
- ⬜ 创建 `Dockerfile.server`：Python 3.11 + FastAPI + Uvicorn
- ⬜ 创建 `docker-compose.yml`（生产环境）：
  - `frontend`：Nginx 服务静态文件
  - `backend`：FastAPI + Uvicorn（4 workers）
  - `db`：PostgreSQL 16（数据持久化 volume）
  - `nginx`：反向代理（HTTPS 终止 + WebSocket 代理 + 静态文件服务）
- ⬜ 创建 `docker-compose.dev.yml`（开发环境）：热重载，挂载本地代码
- ⬜ 创建 `nginx.conf`：
  - HTTPS 配置（SSL 证书路径）
  - WebSocket 代理（`/ws/` 路径）
  - SSE 代理（`/api/v1/*/stream` 路径，禁用缓冲）
  - 静态文件服务（前端 build 产物）
  - API 反向代理（`/api/` → `backend:8000`）
- ⬜ 创建部署文档 `DEPLOY.md`：一键部署步骤、环境变量配置说明、SSL 证书配置

### P6.11 Phase 6 验收标准 ⭐
- ⬜ 财务大盘显示真实数据（来自 `finance_tracker.csv` + 数据库）
- ⬜ Wiki 可新建/编辑/搜索文档
- ⬜ 渠道可配置并测试连通性
- ⬜ 移动端（375px）所有核心功能可用
- ⬜ ⌘K 命令面板接入真实数据
- ⬜ `docker-compose up` 一键启动完整系统
- ⬜ 公网可通过 HTTPS 访问

---

## Phase 7：扩展功能（按需实现）

**目标**：在核心功能稳定后，逐步扩展多模态能力、渠道集成和技能市场。

### P7.1 多模态能力集成

- ⬜ 图片生成：在对话界面支持 `/image {prompt}` 命令，调用 DALL-E/Stable Diffusion API
- ⬜ 语音合成（TTS）：消息气泡添加"朗读"按钮，调用 TTS API 播放
- ⬜ 语音识别（STT）：对话输入框添加麦克风按钮，录音后转文字
- ⬜ 音乐生成：在工作流节点中支持音乐生成工具节点
- ⬜ 视频生成：在工作流节点中支持视频生成工具节点

### P7.2 IM 渠道实际集成

- ⬜ 微信公众号 Webhook 接收消息，路由给绑定 Agent 处理
- ⬜ 钉钉机器人 Webhook 集成
- ⬜ Telegram Bot API 集成（轮询或 Webhook）
- ⬜ Discord Bot 集成
- ⬜ 创建 `server/services/channel_router.py`：统一消息路由（接收 → 解析 → 调用 Agent → 回复）

### P7.3 技能市场

- ⬜ 技能市场 UI（浏览/搜索/安装）
- ⬜ 技能版本管理（SKILL.md 版本控制）
- ⬜ 技能评分和使用统计

### P7.4 记忆系统增强

- ⬜ 集成 ChromaDB（本地向量数据库）
- ⬜ KAIROS 日志自动向量化（入库时生成 embedding）
- ⬜ 语义搜索：在时空追溯页面支持自然语言搜索（"找出所有关于客户 A 的决策"）
- ⬜ 长期记忆触发：对话超过上下文窗口时，自动检索相关记忆注入

### P7.5 高级编排功能

- ⬜ 工作流版本控制（保存历史版本，支持回滚）
- ⬜ 工作流调试模式（单步执行，断点暂停）
- ⬜ 工作流市场（分享和导入社区工作流模板）
- ⬜ 事件触发器（基于系统事件自动触发工作流，如"新任务创建时"）

---

## 附录：关键文件索引

### 后端核心文件（Phase 2 必须创建）

| 文件路径 | 功能 |
|---|---|
| `server/main.py` | FastAPI 入口 |
| `server/core/config.py` | 环境变量配置 |
| `server/core/database.py` | 数据库连接 |
| `server/core/security.py` | JWT 工具函数 |
| `server/core/dependencies.py` | 依赖注入 |
| `server/services/file_reader.py` | 文件系统读取 |
| `server/services/soul_parser.py` | SOUL.md 解析 |
| `server/services/kairos_parser.py` | KAIROS 日志解析 |
| `server/api/v1/auth.py` | 认证 API |
| `server/api/v1/agents.py` | Agent 管理 API |
| `server/api/v1/dashboard.py` | 仪表盘 API |
| `server/api/v1/ws.py` | WebSocket 端点 |
| `server/migrations/versions/001_initial_schema.py` | 22 张表建表迁移 |

### 前端核心文件（Phase 2 必须创建/修改）

| 文件路径 | 功能 |
|---|---|
| `client/src/lib/api.ts` | Axios 实例 + JWT 拦截器 |
| `client/src/stores/authStore.ts` | 认证状态 |
| `client/src/stores/agentStore.ts` | Agent 实时状态 |
| `client/src/hooks/useAuth.ts` | 认证逻辑 |
| `client/src/hooks/useWebSocket.ts` | WebSocket 管理 |
| `client/src/pages/auth/Login.tsx` | 登录页 |
| `client/src/components/layout/AppLayout.tsx` | 主布局 |
| `client/src/components/layout/MobileNav.tsx` | 移动端导航 |
| `client/src/components/agent/AgentDrawer.tsx` | SOUL 透视镜 |

---

*文档版本：v1.0 | 生成时间：2026-05-05 | 基于 OPC_Final_Development_Plan_v6.md*
*v4+v5 融合确认：✅ 完整融合（API 端点、增删改查细节、导航体系、设置模块、多模态配置均已包含）*
