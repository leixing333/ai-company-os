# OPC × MateClaw 对接包

**版本：** v1.0  
**适用：** MateClaw v1.2+ | OPC ai-company-os  
**用途：** 将 OPC 公司的 22 个数字员工导入 MateClaw，实现真正可执行的多智能体协作

---

## 目录结构

```
mateclaw-integration-pack/
├── README.md                          # 本文件（总览）
├── agents/
│   └── opc_agents_import.json         # 22 个 OPC 数字员工的完整定义文件
├── api/
│   ├── mateclaw_client.py             # Python API 客户端（后端/脚本使用）
│   ├── mateclaw_client.ts             # TypeScript API 客户端（OPC Dashboard 使用）
│   └── README.md                      # API 对接详细说明
├── docs/
│   └── 01_MateClaw_Deploy_SOP.md      # 从零部署到导入 Agent 的完整操作手册
└── scripts/
    └── import_agents.py               # 批量导入 Agent 的命令行脚本
```

---

## 快速开始

### 第一步：部署 MateClaw

参考 `docs/01_MateClaw_Deploy_SOP.md`，完成 MateClaw 的 Docker 部署。

预计时间：30-60 分钟（首次部署）

### 第二步：批量导入 OPC 数字员工

```bash
# 安装依赖
pip install requests

# 执行导入（替换为你的实际配置）
python scripts/import_agents.py \
    --url http://your-mateclaw-server:8080 \
    --username admin \
    --password your_password
```

### 第三步：验证导入结果

登录 MateClaw 控制台，在"数字员工"页面确认 22 个 Agent 已正确创建。

### 第四步：发送第一个任务

在 MateClaw Chat 界面，选择 **CoS（幕僚长）**，发送：

```
你好，CoS。请帮我规划本周的工作重点，并给出行动建议。
```

### 第五步：连接 OPC Dashboard

将 `api/mateclaw_client.ts` 集成到 OPC Dashboard 项目中，参考 `api/README.md`。

---

## 22 个数字员工清单

| 层级 | Agent 名称 | 角色 | 工作空间 |
|---|---|---|---|
| 公司层 | CEO（人类决策者）| 最高决策者 | 公司层 |
| 战略层 | Strategist（战略官）| 战略规划 | 战略层 |
| 生产核心 | CoS（幕僚长）| 调度中心 | 生产研发 |
| 生产核心 | CTO（技术总监）| 技术决策 | 生产研发 |
| 生产执行 | FE（前端工程师）| 前端开发 | 生产研发 |
| 生产执行 | BE（后端工程师）| 后端开发 | 生产研发 |
| 生产执行 | QA（质量保证）| 质量测试 | 生产研发 |
| 生产执行 | Researcher（研究员）| 市场研究 | 生产研发 |
| 生产执行 | KO（知识管理员）| 知识沉淀 | 生产研发 |
| 生产执行 | Ops（运维安全）| 系统运维 | 生产研发 |
| 市场团队 | Scout（小探）| 线索挖掘 | 市场营销 |
| 市场团队 | Broadcaster（小播）| 内容营销 | 市场营销 |
| 市场团队 | Closer（小销）| 销售转化 | 市场营销 |
| 设计团队 | CDO（设计总监）| 设计管理 | 设计团队 |
| 设计团队 | Designer（UI/UX）| 界面设计 | 设计团队 |
| 设计团队 | Brand（品牌设计师）| 品牌视觉 | 设计团队 |
| 设计团队 | Copywriter（文案）| 文案创作 | 设计团队 |
| 设计团队 | Planner（规划师）| 项目规划 | 设计团队 |
| 设计团队 | PM（项目经理）| 项目协调 | 设计团队 |
| 设计团队 | DesignOps（设计运营）| 效率优化 | 设计团队 |
| 设计团队 | Design Researcher | 用户研究 | 设计团队 |
| 运营团队 | CSM（小服）| 客户成功 | 客户运营 |

---

## 审批机制说明

以下 Agent 的操作需要 CEO 审批，对应 OPC 的 Escalation 机制：

| Agent | 触发审批的条件 |
|---|---|
| CoS | 预算超过 500 元、新客户签约、产品方向变更 |
| Closer | 所有对外邮件和合同 |
| Broadcaster | 发布到外部平台的内容 |
| CSM | 退款、补偿、重大承诺 |
| Ops | 生产环境变更 |
| CTO | 重大架构变更 |

---

## 注意事项

1. **API Key 费用**：22 个 Agent 使用 Claude Opus 和 Sonnet 模型，请确保 Anthropic 账户有足够余额。
2. **网络要求**：MateClaw 服务器需要能访问 Anthropic/OpenAI API，中国大陆服务器需要配置代理。
3. **数据安全**：`opc_agents_import.json` 包含完整的 System Prompt，请妥善保管，不要公开分享。
4. **版本兼容**：本对接包基于 MateClaw v1.2 API，如版本升级请参考官方文档更新 API 调用。
