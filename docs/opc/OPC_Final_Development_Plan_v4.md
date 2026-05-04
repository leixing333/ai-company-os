# OPC 智能体操作平台 — 完整开发规划 v4

> **文档性质**：本文档为路径C（完全自主开发）的最终执行蓝图，整合了 MateClaw 28页 UI 截图分析、15个页面源码功能提取、OPC 现有系统架构，以及用户补充的5项核心需求。确认后可直接指导开发。

---

## 一、战略定位与核心原则

OPC 智能体操作平台（以下简称"OPC 工作台"）是一人公司的数字神经中枢，其核心定位是**CEO 专属指挥舱**，而非通用 AI 助手。与 MateClaw 的最大差异在于：OPC 工作台深度融合了 SOUL.md 人格体系、KAIROS 决策日志、四大团队组织架构和 Escalation 审批机制，是 OPC 业务语义的完整可视化。

**五项核心设计原则**如下：

| 原则 | 说明 |
|---|---|
| 原样可视化 | 读取已有文件系统（SOUL.md、status.json、kairos_logs），不重建数据 |
| 深空主题延续 | 沿用 Phase 1 的深空操控台风格，支持暗色/亮色双模式切换 |
| 移动端优先响应式 | 所有页面在手机端可用，关键操作（审批、查看）在移动端完整支持 |
| LLM 多提供商容错 | 支持多个 LLM 提供商配置，按优先级排序，失败自动切换并保持上下文 |
| 公网部署就绪 | WebSocket/SSE 配置适配公网，JWT 认证，HTTPS 支持 |

---

## 二、技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    OPC 工作台                            │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  React 19   │    │  FastAPI    │    │  SQLite/    │  │
│  │  前端        │◄──►│  后端        │◄──►│  PostgreSQL │  │
│  │  TypeScript │    │  Python     │    │  数据库      │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                  │                            │
│         │                  ▼                            │
│         │         ┌─────────────────┐                   │
│         │         │  文件系统读取     │                   │
│         │         │  ai-company-os/ │                   │
│         │         │  SOUL.md        │                   │
│         │         │  status.json    │                   │
│         │         │  kairos_logs/   │                   │
│         │         └─────────────────┘                   │
│         │                  │                            │
│         ▼                  ▼                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              LLM 多提供商路由层                       │ │
│  │  Claude → GPT-4o → Gemini → 本地模型（按优先级）     │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选型

| 层级 | 技术选型 | 选型理由 |
|---|---|---|
| 前端框架 | React 19 + TypeScript | 已有 Phase 1 基础，生态成熟 |
| 前端路由 | Wouter | 轻量，已集成 |
| UI 组件库 | shadcn/ui + Radix UI | 已集成，可高度定制 |
| 样式系统 | Tailwind CSS 4 | 已集成，主题变量完整 |
| 图表库 | Recharts | 已集成，支持响应式 |
| 动画库 | Framer Motion | 已集成，星系视图动效 |
| 状态管理 | Zustand | 轻量，适合中等复杂度 |
| 实时通信 | WebSocket + SSE | 任务进度推送、日志流式输出 |
| 后端框架 | FastAPI (Python 3.11) | 与 kairos_daemon.py 同语言，异步支持好 |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） | 轻量启动，可平滑迁移 |
| ORM | SQLAlchemy 2.0 + Alembic | 类型安全，迁移管理 |
| 认证 | JWT（python-jose）+ bcrypt | 标准方案，支持滑动续签 |
| LLM 编排 | LangChain + LiteLLM | 多提供商统一接口，自动故障转移 |
| 任务队列 | APScheduler | Cron 任务管理，与现有 kairos_daemon 兼容 |
| 部署 | Docker Compose | 前后端一键启动，公网就绪 |

### 2.3 项目目录结构

```
opc-dashboard/
├── client/                          # React 前端
│   └── src/
│       ├── pages/                   # 页面组件（对应路由）
│       │   ├── Dashboard.tsx        # 指挥大盘
│       │   ├── Agents.tsx           # 活体图谱
│       │   ├── Backstage.tsx        # 任务管理中心
│       │   ├── ChatConsole.tsx      # CEO 对话干预
│       │   ├── Timeline.tsx         # 时空追溯
│       │   ├── Finance.tsx          # 财务运营大盘
│       │   ├── Security.tsx         # 安全审批中心
│       │   ├── Settings/            # 配置中心（多子页）
│       │   └── Wiki.tsx             # 知识资产管理
│       ├── components/              # 复用组件
│       │   ├── layout/              # 布局组件
│       │   ├── agent/               # Agent 相关组件
│       │   ├── task/                # 任务相关组件
│       │   ├── chat/                # 对话相关组件
│       │   └── CommandPalette.tsx   # ⌘K 命令面板
│       ├── hooks/                   # 自定义 Hook
│       ├── stores/                  # Zustand 状态
│       └── lib/                     # 工具函数
├── server/                          # FastAPI 后端
│   ├── main.py                      # 入口
│   ├── api/                         # API 路由
│   │   ├── auth.py                  # 认证
│   │   ├── agents.py                # Agent 管理
│   │   ├── tasks.py                 # 任务管理
│   │   ├── chat.py                  # 对话（SSE 流式）
│   │   ├── timeline.py              # KAIROS 日志
│   │   ├── finance.py               # 财务数据
│   │   ├── security.py              # 安全审批
│   │   ├── settings.py              # 配置管理
│   │   └── cron.py                  # 定时任务
│   ├── models/                      # SQLAlchemy 模型
│   ├── schemas/                     # Pydantic 模式
│   ├── services/                    # 业务逻辑层
│   │   ├── llm_router.py            # LLM 多提供商路由
│   │   ├── file_reader.py           # 文件系统读取
│   │   └── kairos_parser.py         # KAIROS 日志解析
│   └── core/                        # 核心配置
│       ├── config.py
│       ├── database.py
│       └── security.py
└── docker-compose.yml               # 一键部署
```

