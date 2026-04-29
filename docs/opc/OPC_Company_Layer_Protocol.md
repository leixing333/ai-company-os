# OPC 公司层 Agent 协作协议 (Company Layer Protocol)

> 本文档定义了公司层 4 个 Agent（小探/小播/小销/小服）与生产层（龙虾军团）之间的完整协作机制，确保商业闭环自动化运转。

---

## 1. 整体架构

```
                        ┌─────────────────────────────────────────┐
                        │           CEO (人类决策层)               │
                        │   只在 ESCALATED 状态时介入              │
                        └──────────────┬──────────────────────────┘
                                       │ 审批 / 处理升级事件
                    ┌──────────────────┼──────────────────────┐
                    │                  │                       │
          ┌─────────▼──────┐  ┌────────▼───────┐  ┌──────────▼──────┐
          │  流量引擎       │  │  转化引擎       │  │  交付引擎        │
          │  小探 + 小播    │  │  小销 (Closer) │  │  小服 (CSM)     │
          │  (获客)         │  │  (成交)         │  │  (交付+复购)    │
          └─────────┬──────┘  └────────┬───────┘  └──────────┬──────┘
                    │                  │                       │
                    │  leads/*.json    │  active_projects/     │  feedback_loop/
                    │                  │  status.json          │
                    └──────────────────┼──────────────────────┘
                                       │
                        ┌──────────────▼──────────────────────────┐
                        │         生产引擎 (龙虾军团)               │
                        │   CoS → 设计团队 → 开发团队 → QA → Ops   │
                        │   读取 active_projects/brief.md          │
                        │   写入 4_operations/deliverables/         │
                        └─────────────────────────────────────────┘
```

---

## 2. 完整商业闭环状态机

### 2.1 正常流转路径

```
[每日 08:00]
小探 扫描 Product Hunt / LinkedIn
    → 生成 leads/YYYYMMDD_CompanyX.json
    → 状态: LEAD_GENERATED

[每日 10:00]
小销 读取 leads/*.json (筛选 lead_score >= 7)
    → 生成个性化冷邮件
    → 通过 Resend API 发送
    → 更新 leads/CompanyX.json: status = "CONTACTED"

[客户回复后，实时触发]
小销 分析客户回复
    → 如果有意向: 发送报价单 + Stripe 支付链接
    → 更新状态: NEGOTIATING

[Stripe Webhook 支付成功 或 CEO 申请成功，实时触发]

**路径 A — 支付成功**
小销 接收 Stripe Webhook 支付成功事件
    → 创建 3_production/active_projects/P-YYYYMMDD-XXX/
    → 写入 brief.md，写入 status.json: current_status = "PRODUCTION_STARTED"
    → 记录 trigger_source = "payment"
    → 通知 CEO

**路径 B — CEO 申请成功**
小销 判断客户有明确意向但尚未付款
    → 写入 1_strategy/ESCALATIONS/CEO_APPROVAL_REQUEST_P-XXX.json
    → 更新线索状态: CEO_APPROVAL_PENDING
    → 发送通知等待 CEO 确认

CEO 确认后（手动写入或点击确认）
    → 创建 3_production/active_projects/P-YYYYMMDD-XXX/
    → 写入 brief.md，写入 status.json: current_status = "PRODUCTION_STARTED"
    → 记录 trigger_source = "ceo_approval"
    → 付款可在交付后结清（小销后续跟进）

[生产引擎自动接单，实时触发]
龙虾军团 CoS 扫描 active_projects/
    → 发现 status = "PRODUCTION_STARTED"
    → QAPS 拆解任务
    → 分配给设计团队或开发团队
    → 更新状态: DESIGNING / DEVELOPING

[生产完成，实时触发]
龙虾军团 Ops
    → 将交付物复制到 4_operations/deliverables/P-XXX/
    → 更新状态: READY_FOR_DELIVERY

[交付物就绪，实时触发]
小服 监听 deliverables/ 目录
    → 发现新文件且状态为 READY_FOR_DELIVERY
    → 生成个性化交付邮件
    → 通过 Resend API 发送给客户 (含附件/链接)
    → 更新状态: DELIVERED

[客户回复满意，实时触发]
小服 分析客户回复
    → 如果满意: 更新状态 = COMPLETED, 归档项目
    → 如果需要修改: 更新状态 = PRODUCTION_STARTED (退回生产)
    → 发送感谢邮件 + 复购邀请

[每月 1 日 09:00]
财务脚本 统计上月收入
    → 更新 1_strategy/finance_tracker.csv
    → 发送月度财务报告给 CEO
```

