# OPC (One Person Company) 多智能体公司操作系统

> **"一句话触发，多智能体自主完成商业闭环。"**

OPC 是一个由 20 个 AI Agent 驱动的完整公司操作系统。它不仅仅是一个开发工具，而是一家**真实运营的智能体公司**。

系统包含四大引擎，实现了从获客、销售、生产到交付的端到端自动化。

---

## 🚀 核心架构：四引擎商业闭环

```mermaid
graph LR
    A[流量引擎] -->|线索| B[转化引擎]
    B -->|订单| C[生产引擎]
    C -->|交付物| D[交付引擎]
    
    subgraph 公司层 (Front-Office)
    A(小探 Scout / 小播 Broadcaster)
    B(小销 Closer)
    D(小服 CSM)
    end
    
    subgraph 生产层 (Back-Office)
    C(龙虾军团: 8个设计Agent + 8个开发Agent)
    end
```

### 1. 流量引擎 (Marketing)
- **小探 (Scout)**：每天自动从 Product Hunt / LinkedIn 抓取高质量潜在客户线索。
- **小播 (Broadcaster)**：每天自动生成并发布 Twitter / LinkedIn 营销内容。

### 2. 转化引擎 (Sales)
- **小销 (Closer)**：自动发送冷邮件，处理客户回复。
- **触发机制**：当检测到 Stripe 支付成功，或 CEO 审批通过时，自动创建项目并触发生产引擎。

### 3. 生产引擎 (Production)
- **龙虾军团 (Lobster Legion)**：包含 16 个专业 Agent（设计团队 + 开发团队）。
- **工作流**：CoS 接单 → 设计团队出图 → 开发团队写代码 → QA 验收。

### 4. 交付引擎 (Operations)
- **小服 (CSM)**：监听到生产完成，自动打包交付物发送给客户，收集反馈并归档。

---

## 📂 目录结构

```
ai-company-os/
├── .opc/config.json              ← 全局配置（API Keys、定价、触发器）
├── 1_strategy/                   ← 战略层（商业模式、财务追踪、CEO审批）
├── 2_marketing/                  ← 营销层（小探、小播、小销）
├── 3_production/                 ← 生产层
│   ├── active_projects/          ← 正在进行的项目（状态机驱动）
│   ├── shared_workspace/         ← 双团队公共工作区与交接规范
│   └── infrastructure/
│       └── lobster-legion/       ← 龙虾军团（核心生产力引擎）
├── 4_operations/                 ← 运营层（小服、交付物、客户反馈）
└── docs/opc/                     ← 系统架构与规范文档 (M1-M5)
```

---

## ⚙️ 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/leixing333/ai-company-os.git
cd ai-company-os
```

### 2. 配置环境变量
复制 `.opc/config.json.example` 为 `.opc/config.json`，填入你的 API Keys（OpenAI, Anthropic, Stripe, Resend）。

### 3. 启动 OPC 守护进程
```bash
python3 .opc/cli/opc_daemon.py start
```
系统将自动接管定时任务和目录监听，开始自动化运转。

---

## 📖 核心文档导航

- [M1: 公司目录架构规范](docs/opc/M1_Company_Architecture.md)
- [M2: 20 个 Agent 角色卡](docs/opc/M2_Agent_Cards.md)
- [M3: 商业闭环状态机协议](docs/opc/M3_Business_Loop_Protocol.md)
- [M4: 技术规范与解决方案](docs/opc/M4_Technical_Specs.md)
- [M5: 开发路线图](docs/opc/M5_Execution_Roadmap.md)
- [生产层双团队协同协议](docs/opc/OPC_Production_Layer_Protocol.md)

---
*Powered by OPT Lobster Legion v7.2.0*