---

## 三、数据库设计

### 3.1 核心表结构

#### 用户与认证

```sql
-- 用户表（仅 CEO 一人，但保留多用户扩展能力）
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    email       TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    role        TEXT DEFAULT 'ceo',  -- ceo | observer
    is_active   BOOLEAN DEFAULT TRUE,
    last_login  DATETIME,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- JWT 刷新令牌表（支持滑动续签）
CREATE TABLE refresh_tokens (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER REFERENCES users(id),
    token_hash  TEXT UNIQUE NOT NULL,
    expires_at  DATETIME NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    revoked     BOOLEAN DEFAULT FALSE
);
```

#### Agent 管理

```sql
-- Agent 主表（与文件系统 SOUL.md 双向同步）
CREATE TABLE agents (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT UNIQUE NOT NULL,  -- 如 cos, scout, closer
    name            TEXT NOT NULL,         -- 如 CoS 首席参谋长
    team            TEXT NOT NULL,         -- company | marketing | product | operations
    layer           TEXT NOT NULL,         -- company | strategy | execution
    role_title      TEXT,                  -- 角色头衔
    soul_md_path    TEXT,                  -- SOUL.md 文件路径
    soul_md_content TEXT,                  -- SOUL.md 缓存内容（定期同步）
    soul_md_hash    TEXT,                  -- 内容哈希，用于检测变更
    status          TEXT DEFAULT 'idle',   -- idle | active | busy | error | offline
    is_enabled      BOOLEAN DEFAULT TRUE,
    workload_score  REAL DEFAULT 0.0,      -- 0.0-1.0，用于星系视图发光强度
    last_active_at  DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Agent 工具权限表
CREATE TABLE agent_tools (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id    INTEGER REFERENCES agents(id),
    tool_name   TEXT NOT NULL,
    is_enabled  BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Agent 运行统计表（Token 消耗、API 调用）
CREATE TABLE agent_stats (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id        INTEGER REFERENCES agents(id),
    date            DATE NOT NULL,
    token_input     INTEGER DEFAULT 0,
    token_output    INTEGER DEFAULT 0,
    api_calls       INTEGER DEFAULT 0,
    tasks_completed INTEGER DEFAULT 0,
    avg_response_ms REAL DEFAULT 0.0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, date)
);
```

#### 任务管理

```sql
-- 项目表（对应 active_projects/ 目录）
CREATE TABLE projects (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      TEXT UNIQUE NOT NULL,  -- 如 P-001
    name            TEXT NOT NULL,
    description     TEXT,
    client          TEXT,
    status          TEXT DEFAULT 'briefing',
    -- 状态机：briefing | planning | in_progress | review | approved | delivered | archived | cancelled
    priority        TEXT DEFAULT 'medium', -- low | medium | high | urgent
    brief_md_path   TEXT,                  -- brief.md 文件路径
    status_json_path TEXT,                 -- status.json 文件路径
    assigned_agents TEXT,                  -- JSON 数组，指派的 Agent slug 列表
    deadline        DATE,
    budget          REAL,
    revenue         REAL,
    tags            TEXT,                  -- JSON 数组
    created_by      INTEGER REFERENCES users(id),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务表（项目下的具体任务）
CREATE TABLE tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER REFERENCES projects(id),
    task_id         TEXT UNIQUE NOT NULL,  -- 如 T-001-01
    title           TEXT NOT NULL,
    description     TEXT,
    status          TEXT DEFAULT 'pending',
    -- 状态：pending | assigned | in_progress | review | done | cancelled
    priority        TEXT DEFAULT 'medium',
    assigned_agent  TEXT,                  -- Agent slug
    parent_task_id  INTEGER REFERENCES tasks(id),  -- 子任务支持
    plan_steps      TEXT,                  -- JSON 数组，Plan-and-Execute 步骤
    thinking_log    TEXT,                  -- 思考链日志（JSON Lines）
    tool_calls      TEXT,                  -- 工具调用记录（JSON）
    result          TEXT,                  -- 执行结果摘要
    started_at      DATETIME,
    completed_at    DATETIME,
    created_by      INTEGER REFERENCES users(id),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务评论/备注表
CREATE TABLE task_comments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id     INTEGER REFERENCES tasks(id),
    author      TEXT NOT NULL,  -- 'ceo' 或 Agent slug
    content     TEXT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 对话系统

```sql
-- 对话会话表
CREATE TABLE conversations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT,
    agent_slug      TEXT,                  -- 绑定的 Agent
    project_id      INTEGER REFERENCES projects(id),  -- 可选关联项目
    context_files   TEXT,                  -- JSON 数组，挂载的上下文文件路径
    llm_provider    TEXT,                  -- 使用的 LLM 提供商
    llm_model       TEXT,                  -- 使用的具体模型
    total_tokens    INTEGER DEFAULT 0,
    is_archived     BOOLEAN DEFAULT FALSE,
    created_by      INTEGER REFERENCES users(id),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 消息表
