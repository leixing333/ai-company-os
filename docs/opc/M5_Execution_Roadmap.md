# M5: OPC 分阶段开发路线图 (Execution Roadmap)

本模块将前四个模块的架构设计转化为具体的、可执行的开发任务清单。路线图分为 4 个阶段，每个阶段都有明确的里程碑和验收标准。

---

## Phase 1: 基础设施与目录重构 (The Foundation)

**目标**：建立 OPC 公司级操作系统（Company OS）的物理骨架，并将原有的龙虾军团安全降级为生产引擎。

| 任务编号 | 任务描述 | 执行命令/动作 | 验收标准 |
|---|---|---|---|
| **1.1** | 初始化 `ai-company-os` 根目录及四大核心目录 | `mkdir -p ai-company-os/{1_strategy,2_marketing,3_production,4_operations}` | 目录结构与 M1 规范完全一致。 |
| **1.2** | 迁移龙虾军团 | `cp -r opt-openclaw-v6 ai-company-os/3_production/infrastructure/lobster-legion` | 龙虾军团内部结构完整保留。 |
| **1.3** | 配置全局状态机与契约模板 | 在 `3_production/shared_workspace/` 下创建 `status.json` 和 `BRIEF_SCHEMA.json` | 文件格式符合 M3 规范。 |
| **1.4** | 调整龙虾军团路径配置 | 修改 `lobster-legion/config/openclaw.json`，将工作区路径指向上层的 `active_projects` | 龙虾军团能够正确读写上层目录。 |

**里程碑 1**：物理目录结构搭建完毕，龙虾军团在新的位置能够正常启动并读取外部任务。

---

## Phase 2: 公司层智能体开发 (The Front-Office)

**目标**：开发负责"搞钱"的 4 个全新 Agent，补齐商业闭环的流量、转化与交付引擎。

| 任务编号 | 任务描述 | 执行命令/动作 | 验收标准 |
|---|---|---|---|
| **2.1** | 开发小探 (Scout) | 编写 `2_marketing/agents/scout/AGENT_CARD.md` 和抓取脚本 | 能够成功抓取并生成 `LEAD_SCHEMA.json`。 |
| **2.2** | 开发小播 (Broadcaster) | 编写 `2_marketing/agents/broadcaster/AGENT_CARD.md` 和内容生成脚本 | 能够读取交付物并生成 Twitter 帖子草稿。 |
| **2.3** | 开发小销 (Closer) | 编写 `2_marketing/agents/closer/AGENT_CARD.md` 和邮件回复逻辑 | 能够根据线索生成冷邮件，并将客户回复转化为 `PROJECT_BRIEF.md`。 |
| **2.4** | 开发小服 (CSM) | 编写 `4_operations/agents/csm/AGENT_CARD.md` 和打包交付逻辑 | 能够监控 `READY_FOR_DELIVERY` 状态，打包文件并生成交付邮件。 |

**里程碑 2**：公司层 4 个 Agent 具备独立运行能力，能够按照 M2 规范读写指定目录。

---

## Phase 3: 生产层双团队协同协议 (The Back-Office)

**目标**：打通设计团队与开发团队的跨团队协作壁垒，确保生产引擎能够高效运转。

| 任务编号 | 任务描述 | 执行命令/动作 | 验收标准 |
|---|---|---|---|
| **3.1** | 制定设计交接规范 | 编写 `3_production/shared_workspace/DESIGN_HANDOFF_SPEC.md` | 明确规定设计资产的目录结构和命名规范。 |
| **3.2** | 更新小运 (Operations) 逻辑 | 修改设计团队小运的 Prompt，强制其按规范输出到 `shared_workspace` | 小运能够正确打包设计资产。 |
| **3.3** | 更新 FE (前端) 逻辑 | 修改开发团队 FE 的 Prompt，强制其从 `shared_workspace` 读取资产 | FE 能够正确读取设计资产并开始编码。 |
| **3.4** | 配置 Escalation 拦截器 | 在底层文件读写工具中加入权限校验逻辑 | 触发越权访问或超时时，能够正确生成报警文件并挂起进程。 |

**里程碑 3**：设计团队与开发团队能够通过 `shared_workspace` 无缝交接，生产引擎内部运转顺畅。

---

## Phase 4: 商业闭环联调测试 (The Loop Test)

**目标**：模拟一个真实的客户订单，跑通从获客到交付的全链路，验证商业闭环。

| 任务编号 | 任务描述 | 执行命令/动作 | 验收标准 |
|---|---|---|---|
| **4.1** | 模拟获客与销售 | 手动在 `2_marketing/leads/` 放入一个测试线索，触发小销 | 小销成功生成 `PROJECT_BRIEF.md`，状态变为 `PAYMENT_RECEIVED`。 |
| **4.2** | 模拟生产执行 | 唤醒生产引擎，监控 `status.json` 的状态流转 | 状态依次经历 `DESIGNING` -> `DEVELOPING` -> `TESTING` -> `READY_FOR_DELIVERY`。 |
| **4.3** | 模拟交付与反馈 | 监控小服 (CSM) 的动作 | 小服成功打包交付物，生成交付邮件，状态变为 `DELIVERED`。 |
| **4.4** | 财务与记忆沉淀 | 检查 `finance_tracker.csv` 和 `global_skills/` | 成功记录 API 成本，KO 成功提炼本次项目的 `SKILL.md`。 |

**里程碑 4**：商业闭环全链路跑通，OPC 公司级操作系统正式上线，准备迎接真实客户。

---
*至此，OPC 系统架构的 5 个核心模块已全部定义完毕。随时可以进入 Phase 1 开始编码。*
