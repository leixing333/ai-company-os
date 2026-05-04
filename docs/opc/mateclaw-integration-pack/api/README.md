# MateClaw API 对接说明

本目录包含 OPC Dashboard 与 MateClaw REST API 对接的完整代码，提供 Python 和 TypeScript 双版本。

---

## 文件说明

| 文件 | 用途 |
|---|---|
| `mateclaw_client.py` | Python 版本 API 客户端，用于批量导入 Agent 和后端脚本 |
| `mateclaw_client.ts` | TypeScript 版本 API 客户端，用于 OPC Dashboard 前端对接 |
| `README.md` | 本文档 |

---

## Python 客户端使用方法

### 安装依赖

```bash
pip install requests python-dotenv
```

### 基本使用

```python
from mateclaw_client import MateClawClient

# 初始化客户端
client = MateClawClient(
    base_url="http://localhost:8080",
    username="admin",
    password="your_password"
)

# 获取所有 Agent 状态
statuses = client.list_all_agent_statuses()
for s in statuses:
    print(f"{s['name']}: {s['status']}")

# 向 CoS 发布任务
task = client.create_task(
    agent_id="cos_agent_id",
    content="请分析本周的市场线索，给出跟进建议",
    priority="high"
)
print(f"任务已创建: {task['id']}")

# 查看待审批列表
approvals = client.list_pending_approvals()
for approval in approvals:
    print(f"待审批: {approval['agentName']} - {approval['reason']}")
    
# 审批通过
client.approve(approvals[0]['approvalId'], comment="CEO 审批通过")
```

### 批量导入 Agent

```bash
# 方法一：使用命令行脚本
cd scripts/
python import_agents.py \
    --url http://localhost:8080 \
    --username admin \
    --password your_password \
    --import-file ../agents/opc_agents_import.json

# 方法二：使用环境变量
export MATECLAW_URL=http://localhost:8080
export MATECLAW_USERNAME=admin
export MATECLAW_PASSWORD=your_password
python import_agents.py
```

---

## TypeScript 客户端使用方法

### 在 OPC Dashboard 中集成

**第一步：在项目中引入客户端**

将 `mateclaw_client.ts` 复制到 OPC Dashboard 项目的 `client/src/lib/` 目录下。

**第二步：初始化客户端**

在 `client/src/lib/mateclaw.ts` 中创建全局实例：

```typescript
import { initMateClawClient, MateClawClient } from './mateclaw_client';

// 从环境变量读取配置
export const mateClawClient = initMateClawClient({
  baseUrl: import.meta.env.VITE_MATECLAW_URL || 'http://localhost:8080',
  username: import.meta.env.VITE_MATECLAW_USERNAME || 'admin',
  password: import.meta.env.VITE_MATECLAW_PASSWORD || '',
  onTokenExpired: () => {
    // Token 过期时的处理（如跳转到登录页）
    window.location.href = '/login';
  }
});

// 登录
await mateClawClient.login(
  import.meta.env.VITE_MATECLAW_USERNAME,
  import.meta.env.VITE_MATECLAW_PASSWORD
);
```

**第三步：在 React 组件中使用**

```typescript
// DashboardView.tsx 中获取大盘数据
import { getMateClawClient } from '@/lib/mateclaw_client';

const DashboardView = () => {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    const client = getMateClawClient();
    client.getDashboardStats().then(setStats);
    
    // 每 30 秒刷新一次
    const interval = setInterval(() => {
      client.getDashboardStats().then(setStats);
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);
  
  // ...
};

// GalaxyView.tsx 中获取 Agent 状态
const GalaxyView = () => {
  const [agentStatuses, setAgentStatuses] = useState([]);
  
  useEffect(() => {
    const client = getMateClawClient();
    client.listAllAgentStatuses().then(setAgentStatuses);
  }, []);
  
  // ...
};

// 审批操作
const handleApprove = async (approvalId: string) => {
  const client = getMateClawClient();
  await client.approve(approvalId, 'CEO 审批通过');
  // 刷新列表
};
```

**第四步：配置环境变量**

在 OPC Dashboard 项目根目录创建 `.env.local`：

```env
VITE_MATECLAW_URL=http://localhost:8080
VITE_MATECLAW_USERNAME=admin
VITE_MATECLAW_PASSWORD=your_password
```

---

## API 端点速查表

| 功能 | 方法 | 端点 |
|---|---|---|
| 登录 | POST | `/api/v1/auth/login` |
| 工作空间列表 | GET | `/api/v1/workspaces` |
| Agent 列表 | GET | `/api/v1/agents` |
| Agent 状态 | GET | `/api/v1/agents/{id}/status` |
| 创建任务 | POST | `/api/v1/tasks` |
| 任务列表 | GET | `/api/v1/tasks` |
| 任务日志 | GET | `/api/v1/tasks/{id}/logs` |
| 待审批列表 | GET | `/api/v1/approvals?status=pending` |
| 审批操作 | POST | `/api/v1/approvals/{id}/review` |
| 大盘统计 | GET | `/api/v1/dashboard/stats` |
| 活动流 | GET | `/api/v1/activities` |
| 定时任务 | GET/POST | `/api/v1/cron-tasks` |

---

## 注意事项

1. **CORS 配置**：如果 OPC Dashboard 和 MateClaw 部署在不同域名，需要在 MateClaw 的配置中添加 CORS 允许域名。

2. **Token 管理**：JWT Token 默认有效期 24 小时，客户端会在过期前 1 分钟自动刷新。

3. **错误处理**：所有 API 调用都可能抛出 `MateClawAPIError`，建议在组件层面统一处理。

4. **API 版本**：本文档基于 MateClaw v1.2 API，如版本升级请参考官方 Changelog。