CREATE TABLE messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER REFERENCES conversations(id),
    role            TEXT NOT NULL,         -- user | assistant | system | tool
    content         TEXT NOT NULL,
    thinking        TEXT,                  -- 思考链内容（Claude Thinking 模式）
    tool_calls      TEXT,                  -- JSON，工具调用
    tool_results    TEXT,                  -- JSON，工具结果
    token_count     INTEGER DEFAULT 0,
    llm_provider    TEXT,
    llm_model       TEXT,
    response_ms     INTEGER,               -- 响应时间（毫秒）
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 安全与审批

```sql
-- 审批请求表（Escalation）
CREATE TABLE approvals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    approval_id     TEXT UNIQUE NOT NULL,  -- 如 APR-001
    type            TEXT NOT NULL,         -- tool_guard | task_start | budget | external_action
    title           TEXT NOT NULL,
    description     TEXT,
    requested_by    TEXT NOT NULL,         -- Agent slug
    project_id      INTEGER REFERENCES projects(id),
    task_id         INTEGER REFERENCES tasks(id),
    payload         TEXT,                  -- JSON，审批相关数据
    status          TEXT DEFAULT 'pending', -- pending | approved | rejected | expired
    priority        TEXT DEFAULT 'medium', -- low | medium | high | critical
    expires_at      DATETIME,
    reviewed_by     INTEGER REFERENCES users(id),
    review_note     TEXT,
    reviewed_at     DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 安全规则表（Tool Guard）
CREATE TABLE security_rules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id         TEXT UNIQUE NOT NULL,  -- 如 RULE_001
    name            TEXT NOT NULL,
    pattern         TEXT NOT NULL,         -- 正则表达式
    severity        TEXT DEFAULT 'medium', -- low | medium | high | critical
    category        TEXT,                  -- COMMAND_INJECTION | FILE_SYSTEM | NETWORK 等
    action          TEXT DEFAULT 'needs_approval', -- block | needs_approval | log_only
    target_tools    TEXT,                  -- JSON 数组，目标工具列表
    is_enabled      BOOLEAN DEFAULT TRUE,
    priority        INTEGER DEFAULT 100,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 审计日志表
CREATE TABLE audit_logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type  TEXT NOT NULL,  -- login | logout | task_create | approval | config_change 等
    actor       TEXT NOT NULL,  -- 'ceo' 或 Agent slug
    target      TEXT,           -- 操作对象描述
    payload     TEXT,           -- JSON，详细数据
    ip_address  TEXT,
    user_agent  TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### LLM 配置

```sql
-- LLM 提供商配置表
CREATE TABLE llm_providers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id TEXT UNIQUE NOT NULL,  -- 如 anthropic-claude, openai-gpt4
    name        TEXT NOT NULL,
    base_url    TEXT,
    api_key_encrypted TEXT NOT NULL,   -- AES 加密存储
    protocol    TEXT DEFAULT 'openai', -- openai | anthropic | gemini | ollama
    models      TEXT,                  -- JSON 数组，支持的模型列表
    priority    INTEGER DEFAULT 100,   -- 数字越小优先级越高
    is_enabled  BOOLEAN DEFAULT TRUE,
    is_default  BOOLEAN DEFAULT FALSE,
    test_status TEXT DEFAULT 'unknown', -- unknown | ok | error
    last_tested DATETIME,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Token 消耗统计表
