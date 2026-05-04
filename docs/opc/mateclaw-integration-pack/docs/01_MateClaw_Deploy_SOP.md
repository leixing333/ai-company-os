# MateClaw 部署与 OPC Agent 导入 SOP

**文档版本：** v1.0  
**适用版本：** MateClaw v1.2+  
**预计完成时间：** 约 60-90 分钟（首次部署）

---

## 概述

本文档是将 OPC 公司的 22 个数字员工（Agent）导入 MateClaw 多智能体操作系统的完整操作手册。完成后，你将拥有一个可以真正执行任务、相互协作的 AI 公司运营系统，并可通过 OPC Dashboard 进行可视化管理。

**完成后你将获得的能力：**

- 在 MateClaw 中向 CoS（幕僚长）发布任务，CoS 自动分解并委派给相应 Agent
- 所有需要 CEO 审批的决策会自动暂停，等待你在审批界面确认
- Scout 每天自动执行线索挖掘，Cron 任务无需人工触发
- 通过 OPC Dashboard 的 REST API 对接，实时可视化所有 Agent 的工作状态

---

## 第一步：环境准备

### 1.1 服务器要求

MateClaw 可以部署在以下环境中，推荐使用云服务器（如阿里云、腾讯云、AWS）：

| 配置项 | 最低要求 | 推荐配置 |
|---|---|---|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 磁盘 | 20 GB SSD | 50 GB SSD |
| 操作系统 | Ubuntu 20.04+ / CentOS 7+ | Ubuntu 22.04 LTS |
| 网络 | 能访问 OpenAI/Anthropic API | 境外服务器或有代理 |

**本地开发环境（Mac/Windows）** 同样可以部署，用于测试和验证。

### 1.2 安装 Docker 和 Docker Compose

```bash
# Ubuntu 系统
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo apt-get install docker-compose-plugin

# 验证安装
docker --version
docker compose version
```

### 1.3 准备 LLM API Key

MateClaw 支持多个 LLM 提供商，OPC 系统主要使用以下模型：

| Agent | 推荐模型 | API 提供商 |
|---|---|---|
| CoS、CTO、Strategist | claude-opus-4-5 | Anthropic |
| 其他 Agent | claude-3-5-sonnet-20241022 | Anthropic |
| 备用/降级 | gpt-4o | OpenAI |

**获取 API Key：**
- Anthropic：https://console.anthropic.com/settings/keys
- OpenAI：https://platform.openai.com/api-keys

---

## 第二步：部署 MateClaw

### 2.1 克隆代码仓库

```bash
git clone https://github.com/matevip/mateclaw.git
cd mateclaw
```

### 2.2 配置环境变量

复制示例配置文件并编辑：

```bash
cp .env.example .env
nano .env  # 或使用 vim .env
```

**必须配置的关键变量：**

```env
# ===== 数据库配置 =====
MYSQL_ROOT_PASSWORD=your_strong_password_here
MYSQL_DATABASE=mateclaw
MYSQL_USER=mateclaw
MYSQL_PASSWORD=your_db_password_here

# ===== JWT 密钥（随机生成，长度至少32位）=====
JWT_SECRET=your_random_jwt_secret_at_least_32_chars

# ===== 管理员账号 =====
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password

# ===== LLM API Keys =====
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-openai-key-here

# ===== 服务端口 =====
SERVER_PORT=8080

# ===== 应用域名（部署到服务器时填写）=====
APP_DOMAIN=https://your-domain.com
# 本地开发时使用：
# APP_DOMAIN=http://localhost:8080
```

### 2.3 启动服务

```bash
# 启动所有服务（后台运行）
docker compose up -d

# 查看启动日志
docker compose logs -f mateclaw-server

# 等待看到以下输出表示启动成功：
# Started MateClaw Application in X.XXX seconds
```

### 2.4 验证部署

打开浏览器访问：`http://localhost:8080`（或你的服务器 IP）

