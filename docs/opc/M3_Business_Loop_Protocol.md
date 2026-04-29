# M3: OPC 商业闭环四引擎完整运行协议 (Business Loop Protocol)

本模块定义了 OPC 商业闭环中，四个引擎（流量、转化、生产、交付）如何通过**状态机**和**结构化数据契约**进行无缝衔接，实现"一句话触发，全自动运转"的商业闭环。

---

## 1. 核心设计理念：状态机驱动 (State Machine Driven)

在 OPC 架构中，Agent 之间**不通过自然语言对话来交接任务**。所有协作均由一个全局的 JSON 状态机（`status.json`）驱动。每个 Agent 像流水线上的工人，只监控特定的状态，当状态符合自己的触发条件时，开始工作；工作完成后，更新状态，触发下一个 Agent。

### 1.1 全局状态定义 (Global States)

| 状态码 | 含义 | 负责引擎 | 负责 Agent |
|---|---|---|---|
| `LEAD_GENERATED` | 发现潜在客户线索 | 流量引擎 | 小探 (Scout) |
| `CONTACTED` | 已发送冷邮件/私信 | 转化引擎 | 小销 (Closer) |
| `NEGOTIATING` | 客户回复，正在沟通需求与报价 | 转化引擎 | 小销 (Closer) |
| `PAYMENT_RECEIVED` | 客户已付款，需求已确认 | 转化引擎 | 小销 (Closer) |
| `PRODUCTION_STARTED` | 生产引擎已接单，开始执行 | 生产引擎 | CoS / 小管 |
| `DESIGNING` | 设计团队正在出图 | 生产引擎 | 设计团队 |
| `DEVELOPING` | 开发团队正在编码 | 生产引擎 | 开发团队 |
| `TESTING` | QA 正在进行质量验收 | 生产引擎 | QA |
| `READY_FOR_DELIVERY` | 生产完成，交付物已就绪 | 生产引擎 | Ops / 小运 |
| `DELIVERED` | 已发送给客户，等待反馈 | 交付引擎 | 小服 (CSM) |
| `COMPLETED` | 客户确认满意，项目归档 | 交付引擎 | 小服 (CSM) |
| `ESCALATED` | 遇到异常，等待 CEO 介入 | 全局 | CEO (人类) |

---

## 2. 引擎间数据契约 (Data Contracts)

为了确保数据在引擎间流转时不丢失、不产生幻觉，必须使用严格的 JSON/Markdown 契约格式。

### 2.1 流量引擎 -> 转化引擎：`LEAD_SCHEMA.json`
小探 (Scout) 抓取到线索后，必须按此格式写入 `2_marketing/leads/` 目录，触发小销 (Closer)。

```json
{
  "lead_id": "L-20251024-001",
  "source": "Product Hunt",
  "company_name": "AI Startup X",
  "contact_email": "founder@startupx.com",
  "pain_point_analysis": "产品刚上线，但落地页转化率极低，设计粗糙。",
  "estimated_budget": "$1000 - $3000",
  "conversion_probability": 8,
  "status": "LEAD_GENERATED"
}
```

### 2.2 转化引擎 -> 生产引擎：`PROJECT_BRIEF.md`
客户付款后，小销 (Closer) 必须将沟通记录转化为标准化的需求文档，写入 `3_production/active_projects/{Project_ID}/brief.md`，并更新状态为 `PAYMENT_RECEIVED`。

```markdown
# Project Brief: Client A Landing Page
**Project ID**: P-20251025-001
**Client**: AI Startup X
**Budget**: $2999 (Paid via Stripe)
**Deadline**: 2025-10-28 12:00 UTC

## 1. 核心需求 (Core Requirements)
- 重新设计并开发高转化率的 SaaS 落地页。
- 必须包含：Hero Section, How it Works, Pricing, FAQ。

## 2. 品牌资产 (Brand Assets)
- Logo URL: https://...
- 主色调: #4F46E5 (Indigo)

## 3. 验收标准 (Success Criteria)
- 设计稿通过小牌 (Brand) 审核。
- 前端代码通过 QA 测试，Lighthouse 跑分 > 90。
- 部署到 Vercel 并绑定自定义域名。
```

