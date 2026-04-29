# OPC (One Person Company) — AI 多智能体公司操作系统

> **一句话描述**：一个由 20 个 AI Agent 协同驱动的一人公司，从获客、销售、生产到交付，全流程自动化运转。

---

## 系统架构总览

```
ai-company-os/
├── .opc/                    # 公司级系统配置 (CLI 工具)
├── 1_strategy/              # 战略与财务 (CEO 专属)
├── 2_marketing/             # 流量与转化引擎 (前台：小探/小播/小销)
├── 3_production/            # 生产引擎 (后台：龙虾军团 16 Agents)
│   ├── active_projects/     # 正在执行的客户订单
│   ├── infrastructure/
│   │   └── lobster-legion/  # 龙虾军团 (开发+设计双团队)
│   ├── shared_workspace/    # 跨团队公共交换区
│   └── global_skills/       # 跨项目复用技能库
└── 4_operations/            # 交付与运营引擎 (小服)
```

---

## 20 个 Agent 分工

| 层级 | Agent | 职责 |
|---|---|---|
| **公司层** | 小探 (Scout) | 全网抓取潜在客户线索 |
| **公司层** | 小播 (Broadcaster) | 自动生成营销内容 |
| **公司层** | 小销 (Closer) | 发送冷邮件，促成付款 |
| **公司层** | 小服 (CSM) | 打包交付物，发送给客户 |
| **设计团队** | 小管/小研/小策/小设/小文/小牌/CDO/小运 | 视觉设计全流程 |
| **开发团队** | CoS/CTO/Researcher/FE/BE/QA/Ops/KO | 代码开发全流程 |

---

## 商业闭环

```
小探获客 → 小销转化 → 付款 → 龙虾军团生产 → 小服交付 → 复购
```

---

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/leixing333/ai-company-os.git
cd ai-company-os

# 2. 配置 API Keys
cp .opc/config.json .opc/config.local.json
# 编辑 .opc/config.local.json，填入 ANTHROPIC_API_KEY, STRIPE_API_KEY 等

# 3. 启动生产引擎（龙虾军团）
cd 3_production/infrastructure/lobster-legion
# 按照龙虾军团的 README.md 启动
```

---

## 文档导航

| 文档 | 说明 |
|---|---|
| [M1: 公司目录架构](docs/opc/M1_Company_Architecture.md) | 完整目录结构与权限矩阵 |
| [M2: Agent 角色卡](docs/opc/M2_Agent_Cards.md) | 20 个 Agent 的职责与接口 |
| [M3: 商业闭环协议](docs/opc/M3_Business_Loop_Protocol.md) | 状态机与数据契约 |
| [M4: 技术规范](docs/opc/M4_Technical_Specs.md) | 10 个技术问题解决方案 |
| [M5: 执行路线图](docs/opc/M5_Execution_Roadmap.md) | 4 个 Phase 开发清单 |
| [龙虾军团 README](3_production/infrastructure/lobster-legion/README.md) | 生产引擎详细文档 |

---

*OPC v1.0.0 | Phase 1 完成 | 基础设施与目录重构*