使用 `.env` 中配置的管理员账号登录，看到控制台界面即表示部署成功。

---

## 第三步：创建工作空间

MateClaw 使用"工作空间"来隔离不同团队的 Agent，对应 OPC 的四大团队。

### 3.1 登录后进入"工作空间管理"

在左侧导航栏找到 **工作空间** → **新建工作空间**，按以下顺序创建 6 个工作空间：

| 工作空间名称 | 描述 | 图标 |
|---|---|---|
| 公司层 (Company) | 人类 CEO 的角色定义 | 🏢 |
| 战略层 (Strategy) | 公司战略规划和方向制定 | 🎯 |
| 市场营销团队 (Marketing) | 线索挖掘、内容营销、销售转化 | 📢 |
| 生产研发团队 (Production) | 产品开发、技术实现、质量保证 | ⚙️ |
| 设计团队 (Design) | 品牌设计、UI/UX、内容创作 | 🎨 |
| 客户运营团队 (Operations) | 客户成功、用户服务 | 👥 |

---

## 第四步：导入数字员工（Agent）

### 4.1 导入顺序（重要！）

必须按以下顺序导入，因为下级 Agent 的委派规则依赖上级 Agent 的存在：

```
第1批（公司层）：CEO
第2批（战略层）：Strategist
第3批（生产核心）：CoS → CTO
第4批（生产执行）：FE, BE, QA, Researcher, KO, Ops
第5批（市场团队）：Scout, Broadcaster, Closer
第6批（设计团队）：CDO → Designer, Brand, Copywriter, Planner, PM, DesignOps, Design Researcher
第7批（运营团队）：CSM
```

### 4.2 手动导入方法（推荐首次使用）

在 MateClaw 控制台中，进入 **数字员工** → **新建数字员工**，按照 `opc_agents_import.json` 文件中每个 Agent 的字段逐一填写：

**以 CoS（幕僚长）为例：**

1. **基本信息**
   - 名称：`CoS（幕僚长）`
   - 角色：`Chief of Staff / Product Manager`
   - 头像：选择 🎯 或上传自定义图标
   - 所属工作空间：`生产研发团队 (Production)`

2. **模型配置**
   - 模型：`claude-opus-4-5`（或 `claude-3-5-sonnet-20241022` 作为备用）
   - 最大迭代次数：`20`
   - 温度：`0.7`

3. **角色设定（最关键的部分）**
   
   将 `opc_agents_import.json` 中 `agent_cos` 的 `system_prompt` 字段内容完整粘贴到"系统提示词"输入框中。

4. **工具配置**
   
   根据 `tools` 字段，在工具列表中勾选对应工具：
   - `web_search` → 网络搜索
   - `file_read` / `file_write` → 文件读写
   - `delegate_to_agent` → Agent 委派（必须开启）

5. **审批设置**
   
   `approval_required: true` → 开启"需要审批"，并在审批条件中填写：`预算超过500元、新客户签约、产品方向变更`

6. 点击**保存**

### 4.3 使用 API 批量导入（进阶）

如果已经配置好 OPC Dashboard 的 API 对接，可以使用 `scripts/import_agents.py` 脚本批量导入：

```bash
# 安装依赖
pip install requests

# 配置 MateClaw 连接信息
export MATECLAW_URL=http://localhost:8080
export MATECLAW_USERNAME=admin
export MATECLAW_PASSWORD=your_admin_password

# 执行批量导入
python scripts/import_agents.py
```

---

## 第五步：配置工具和知识库

### 5.1 配置 MCP 工具

MateClaw 支持 MCP（Model Context Protocol）工具扩展。OPC 系统推荐配置以下工具：

**网络搜索工具（Scout、Researcher 必需）：**

进入 **工具管理** → **添加工具** → 选择 `SearXNG`（自托管搜索）或 `Tavily`（付费搜索 API）

```env
# 如果使用 Tavily
TAVILY_API_KEY=tvly-your-key-here
```