CREATE TABLE token_usage (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            DATE NOT NULL,
    provider_id     TEXT,
    model           TEXT,
    agent_slug      TEXT,
    conversation_id INTEGER,
    task_id         INTEGER,
    tokens_input    INTEGER DEFAULT 0,
    tokens_output   INTEGER DEFAULT 0,
    cost_usd        REAL DEFAULT 0.0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 定时任务

```sql
-- 定时任务表
CREATE TABLE cron_jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id          TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    description     TEXT,
    cron_expression TEXT NOT NULL,         -- 如 0 9 * * 1-5
    agent_slug      TEXT,                  -- 执行的 Agent
    task_template   TEXT,                  -- JSON，任务模板
    is_enabled      BOOLEAN DEFAULT TRUE,
    last_run_at     DATETIME,
    last_run_status TEXT,                  -- success | error | running
    next_run_at     DATETIME,
    run_count       INTEGER DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 定时任务执行历史
CREATE TABLE cron_run_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id      TEXT REFERENCES cron_jobs(job_id),
    started_at  DATETIME NOT NULL,
    ended_at    DATETIME,
    status      TEXT,                      -- success | error | running
    log         TEXT,
    task_id     INTEGER REFERENCES tasks(id)
);
```

#### 财务管理

```sql
-- 财务记录表（与 finance_tracker.csv 双向同步）
CREATE TABLE finance_records (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    record_date     DATE NOT NULL,
    type            TEXT NOT NULL,         -- income | expense
    category        TEXT NOT NULL,         -- mrr | project | llm_cost | tool_cost | other
    amount          REAL NOT NULL,
    currency        TEXT DEFAULT 'CNY',
    description     TEXT,
    project_id      INTEGER REFERENCES projects(id),
    invoice_no      TEXT,
    is_recurring    BOOLEAN DEFAULT FALSE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 知识资产

```sql
-- Wiki 文档表
CREATE TABLE wiki_docs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    content     TEXT,                      -- Markdown 内容
    file_path   TEXT,                      -- 对应文件系统路径（如有）
    parent_id   INTEGER REFERENCES wiki_docs(id),
    tags        TEXT,                      -- JSON 数组
    is_published BOOLEAN DEFAULT TRUE,
    created_by  INTEGER REFERENCES users(id),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- MCP 连接表
CREATE TABLE mcp_connections (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    transport       TEXT DEFAULT 'stdio',  -- stdio | sse | websocket
    command         TEXT,
    args            TEXT,                  -- JSON 数组
    env_vars        TEXT,                  -- JSON 对象
    working_dir     TEXT,
    connect_timeout INTEGER DEFAULT 30,
    read_timeout    INTEGER DEFAULT 30,
    is_enabled      BOOLEAN DEFAULT TRUE,
    status          TEXT DEFAULT 'unknown',
    last_tested     DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 系统配置表（键值对）
CREATE TABLE system_config (
    key         TEXT PRIMARY KEY,
    value       TEXT,
    type        TEXT DEFAULT 'string',     -- string | boolean | json | number
    description TEXT,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 四、用户系统设计

### 4.1 认证流程

OPC 工作台采用 JWT 双令牌认证机制，确保公网访问安全性。

**登录流程**：

1. CEO 在登录页输入用户名和密码
2. 后端验证密码（bcrypt），生成 Access Token（15分钟有效）和 Refresh Token（30天有效）
3. Access Token 存储在内存（Zustand），Refresh Token 存储在 HttpOnly Cookie
4. 每次 API 请求携带 Access Token，过期前 5 分钟自动静默刷新
5. Refresh Token 过期后跳转登录页，不丢失当前操作上下文

**移动端适配**：移动端使用相同的 JWT 机制，通过 localStorage 存储 Refresh Token（HttpOnly Cookie 在移动端 WebView 中可能受限）。

### 4.2 用户角色

| 角色 | 权限范围 |
|---|---|
| CEO（owner） | 全部权限：读写所有数据、审批操作、配置管理、删除操作 |
| Observer（观察者） | 只读权限：查看仪表盘、任务状态、日志，不可操作 |

### 4.3 API 端点设计（认证模块）

| 方法 | 路径 | 功能 | 权限 |
|---|---|---|---|
| POST | `/api/v1/auth/login` | 登录，返回 Access Token + Refresh Token | 公开 |
| POST | `/api/v1/auth/refresh` | 刷新 Access Token | 需要 Refresh Token |
| POST | `/api/v1/auth/logout` | 登出，撤销 Refresh Token | 已登录 |
| GET | `/api/v1/auth/me` | 获取当前用户信息 | 已登录 |
| PUT | `/api/v1/auth/password` | 修改密码 | CEO |

---

## 五、功能模块详细设计

### 5.1 指挥大盘（Dashboard）

**页面布局**：顶部 KPI 卡片行（4个）+ 中部两栏（左：活跃项目网格，右：系统脉搏心电图）+ 底部两栏（左：Agent 工负排行，右：最近活动流）

**数据来源**：
- KPI 数据：聚合 `tasks`、`token_usage`、`approvals` 表
- 活跃项目：读取 `projects` 表（status != archived/cancelled）
- 系统脉搏：WebSocket 推送，每 5 秒刷新 Agent 状态
- 最近活动：聚合 `audit_logs` + `kairos_logs` 文件

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/dashboard/kpi` | 获取今日/本周/本月 KPI 数据 |
| GET | `/api/v1/dashboard/projects` | 获取活跃项目列表（含进度） |
| GET | `/api/v1/dashboard/activity-feed` | 获取最近 50 条活动记录 |
| WS | `/ws/dashboard` | WebSocket：Agent 状态实时推送 |

**增删改查**：
- 查：仪表盘数据为只读聚合，无增删改操作
- 硬停警报：当 `approvals` 表有 `status=pending AND priority=critical` 时，顶部显示红色警报横幅，点击跳转审批中心

---

### 5.2 活体图谱（Agents）

**页面布局**：左侧 Agent 列表（可切换卡片视图/列表视图）+ 右侧详情抽屉（SOUL.md 透视镜）+ 顶部星系视图切换按钮

**星系视图**：以 CoS 为中心，四大团队（营销/产品/运营/公司层）为同心轨道，Agent 节点大小反映工负分数，发光强度反映实时活跃度，连线表示 A2A 协作关系。

**SOUL.md 透视镜**：点击 Agent 节点，右侧抽屉展开，显示：
- 角色头衔 + 团队标签 + 状态指示灯
- SOUL.md 全文（Markdown 渲染）
- 绑定工具列表（可启用/禁用）
- 近 7 天 Token 消耗趋势图
- 最近执行的任务列表（3条）
- 直接对话按钮（跳转 ChatConsole 并预设 Agent）

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/agents` | 获取所有 Agent 列表（含状态） |
| GET | `/api/v1/agents/{slug}` | 获取单个 Agent 详情（含 SOUL.md） |
| PUT | `/api/v1/agents/{slug}` | 更新 Agent 配置（名称、状态、工具权限） |
| POST | `/api/v1/agents/{slug}/sync-soul` | 从文件系统重新同步 SOUL.md |
| GET | `/api/v1/agents/{slug}/stats` | 获取 Agent 运行统计（Token、任务数） |
| PUT | `/api/v1/agents/{slug}/tools/{tool}` | 启用/禁用特定工具 |
| GET | `/api/v1/agents/graph` | 获取 A2A 协作关系图数据 |

**增删改查**：
- 增：不支持在 UI 中新建 Agent（Agent 由 SOUL.md 文件定义，通过 sync-soul 同步）
- 删：不支持删除（只能禁用）
- 改：可修改 Agent 的显示名称、状态、工具权限
- 查：支持按团队、状态、工负分数筛选和排序

---

### 5.3 任务管理中心（Backstage）

这是 Phase 1 最大的功能缺口，也是 OPC 工作台最核心的新增模块。

**页面布局**：顶部工具栏（新建任务、筛选、视图切换）+ 主体 Kanban 看板（4列：待执行/执行中/审核中/已完成）+ 右侧任务详情抽屉

**Kanban 看板**：
- 每列显示任务卡片，支持拖拽移动（改变状态）
- 任务卡片：任务标题 + 指派 Agent 头像 + 优先级标签 + 截止日期 + 进度条
- 列标题显示任务数量统计

**任务详情抽屉**（点击任务卡片展开）：
- 任务基本信息（标题、描述、优先级、截止日期）
- 指派 Agent 选择器
- Plan 步骤列表（可勾选，显示完成进度）
- 思考链日志（实时 SSE 流式输出，可折叠）
- 工具调用记录（展开/折叠，显示工具名、参数、结果）
- 子任务列表（支持嵌套）
- 评论/备注区域
- 操作按钮：暂停/恢复/停止/重新分配

**新建任务弹窗**：
- 任务标题（必填）
- 任务描述（Markdown 编辑器）
- 关联项目（下拉选择）
- 指派 Agent（下拉，显示 Agent 当前工负）
- 优先级（低/中/高/紧急）
- 截止日期（日期选择器）
- 上下文文件（拖拽上传或选择已有文件）
- 执行前需 CEO 确认（开关，默认开启）

**CEO 确认流程**：
1. 新建任务时，若"执行前需 CEO 确认"开启，任务进入 `pending` 状态
2. 仪表盘顶部显示待确认任务数量徽章
3. CEO 在任务详情中点击"确认执行"，任务状态变为 `assigned`
4. 系统通过 WebSocket 通知对应 Agent 开始执行

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/tasks` | 获取任务列表（支持筛选、分页） |
| POST | `/api/v1/tasks` | 新建任务 |
| GET | `/api/v1/tasks/{id}` | 获取任务详情 |
| PUT | `/api/v1/tasks/{id}` | 更新任务（状态、指派、优先级等） |
| DELETE | `/api/v1/tasks/{id}` | 删除任务（软删除） |
| POST | `/api/v1/tasks/{id}/approve` | CEO 确认执行任务 |
| POST | `/api/v1/tasks/{id}/stop` | 停止任务执行 |
| GET | `/api/v1/tasks/{id}/thinking-log` | 获取思考链日志 |
| SSE | `/api/v1/tasks/{id}/stream` | SSE：实时推送任务执行进度 |
| POST | `/api/v1/tasks/{id}/comments` | 添加评论 |
| GET | `/api/v1/projects` | 获取项目列表 |
| POST | `/api/v1/projects` | 新建项目 |
| PUT | `/api/v1/projects/{id}` | 更新项目 |
| DELETE | `/api/v1/projects/{id}` | 归档项目 |

**增删改查**：
- 增：新建任务（弹窗表单）、新建项目（侧边抽屉）
- 删：软删除（移入已取消列），不物理删除
- 改：拖拽改状态、点击编辑详情、重新指派 Agent
- 查：按状态/Agent/项目/优先级/日期范围多维筛选，支持全文搜索

---

### 5.4 CEO 对话干预（ChatConsole）

**页面布局**：左侧会话列表（可折叠）+ 中间对话区 + 右侧 Agent 信息面板（可折叠）

**核心交互**：
- `@Agent名称` 触发 Agent 选择器，自动注入对应 SOUL.md 为 System Prompt
- 拖拽文件到对话区，自动作为上下文挂载
- 思考链折叠展示（Claude Thinking 模式）
- 工具调用实时展示（工具名 + 参数 + 结果）
- 消息支持 Markdown 渲染、代码高亮、复制

**LLM 多提供商路由**：
- 在会话设置中选择首选提供商和模型
- 若首选提供商返回错误，自动切换到下一个（按优先级排序）
- 切换时保持完整的对话历史上下文
- 底部状态栏显示当前使用的提供商和模型

**上下文挂载**：
- 支持挂载 SOUL.md、brief.md、status.json、kairos_logs 等文件
- 挂载文件以 `<context>` 标签注入 System Prompt
- 显示已挂载文件列表，支持移除

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/conversations` | 获取会话列表 |
| POST | `/api/v1/conversations` | 新建会话 |
| DELETE | `/api/v1/conversations/{id}` | 归档/删除会话 |
| GET | `/api/v1/conversations/{id}/messages` | 获取消息历史 |
| SSE | `/api/v1/conversations/{id}/chat` | SSE：流式对话（支持工具调用） |
| POST | `/api/v1/conversations/{id}/context` | 添加上下文文件 |
| DELETE | `/api/v1/conversations/{id}/context/{file}` | 移除上下文文件 |

---

### 5.5 时空追溯（Timeline）

**页面布局**：顶部筛选栏（类型/项目/日期范围）+ 主体垂直时间线 + 悬浮正反合透镜

**时间线条目**：
- 每条 KAIROS 日志条目显示：时间戳 + 事件类型图标 + 摘要文本 + 来源 Agent
- 点击展开：完整日志内容（Markdown 渲染）
- 悬浮"正反合透镜"按钮：展开 CoS 的决策备选方案视图

**正反合透镜**（OPC 独有功能）：
- 正（Thesis）：当前选择的方案
- 反（Antithesis）：被否定的备选方案
- 合（Synthesis）：综合考量的理由

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/timeline` | 获取时间线数据（支持分页、筛选） |
| GET | `/api/v1/timeline/{id}` | 获取单条日志详情（含正反合） |
| POST | `/api/v1/timeline` | 手动添加日志条目 |
| DELETE | `/api/v1/timeline/{id}` | 删除日志条目 |

---

### 5.6 安全审批中心（Security）

**子页面**：工具防护 / 文件防护 / 审批队列 / 审计日志

**工具防护**：
- 安全规则列表（表格）：规则名/正则/严重级别/分类/处置方式/启用开关
- 新增规则弹窗：规则ID/名称/正则/严重级别/分类/处置/目标工具/优先级
- 预置 OPC 专用规则（对应 KAIROS 的 hard-stop 机制）

**审批队列**：
- 待审批列表（按优先级排序，critical 置顶）
- 每条审批请求：标题/请求方Agent/类型/创建时间/过期时间
- 点击展开：完整请求详情 + 相关上下文
- 操作：批准（绿色按钮）/ 拒绝（红色按钮）+ 备注输入框
- 批准/拒绝后通过 WebSocket 通知对应 Agent

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/approvals` | 获取审批列表（支持状态筛选） |
| GET | `/api/v1/approvals/{id}` | 获取审批详情 |
| POST | `/api/v1/approvals/{id}/approve` | 批准 |
| POST | `/api/v1/approvals/{id}/reject` | 拒绝 |
| GET | `/api/v1/security/rules` | 获取安全规则列表 |
| POST | `/api/v1/security/rules` | 新建安全规则 |
| PUT | `/api/v1/security/rules/{id}` | 更新安全规则 |
| DELETE | `/api/v1/security/rules/{id}` | 删除安全规则 |
| GET | `/api/v1/audit-logs` | 获取审计日志（支持筛选、分页） |

---

### 5.7 定时任务管理（CronJobs）

**页面布局**：任务列表（表格）+ 新建/编辑弹窗 + 执行历史抽屉

**预置 OPC 定时任务**：
- 每日晨报（周一至周五 9:00）：CoS 生成当日工作摘要
- 每周复盘（周五 17:00）：CoS 生成本周 KAIROS 日志总结
- 财务月报（每月1日 10:00）：Finance Agent 生成月度财务报告
- 客户跟进提醒（每日 10:00）：Scout 检查客户跟进状态

**新建任务弹窗**：
- 任务名称（必填）
- Cron 表达式（必填，带可视化解释器）
- 指派 Agent（下拉）
- 任务模板（Markdown，描述 Agent 需要执行的任务）
- 启用（开关）

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/cron-jobs` | 获取定时任务列表 |
| POST | `/api/v1/cron-jobs` | 新建定时任务 |
| PUT | `/api/v1/cron-jobs/{id}` | 更新定时任务 |
| DELETE | `/api/v1/cron-jobs/{id}` | 删除定时任务 |
| POST | `/api/v1/cron-jobs/{id}/run` | 立即执行一次 |
| PUT | `/api/v1/cron-jobs/{id}/toggle` | 启用/禁用 |
| GET | `/api/v1/cron-jobs/{id}/history` | 获取执行历史 |

---

### 5.8 财务运营大盘（Finance）

**页面布局**：顶部 KPI 卡片（MRR/ARR/本月收入/本月成本）+ 中部图表区（月度趋势 + 成本构成饼图）+ 底部交付记录表

**数据来源**：`finance_records` 表 + `finance_tracker.csv` 文件（双向同步）

**图表组件**：
- 月度收入/利润趋势折线图（12个月）
- 成本构成饼图（LLM成本/工具成本/其他）
- 转化漏斗（线索→商机→成交）
- 项目收入排行榜

**增删改查**：
- 增：新建财务记录弹窗（日期/类型/分类/金额/描述/关联项目）
- 删：软删除财务记录
- 改：编辑财务记录
- 查：按日期范围/类型/分类筛选，支持导出 CSV

**API 端点**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/finance/kpi` | 获取财务 KPI 数据 |
| GET | `/api/v1/finance/records` | 获取财务记录列表 |
| POST | `/api/v1/finance/records` | 新建财务记录 |
| PUT | `/api/v1/finance/records/{id}` | 更新财务记录 |
| DELETE | `/api/v1/finance/records/{id}` | 删除财务记录 |
| GET | `/api/v1/finance/export` | 导出 CSV |

---

### 5.9 配置中心（Settings）

**子页面**：模型管理 / 系统设置 / 工作区 / Agent 上下文 / MCP 连接 / 工具目录 / Token 统计 / 功能开关 / 关于

**模型管理**（对标 MateClaw 模型管理页）：
- 已配置提供商列表（表格）：名称/类型/状态/优先级/操作
- 新增提供商弹窗：提供商ID/名称/Base URL/API Key/协议/优先级
- 测试连接按钮（实时验证 API Key 有效性）
- 拖拽排序（调整故障转移优先级）

**Agent 上下文**（对标 MateClaw 智能体上下文页）：
- 选择 Agent 下拉
- 核心文件列表（SOUL.md/AGENTS.md/MEMORY.md 等，可开关）
- 文件内容预览/编辑（Markdown 编辑器，支持编辑/分屏/预览三模式）
- 新建文件、保存、重置、删除

**API 端点（配置中心）**：

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/api/v1/settings/llm-providers` | 获取 LLM 提供商列表 |
| POST | `/api/v1/settings/llm-providers` | 新增提供商 |
| PUT | `/api/v1/settings/llm-providers/{id}` | 更新提供商 |
| DELETE | `/api/v1/settings/llm-providers/{id}` | 删除提供商 |
| POST | `/api/v1/settings/llm-providers/{id}/test` | 测试连接 |
| GET | `/api/v1/settings/system` | 获取系统配置 |
| PUT | `/api/v1/settings/system` | 更新系统配置 |
| GET | `/api/v1/settings/agent-context/{slug}` | 获取 Agent 上下文文件列表 |
| PUT | `/api/v1/settings/agent-context/{slug}/{file}` | 更新上下文文件内容 |
| GET | `/api/v1/settings/mcp` | 获取 MCP 连接列表 |
| POST | `/api/v1/settings/mcp` | 新增 MCP 连接 |
| PUT | `/api/v1/settings/mcp/{id}` | 更新 MCP 连接 |
| DELETE | `/api/v1/settings/mcp/{id}` | 删除 MCP 连接 |
| POST | `/api/v1/settings/mcp/{id}/test` | 测试 MCP 连接 |
| GET | `/api/v1/settings/token-usage` | 获取 Token 消耗统计 |

---

### 5.10 知识资产管理（Wiki）

**页面布局**：左侧文件树（支持文件夹嵌套）+ 右侧 Markdown 编辑器

**数据来源**：`wiki_docs` 表 + `ai-company-os/` 文件系统（双向同步）

**功能**：
- 新建文档/文件夹
- 全文搜索（标题+内容）
- 文档可被 Agent 对话引用（通过上下文挂载）
- 支持文件上传（图片、PDF）

---

## 六、⌘K 全局命令面板

命令面板是 OPC 工作台最核心的交互创新，支持以下命令类型：

| 命令类型 | 示例 | 动作 |
|---|---|---|
| 导航 | `go dashboard` | 跳转到指挥大盘 |
| Agent 操作 | `chat scout` | 打开与 Scout 的对话 |
| 任务操作 | `new task` | 打开新建任务弹窗 |
| 审批操作 | `approve APR-001` | 直接批准审批请求 |
| 项目跳转 | `project P-001` | 跳转到项目详情 |
| 搜索 | `search 客户跟进` | 全局搜索 |
| 配置 | `settings models` | 跳转到模型配置 |

---

## 七、移动端适配策略

移动端采用响应式布局，关键适配点如下：

| 页面 | 桌面端 | 移动端 |
|---|---|---|
| 指挥大盘 | 多栏网格 | 单列滚动，KPI 卡片 2x2 |
| 活体图谱 | 星系视图 + 详情抽屉 | 列表视图，点击展开详情 |
| 任务管理 | Kanban 看板 | 单列列表，状态标签筛选 |
| 对话干预 | 三栏布局 | 全屏对话，底部输入框 |
| 审批中心 | 表格 + 详情 | 卡片列表，滑动操作 |

底部导航栏（移动端）：仪表盘 / 任务 / 对话 / 审批 / 更多

---

## 八、暗色/亮色主题切换

主题切换基于 CSS 变量，支持：
- 系统自动跟随（prefers-color-scheme）
- 手动切换（右上角切换按钮）
- 记忆用户偏好（localStorage）

**暗色主题**（默认）：深空黑 `#080C14`，电青 `#00D4FF` 强调色
**亮色主题**：暖白 `#F8F9FA`，深海蓝 `#0A2540` 强调色

---

## 九、分阶段开发计划

### Phase 2（Week 1-2）：全栈化 + 真实数据

**目标**：将 Phase 1 的静态 mock 数据替换为真实文件系统数据，建立完整的前后端通信。

**Week 1 任务**：
1. 升级项目为 `web-db-user` 全栈模式
2. 搭建 FastAPI 后端框架（数据库初始化、JWT 认证、基础路由）
3. 实现登录页面（用户名/密码，JWT 存储）
4. 实现文件系统读取服务（SOUL.md 解析、status.json 读取）
5. 替换指挥大盘的 mock 数据为真实 API 数据

**Week 2 任务**：
1. 实现 Agent 管理 API（CRUD + SOUL.md 同步）
2. 替换活体图谱的 mock 数据
3. 实现 KAIROS 日志解析服务
4. 替换时空追溯的 mock 数据
5. 实现 WebSocket 服务（Agent 状态实时推送）

**交付物**：可登录的完整工作台，仪表盘/图谱/时间线显示真实数据

---

### Phase 3（Week 3）：任务管理中心

**目标**：实现完整的任务发布、管理、执行监控闭环。

**任务列表**：
1. 任务数据库表创建 + API 实现
2. Kanban 看板 UI（拖拽支持）
3. 新建任务弹窗（含 CEO 确认机制）
4. 任务详情抽屉（Plan 步骤 + 思考链）
5. SSE 流式推送任务执行进度
6. 项目管理 CRUD

**交付物**：可发布任务、查看执行进度、CEO 确认审批的完整任务管理系统

---

### Phase 4（Week 4）：对话干预 + 审批流

**目标**：实现 CEO 与 Agent 的直接对话，以及完整的安全审批机制。

**任务列表**：
1. LLM 多提供商路由服务（LiteLLM 集成）
2. 对话 API（SSE 流式输出 + 工具调用）
3. ChatConsole UI（@Agent 注入、上下文挂载、思考链展示）
4. 审批队列 UI（批准/拒绝 + WebSocket 通知）
5. 安全规则管理 CRUD
6. 审计日志查看

**交付物**：可与任意 Agent 对话，支持多 LLM 故障转移，审批流完整可用

---

### Phase 5（Week 5）：定时任务 + 配置中心

**目标**：实现定时任务调度和完整的系统配置管理。

**任务列表**：
1. APScheduler 集成，Cron 任务 CRUD
2. 预置 4 个 OPC 定时任务
3. 模型管理 UI（提供商增删改查 + 测试连接）
4. Agent 上下文编辑器（Markdown 编辑器集成）
5. MCP 连接管理 CRUD
6. Token 统计图表

**交付物**：定时任务可配置可执行，LLM 提供商可在 UI 中管理

---

### Phase 6（Week 6）：财务大盘 + 知识资产 + 移动端优化

**目标**：完成所有功能模块，优化移动端体验，完成完整闭环。

**任务列表**：
1. 财务记录 CRUD + 图表展示
2. finance_tracker.csv 双向同步
3. Wiki 文档管理（文件树 + Markdown 编辑器）
4. 移动端响应式全面优化
5. ⌘K 命令面板完整实现（含自然语言命令解析）
6. 暗色/亮色主题切换完善
7. 性能优化（虚拟列表、懒加载）
8. Docker Compose 部署配置

**交付物**：功能完整、移动端可用、可 Docker 部署的 OPC 工作台正式版

---

## 十、MateClaw UI 可直接借鉴的组件模式

基于对 MateClaw 28页截图和 15个页面源码的分析，以下 UI 模式可直接参考实现：

| 组件/模式 | MateClaw 来源 | OPC 应用位置 |
|---|---|---|
| 三栏布局（导航+内容+抽屉） | MainLayout | 所有主页面 |
| Agent 卡片网格 | Agents.vue | 活体图谱列表视图 |
| Kanban 看板 + 状态拖拽 | Backstage.vue | 任务管理中心 |
| 思考链折叠展示 | ChatConsole.vue | 任务详情 + 对话界面 |
| 模型提供商弹窗（Base URL + API Key） | Settings/Models | 配置中心模型管理 |
| 安全规则表格 + 新增规则弹窗 | Security/ToolGuard | 安全审批中心 |
| MCP 连接管理弹窗 | McpServers.vue | 配置中心 MCP 管理 |
| 工具目录启用/禁用开关 | Tools.vue | Agent 工具权限管理 |
| Agent 上下文文件编辑器 | AgentContext.vue | 配置中心 Agent 上下文 |
| Token 统计日期范围图表 | TokenUsage.vue | 配置中心 Token 统计 |
| 功能开关列表（带实验性标签） | FeatureFlags.vue | 配置中心功能开关 |
| 登录页（用户名/密码/加载状态） | Login.vue | 登录页 |
| Cron 任务表格 + 立即运行 | CronJobs.vue | 定时任务管理 |
| 数据源连接测试弹窗 | Datasources.vue | MCP/工具连接测试 |

---

*文档版本：v4.0 | 最后更新：2026-05-05 | 作者：Manus AI*
