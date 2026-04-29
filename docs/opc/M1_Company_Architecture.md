# M1: OPC 完整公司目录架构 (Company OS Architecture)

## 1. 架构设计原则

OPC (One Person Company) 的目录架构不再是一个单纯的代码仓库，而是一个**公司级操作系统 (Company OS)**。其设计遵循以下原则：

1. **业务闭环映射**：目录结构严格映射商业闭环的四个引擎（战略、营销、生产、运营）。
2. **Fail-closed 权限隔离**：每个 Agent 只能读写其专属目录，跨部门协作必须通过 `shared_workspace` 进行。
3. **状态可见性**：CEO 可以通过查看特定目录（如 `active_projects`）立即了解公司运转状态。
4. **向下兼容**：原有的 OPT 龙虾军团（`opt-openclaw-v6`）作为生产引擎，被完整降级并嵌入到 `3_production/infrastructure/` 目录下，保持其内部结构的完整性。

---

## 2. 顶层目录结构全景图

```text
ai-company-os/                     # OPC 公司根目录
├── .opc/                          # 公司级系统配置 (CLI 工具使用)
│   ├── config.json                # 全局配置 (API Keys, 域名, 支付网关)
│   └── cli/                       # opc-cli 命令行工具源码
│
├── 1_strategy/                    # 战略与财务 (CEO 专属，最高权限)
│   ├── business_model.md          # 商业模式与定价策略定义
│   ├── finance_tracker.csv        # 收入与 API 成本追踪表
│   └── ESCALATIONS/               # 需要 CEO 紧急处理的升级事件
│
├── 2_marketing/                   # 流量与转化引擎 (Front-Office)
│   ├── agents/                    # 公司层 Agent 配置
│   │   ├── scout/                 # 小探 (线索抓取)
│   │   ├── broadcaster/           # 小播 (内容分发)
│   │   └── closer/                # 小销 (销售转化)
│   ├── leads/                     # 抓取到的潜在客户名单 (CSV/JSON)
│   ├── content_matrix/            # 自动生成的营销内容草稿与发布记录
│   └── sales_scripts/             # 销售话术、邮件模板与报价单
│
├── 3_production/                  # 生产引擎 (Back-Office)
│   ├── active_projects/           # 正在执行的客户订单 (按项目建档)
│   │   └── Client_A_Landing_Page/ # 示例项目目录
│   │       ├── brief.md           # 客户需求文档
│   │       ├── status.json        # 项目状态机
│   │       └── workspace/         # 该项目的局部共享工作区
│   │
│   ├── infrastructure/            # 生产基础设施
│   │   └── lobster-legion/        # 龙虾军团 (原 opt-openclaw-v6 完整迁移)
│   │       ├── agents/            # 16 个生产层 Agent (设计+开发)
│   │       ├── engine/            # KAIROS, TAOR 等底层引擎
│   │       └── config/            # 龙虾军团内部配置
│   │
│   ├── shared_workspace/          # 跨团队公共交换区 (设计与开发交接)
│   │   ├── design_handoffs/       # 设计团队输出的规范与切图
│   │   └── api_contracts/         # 开发团队输出的接口文档
│   │
│   └── global_skills/             # 全局技能库 (跨项目复用的 SKILL.md)
│
└── 4_operations/                  # 交付与运营引擎
    ├── agents/
    │   └── csm/                   # 小服 (客户成功与交付)
    ├── deliverables/              # 生产完成、待发送给客户的最终交付物
    └── feedback_loop/             # 客户反馈记录与迭代建议
```

---

## 3. 核心目录用途详解

### 3.1 `1_strategy/` (战略与财务)
- **用途**：公司的"大脑"和"账本"。只有 CEO（人类）和特定的财务脚本有写入权限。
- **关键文件**：
  - `finance_tracker.csv`：记录每一笔 Stripe 收入和 OpenAI/Anthropic API 支出，用于计算真实利润率。
  - `ESCALATIONS/`：当任何 Agent 遇到无法解决的问题（如 API 额度耗尽、客户提出退款），会在此目录下生成 `.md` 文件，触发 CEO 手机报警。

### 3.2 `2_marketing/` (流量与转化)
- **用途**：公司的"销售部"。负责从公域获取流量，并转化为付费订单。
- **关键文件**：
  - `leads/`：小探 (Scout) 每天抓取的潜在客户名单，包含邮箱、公司背景、痛点分析。
  - `sales_scripts/`：小销 (Closer) 使用的标准化邮件模板。当客户回复邮件时，小销会根据模板自动生成回复并抄送 CEO。

### 3.3 `3_production/active_projects/` (项目执行区)
- **用途**：公司的"车间"。每一个付费订单都会在这里生成一个独立的文件夹。
- **关键文件**：
  - `status.json`：记录项目当前处于哪个阶段（如 `DESIGNING`, `DEVELOPING`, `TESTING`, `READY_FOR_DELIVERY`）。
  - `workspace/`：该项目专属的局部工作区，设计团队和开发团队在此交换中间产物，项目结束后归档。

### 3.4 `3_production/infrastructure/lobster-legion/` (龙虾军团)
- **用途**：公司的"生产设备"。这是原有的 `opt-openclaw-v6` 仓库。
- **改造点**：
  - 内部结构保持不变（包含 `agents/`, `engine/` 等）。
  - 修改其 `openclaw.json` 中的路径配置，使其能够读取上层的 `active_projects/` 和 `shared_workspace/`。

### 3.5 `3_production/shared_workspace/` (公共交换区)
- **用途**：解决设计团队和开发团队的跨团队协作问题。
- **关键机制**：
  - 设计团队（小运）将最终的设计规范和切图放入 `design_handoffs/`。
  - 开发团队（FE）从该目录读取资产进行编码。
  - 任何一方不得直接修改对方内部工作区的文件。

### 3.6 `4_operations/` (交付与运营)
- **用途**：公司的"客服部"。负责将生产好的产品打包发送给客户。
- **关键文件**：
  - `deliverables/`：当项目状态变为 `READY_FOR_DELIVERY` 时，生产引擎会将最终代码/设计稿复制到这里。小服 (CSM) 会监控此目录，自动生成交付邮件发送给客户。

---

## 4. 目录权限矩阵 (Fail-closed)

为了防止 Agent 幻觉导致系统崩溃，实施严格的目录读写权限控制：

| 目录 | CEO | 公司层 Agent (小探/小播/小销/小服) | 生产层 Agent (龙虾军团) |
|---|---|---|---|
| `1_strategy/` | **读/写** | 仅读 (部分) | 无权限 |
| `2_marketing/` | **读/写** | **读/写** | 无权限 |
| `3_production/active_projects/` | **读/写** | 仅读 (小服) | **读/写** |
| `3_production/shared_workspace/`| **读/写** | 无权限 | **读/写** |
| `4_operations/` | **读/写** | **读/写** (小服) | 仅写 (交付物) |

---
*本模块定义了 OPC 的物理骨架。下一模块 (M2) 将定义在这个骨架中运行的 20 个 Agent 的灵魂。*