### 2.2 异常处理路径（Escalation）

当以下任何条件触发时，系统自动在 `1_strategy/ESCALATIONS/` 创建升级文件，并通知 CEO：

| 触发条件 | 升级原因 | CEO 需要做的事 |
|---|---|---|
| 报价超过 $5,000 | 超过自动授权额度 | 审批是否接单 |
| 客户邮件包含"refund/退款" | 潜在纠纷风险 | 亲自处理客户关系 |
| 生产超时 48 小时 | 可能影响 SLA | 检查生产引擎状态 |
| 当日 API 成本超过 $50 | 异常高消耗 | 检查是否有 Agent 失控 |

---

## 3. 文件接口规范

### 3.1 线索档案格式 (`leads/YYYYMMDD_CompanyName.json`)

```json
{
  "lead_id": "L-20251025-001",
  "company_name": "AI Startup X",
  "website": "https://startupx.com",
  "pain_point": "Hero 区缺乏清晰的价值主张，CTA 按钮颜色与背景对比度不足",
  "founder_name": "John Doe",
  "contact_email": "john@startupx.com",
  "lead_score": 8,
  "source": "Product Hunt",
  "status": "LEAD_GENERATED",
  "created_at": "2025-10-25T08:00:00Z",
  "updated_at": "2025-10-25T08:00:00Z",
  "notes": ""
}
```

### 3.2 项目状态文件格式 (`active_projects/P-XXX/status.json`)

```json
{
  "project_id": "P-20251025-001",
  "client_name": "AI Startup X",
  "client_email": "john@startupx.com",
  "package_tier": "Growth",
  "budget_usd": 2499,
  "current_status": "PRODUCTION_STARTED",
  "current_agent": "cos",
  "deadline_utc": "2025-10-28T12:00:00Z",
  "stripe_payment_id": "pi_xxx",
  "status_history": [
    { "status": "PAYMENT_RECEIVED", "timestamp": "2025-10-25T10:30:00Z", "agent": "closer" },
    { "status": "PRODUCTION_STARTED", "timestamp": "2025-10-25T10:31:00Z", "agent": "closer" }
  ],
  "created_at": "2025-10-25T10:30:00Z",
  "updated_at": "2025-10-25T10:31:00Z"
}
```

---

## 4. Agent 权限矩阵

| Agent | 可读目录 | 可写目录 | 禁止访问 |
|---|---|---|---|
| **小探 (Scout)** | 无 | `2_marketing/leads/` | 所有其他目录 |
| **小播 (Broadcaster)** | 无 | `2_marketing/content_matrix/` | 所有其他目录 |
| **小销 (Closer)** | `2_marketing/leads/` | `2_marketing/leads/`, `3_production/active_projects/` | `1_strategy/`, 龙虾军团内部 |
| **小服 (CSM)** | `3_production/active_projects/`, `4_operations/deliverables/` | `4_operations/deliverables/`, `4_operations/feedback_loop/`, `3_production/active_projects/*/status.json` | `1_strategy/`, 龙虾军团内部 |
| **龙虾军团 (CoS)** | `3_production/active_projects/` | `3_production/active_projects/*/workspace/`, `3_production/shared_workspace/`, `4_operations/deliverables/` | `1_strategy/`, `2_marketing/` |

---

## 5. 调度时间表

| 时间 | Agent | 任务 |
|---|---|---|
| 每天 08:00 | 小探 (Scout) | 抓取 Product Hunt 最新产品，生成线索 |
| 每天 10:00 | 小销 (Closer) | 读取新线索，发送冷邮件 |
| 每天 09:00 | 小播 (Broadcaster) | 生成并发布当日社交媒体内容 |
| 实时触发 | 小销 (Closer) | 处理客户回复邮件，发送报价单 |
| 实时触发 | 小销 (Closer) | 接收 Stripe Webhook，触发生产引擎 |
| 实时触发 | 龙虾军团 (CoS) | 扫描 active_projects，接单生产 |
| 实时触发 | 小服 (CSM) | 监听 deliverables，发送交付邮件 |
| 实时触发 | 小服 (CSM) | 处理客户反馈，归档或退回生产 |
| 每月 1 日 09:00 | 财务脚本 | 生成月度财务报告 |
| 每周一 02:00 | 龙虾军团 (KO) | Auto Dream 记忆巩固与技能进化 |

---

*本文档是 OPC Phase 2 的核心交付物，定义了公司层 4 个 Agent 的完整协作机制。*