### 2.3 生产引擎 -> 交付引擎：`DELIVERY_MANIFEST.json`
生产完成后，Ops 或小运将最终产物放入 `4_operations/deliverables/{Project_ID}/`，并生成此清单，触发小服 (CSM)。

```json
{
  "project_id": "P-20251025-001",
  "status": "READY_FOR_DELIVERY",
  "assets": [
    {
      "type": "design_source",
      "path": "deliverables/P-20251025-001/figma_export.zip"
    },
    {
      "type": "live_url",
      "url": "https://client-a-landing.vercel.app"
    }
  ],
  "release_notes": "落地页已成功部署，Lighthouse 性能评分 98。"
}
```

---

## 3. 商业闭环完整运转流程 (The Loop in Action)

以下是一个完整的商业闭环运转实例（以"产品化 AI 设计服务"为例）：

### 步骤 1：获客 (Traffic)
1. **触发**：每天早上 8:00，定时任务唤醒**小探 (Scout)**。
2. **执行**：小探扫描 Product Hunt，发现 5 个设计粗糙的新产品，生成 5 份 `LEAD_SCHEMA.json`，状态设为 `LEAD_GENERATED`。

### 步骤 2：销售 (Sales)
1. **触发**：**小销 (Closer)** 监控到新的 `LEAD_GENERATED` 状态。
2. **执行**：小销读取痛点分析，调用邮件 API 发送定制化的冷邮件（包含痛点指出和我们的 $999 落地页重构套餐链接），状态更新为 `CONTACTED`。
3. **转化**：客户回复邮件询问细节，小销自动回复并解答。客户点击 Stripe 链接完成支付。
4. **交接**：Stripe Webhook 触发小销，小销生成 `PROJECT_BRIEF.md`，在 `active_projects/` 建档，状态更新为 `PAYMENT_RECEIVED`。

### 步骤 3：生产 (Production)
1. **触发**：**CoS (幕僚长)** 和 **小管 (PM)** 监控到 `PAYMENT_RECEIVED`。
2. **执行 (设计)**：小管接单，状态更新为 `DESIGNING`。小策出线框图 -> 小设出视觉稿 -> 小文写文案 -> 小牌审核。设计资产存入 `shared_workspace/design_handoffs/`。
3. **执行 (开发)**：CoS 接单，状态更新为 `DEVELOPING`。FE 读取设计资产进行编码 -> BE 写接口 -> QA 测试 (`TESTING`) -> Ops 部署上线。
4. **交接**：Ops 将源码和线上链接打包放入 `4_operations/deliverables/`，生成 `DELIVERY_MANIFEST.json`，状态更新为 `READY_FOR_DELIVERY`。

### 步骤 4：交付与复购 (Delivery & Retention)
1. **触发**：**小服 (CSM)** 监控到 `READY_FOR_DELIVERY`。
2. **执行**：小服读取清单，撰写热情洋溢的交付邮件，附带源码下载链接和线上预览地址，发送给客户。状态更新为 `DELIVERED`。
3. **反馈**：3 天后，小服自动发送跟进邮件询问满意度（NPS）。如果客户满意，小服会顺势推销"每月 $499 的持续维护套餐"；如果客户提出修改意见，小服将意见整理为新的 `brief.md`，状态回退至 `PRODUCTION_STARTED`。

---

## 4. 异常处理与人类在环 (Human-in-the-loop)

在上述全自动闭环中，为了控制风险，必须在以下节点设置**硬性拦截（Hard Stops）**，等待 CEO 审批：

1. **大额报价审批**：当小销准备发送超过 $5000 的定制报价单时。
2. **退款请求**：当客户在邮件中提到 "refund", "cancel", "unhappy" 等负面词汇时。
3. **生产超时**：当项目停留在 `DESIGNING` 或 `DEVELOPING` 状态超过 48 小时未推进时。
4. **API 成本超标**：当 `finance_tracker.csv` 显示单日 API 消耗超过 $50 时。

当触发拦截时，系统状态变为 `ESCALATED`，并在 `1_strategy/ESCALATIONS/` 生成报警文件，等待 CEO 处理。

*本模块定义了 OPC 的商业运转血液。下一模块 (M4) 将解决支撑这套血液循环的 10 个底层技术难题。*