**文件系统工具（CoS、KO 必需）：**

配置允许 Agent 读写的目录路径，建议映射到 `ai-company-os` 目录：

```yaml
# 在 docker-compose.yml 中添加卷映射
volumes:
  - /path/to/ai-company-os:/workspace/ai-company-os
```

### 5.2 上传知识库文件

进入 **知识库** → **新建知识库** → 上传以下文件：

| 知识库名称 | 上传文件 | 用途 |
|---|---|---|
| OPC 公司规范 | `1_company/` 目录下所有 .md 文件 | 公司文化、工作原则 |
| OPC 工作流程 | `3_production/shared/` 目录下所有文件 | 状态机、Brief 模板 |
| OPC 技能库 | `skills/` 目录下所有 SKILL.md | Agent 技能参考 |

---

## 第六步：测试验证

### 6.1 发送第一个任务

在 MateClaw 的 Chat 界面中，选择 **CoS（幕僚长）** 作为对话对象，发送以下测试消息：

```
你好，CoS。请帮我分析一下我们公司目前的市场定位，并给出下周的工作计划建议。
```

**预期行为：**
1. CoS 回复并请求确认工作计划（不会直接执行，会先询问）
2. 你确认后，CoS 开始分解任务
3. 如果需要市场研究，CoS 会委派给 Researcher
4. 最终汇总结果返回给你

### 6.2 测试审批流程

发送一个需要审批的任务：

```
CoS，请帮我起草一封给潜在客户的销售邮件，准备发送给上周 Scout 找到的那个线索。
```

**预期行为：**
1. CoS 委派给 Closer 起草邮件
2. Closer 完成草稿后，系统自动创建审批请求
3. 你会在 MateClaw 的**审批中心**看到待处理的审批
4. 你审批通过后，邮件才会被标记为"可发送"

### 6.3 测试 Cron 任务

进入 **定时任务** → **新建任务**，配置 Scout 的每日自动执行：

```
任务名称：Scout 每日线索挖掘
执行 Agent：Scout（小探）
Cron 表达式：0 9 * * 1-5  （工作日早上 9 点）
任务描述：从 Product Hunt、LinkedIn、Twitter、Hacker News 抓取今日高质量线索
```

---

## 第七步：连接 OPC Dashboard

完成以上步骤后，MateClaw 已经可以独立运行。下一步是将 OPC Dashboard 与 MateClaw 的 REST API 对接，实现可视化管理。

详细的 API 对接代码请参考：`api/` 目录下的文件：
- `api/mateclaw_client.py`：Python 版本 API 客户端
- `api/mateclaw_client.ts`：TypeScript 版本 API 客户端
- `api/README.md`：API 对接说明

---

## 常见问题排查

**Q：Docker 启动后访问不了界面？**

检查防火墙是否开放了 8080 端口：
```bash
sudo ufw allow 8080
# 或云服务器的安全组规则中添加 8080 端口
```

**Q：Agent 调用 LLM 时报错 "API Key Invalid"？**

检查 `.env` 文件中的 API Key 格式是否正确，Anthropic 的 Key 以 `sk-ant-` 开头，OpenAI 的 Key 以 `sk-` 开头。

**Q：Agent 委派失败，提示"找不到目标 Agent"？**

确认被委派的 Agent 已经在同一个工作空间中创建，且 Agent 名称与委派规则中的名称完全一致。

**Q：审批请求没有出现？**

检查 Agent 的"审批设置"是否已开启，以及触发审批的条件是否与任务内容匹配。

---

## 参考资料

- [MateClaw 官方文档](https://claw.mate.vip/docs/zh/intro.html)
- [MateClaw GitHub 仓库](https://github.com/matevip/mateclaw)
- [MateClaw 安全与审批文档](https://claw.mate.vip/docs/zh/security.html)
- [MateClaw 工作空间文档](https://claw.mate.vip/docs/zh/workspaces.html)
