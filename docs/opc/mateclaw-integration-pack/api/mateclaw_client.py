"""
MateClaw REST API Python 客户端
用于 OPC Dashboard 与 MateClaw 的数据对接

依赖安装：pip install requests python-dotenv
使用方法：
    from mateclaw_client import MateClawClient
    client = MateClawClient(base_url="http://localhost:8080", username="admin", password="xxx")
    agents = client.list_agents()
"""

import os
import json
import time
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    raise ImportError("请先安装依赖：pip install requests")

logger = logging.getLogger(__name__)


class MateClawAPIError(Exception):
    """MateClaw API 调用异常"""
    def __init__(self, status_code: int, message: str, response_body: dict = None):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body or {}
        super().__init__(f"[{status_code}] {message}")


class MateClawClient:
    """
    MateClaw REST API 客户端
    
    支持功能：
    - JWT 认证（自动续签）
    - Agent 管理（列表、详情、状态）
    - 任务管理（创建、查询、审批）
    - 工作空间管理
    - 日志查询
    """

    def __init__(
        self,
        base_url: str = None,
        username: str = None,
        password: str = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self.base_url = (base_url or os.getenv("MATECLAW_URL", "http://localhost:8080")).rstrip("/")
        self.username = username or os.getenv("MATECLAW_USERNAME", "admin")
        self.password = password or os.getenv("MATECLAW_PASSWORD", "")
        self.timeout = timeout
        self._token: Optional[str] = None
        self._token_expires_at: float = 0

        # 配置带重试的 HTTP Session
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    # =========================================================================
    # 认证
    # =========================================================================

    def _ensure_token(self) -> str:
        """确保 JWT Token 有效，过期则自动刷新"""
        if self._token and time.time() < self._token_expires_at - 60:
            return self._token
        return self._login()

    def _login(self) -> str:
        """登录获取 JWT Token"""
        url = f"{self.base_url}/api/v1/auth/login"
        payload = {"username": self.username, "password": self.password}
        try:
            resp = self.session.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self._token = data.get("data", {}).get("token") or data.get("token")
            if not self._token:
                raise MateClawAPIError(200, "登录响应中未找到 token 字段", data)
            # MateClaw 默认 token 有效期 24 小时
            self._token_expires_at = time.time() + 23 * 3600
            logger.info("MateClaw 登录成功")
            return self._token
        except requests.RequestException as e:
            raise MateClawAPIError(0, f"登录请求失败: {e}")

    def _headers(self) -> dict:
        """构建带认证的请求头"""
        return {
            "Authorization": f"Bearer {self._ensure_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """统一 HTTP 请求方法"""
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        kwargs["headers"] = self._headers()
        try:
            resp = self.session.request(method, url, **kwargs)
            if resp.status_code == 401:
                # Token 失效，重新登录后重试
                self._token = None
                kwargs["headers"] = self._headers()
                resp = self.session.request(method, url, **kwargs)
            if not resp.ok:
                try:
                    body = resp.json()
                except Exception:
                    body = {"raw": resp.text}
                raise MateClawAPIError(resp.status_code, body.get("message", resp.reason), body)
            return resp.json()
        except requests.RequestException as e:
            raise MateClawAPIError(0, f"请求失败: {e}")

    # =========================================================================
    # 工作空间
    # =========================================================================

    def list_workspaces(self) -> List[Dict]:
        """获取所有工作空间列表"""
        data = self._request("GET", "/api/v1/workspaces")
        return data.get("data", {}).get("list", data.get("data", []))

    def get_workspace(self, workspace_id: str) -> Dict:
        """获取工作空间详情"""
        data = self._request("GET", f"/api/v1/workspaces/{workspace_id}")
        return data.get("data", {})

    def create_workspace(self, name: str, description: str = "", icon: str = "") -> Dict:
        """创建工作空间"""
        payload = {"name": name, "description": description, "icon": icon}
        data = self._request("POST", "/api/v1/workspaces", json=payload)
        return data.get("data", {})

    # =========================================================================
    # Agent（数字员工）
    # =========================================================================

    def list_agents(self, workspace_id: str = None, page: int = 1, page_size: int = 50) -> Dict:
        """
        获取 Agent 列表
        
        返回格式：
        {
            "list": [...],
            "total": 22,
            "page": 1,
            "page_size": 50
        }
        """
        params = {"page": page, "pageSize": page_size}
        if workspace_id:
            params["workspaceId"] = workspace_id
        data = self._request("GET", "/api/v1/agents", params=params)
        return data.get("data", {})

    def get_agent(self, agent_id: str) -> Dict:
        """获取 Agent 详情（包含 SOUL 配置）"""
        data = self._request("GET", f"/api/v1/agents/{agent_id}")
        return data.get("data", {})

    def get_agent_status(self, agent_id: str) -> Dict:
        """
        获取 Agent 实时状态
        
        返回格式：
        {
            "agent_id": "xxx",
            "status": "idle" | "running" | "waiting_approval" | "error",
            "current_task_id": "xxx" | null,
            "last_active_at": "2026-05-05T10:00:00Z",
            "token_usage_today": 12500
        }
        """
        data = self._request("GET", f"/api/v1/agents/{agent_id}/status")
        return data.get("data", {})

    def list_all_agent_statuses(self) -> List[Dict]:
        """获取所有 Agent 的实时状态（用于 OPC Dashboard 星系视图）"""
        agents_data = self.list_agents(page_size=100)
        agents = agents_data.get("list", [])
        statuses = []
        for agent in agents:
            try:
                status = self.get_agent_status(agent["id"])
                status["name"] = agent.get("name", "")
                status["workspace_id"] = agent.get("workspaceId", "")
                status["role"] = agent.get("role", "")
                statuses.append(status)
            except MateClawAPIError as e:
                logger.warning(f"获取 Agent {agent['id']} 状态失败: {e}")
        return statuses

    def create_agent(self, agent_config: Dict) -> Dict:
        """
        创建 Agent（数字员工）
        
        agent_config 字段参考 opc_agents_import.json 中的 agent 对象
        """
        # 字段映射：OPC 格式 → MateClaw API 格式
        payload = {
            "name": agent_config.get("name"),
            "role": agent_config.get("role"),
            "description": agent_config.get("description"),
            "goal": agent_config.get("goal"),
            "backstory": agent_config.get("backstory"),
            "systemPrompt": agent_config.get("system_prompt"),
            "model": agent_config.get("model", "claude-3-5-sonnet-20241022"),
            "workspaceId": agent_config.get("workspace_id"),
            "tools": agent_config.get("tools", []),
            "approvalRequired": agent_config.get("approval_required", False),
            "approvalThreshold": agent_config.get("approval_threshold", ""),
            "maxIterations": agent_config.get("max_iterations", 20),
            "tags": agent_config.get("tags", []),
        }
        data = self._request("POST", "/api/v1/agents", json=payload)
        return data.get("data", {})

    def batch_import_agents(self, import_file_path: str) -> Dict:
        """
        从 opc_agents_import.json 批量导入所有 Agent
        
        返回：{"success": [...], "failed": [...]}
        """
        with open(import_file_path, "r", encoding="utf-8") as f:
            import_data = json.load(f)

        # 先创建工作空间
        workspace_map = {}
        existing_workspaces = {ws["name"]: ws["id"] for ws in self.list_workspaces()}
        for ws in import_data.get("workspaces", []):
            if ws["name"] not in existing_workspaces:
                created = self.create_workspace(ws["name"], ws.get("description", ""))
                workspace_map[ws["id"]] = created["id"]
                logger.info(f"创建工作空间: {ws['name']}")
            else:
                workspace_map[ws["id"]] = existing_workspaces[ws["name"]]
                logger.info(f"工作空间已存在: {ws['name']}")

        # 按顺序导入 Agent
        results = {"success": [], "failed": []}
        for agent in import_data.get("agents", []):
            # 替换 workspace_id 为实际 ID
            agent["workspace_id"] = workspace_map.get(agent.get("workspace_id"), agent.get("workspace_id"))
            try:
                created = self.create_agent(agent)
                results["success"].append({"name": agent["name"], "id": created.get("id")})
                logger.info(f"导入 Agent 成功: {agent['name']}")
            except MateClawAPIError as e:
                results["failed"].append({"name": agent["name"], "error": str(e)})
                logger.error(f"导入 Agent 失败: {agent['name']} - {e}")

        return results

    # =========================================================================
    # 任务管理
    # =========================================================================

    def create_task(
        self,
        agent_id: str,
        content: str,
        title: str = "",
        context: Dict = None,
        priority: str = "normal",
    ) -> Dict:
        """
        向指定 Agent 发布任务
        
        参数：
            agent_id: 目标 Agent ID（通常是 CoS 的 ID）
            content: 任务内容（自然语言描述）
            title: 任务标题（可选）
            context: 附加上下文（如关联的 brief.md 内容）
            priority: 优先级 "low" | "normal" | "high" | "urgent"
        
        返回：
        {
            "task_id": "xxx",
            "status": "pending",
            "created_at": "2026-05-05T10:00:00Z"
        }
        """
        payload = {
            "agentId": agent_id,
            "title": title or content[:50],
            "content": content,
            "context": context or {},
            "priority": priority,
        }
        data = self._request("POST", "/api/v1/tasks", json=payload)
        return data.get("data", {})

    def get_task(self, task_id: str) -> Dict:
        """获取任务详情"""
        data = self._request("GET", f"/api/v1/tasks/{task_id}")
        return data.get("data", {})

    def list_tasks(
        self,
        agent_id: str = None,
        status: str = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict:
        """
        获取任务列表
        
        status 可选值：pending | running | waiting_approval | completed | failed | cancelled
        """
        params = {"page": page, "pageSize": page_size}
        if agent_id:
            params["agentId"] = agent_id
        if status:
            params["status"] = status
        data = self._request("GET", "/api/v1/tasks", params=params)
        return data.get("data", {})

    def cancel_task(self, task_id: str, reason: str = "") -> Dict:
        """取消任务"""
        payload = {"reason": reason}
        data = self._request("POST", f"/api/v1/tasks/{task_id}/cancel", json=payload)
        return data.get("data", {})

    def get_task_logs(self, task_id: str) -> List[Dict]:
        """获取任务执行日志（对应 KAIROS 日志）"""
        data = self._request("GET", f"/api/v1/tasks/{task_id}/logs")
        return data.get("data", {}).get("list", [])

    # =========================================================================
    # 审批管理（Escalation）
    # =========================================================================

    def list_pending_approvals(self) -> List[Dict]:
        """
        获取所有待审批的请求（对应 OPC 的 Escalation 机制）
        
        返回格式：
        [
            {
                "approval_id": "xxx",
                "task_id": "xxx",
                "agent_name": "CoS（幕僚长）",
                "reason": "预算超过500元",
                "content": "申请购买 xxx 服务，费用 800 元",
                "created_at": "2026-05-05T10:00:00Z"
            }
        ]
        """
        data = self._request("GET", "/api/v1/approvals", params={"status": "pending"})
        return data.get("data", {}).get("list", [])

    def approve(self, approval_id: str, comment: str = "CEO 已审批") -> Dict:
        """审批通过"""
        payload = {"action": "approve", "comment": comment}
        data = self._request("POST", f"/api/v1/approvals/{approval_id}/review", json=payload)
        return data.get("data", {})

    def reject(self, approval_id: str, reason: str) -> Dict:
        """审批拒绝"""
        payload = {"action": "reject", "comment": reason}
        data = self._request("POST", f"/api/v1/approvals/{approval_id}/review", json=payload)
        return data.get("data", {})

    # =========================================================================
    # 系统统计（用于 OPC Dashboard 大盘）
    # =========================================================================

    def get_dashboard_stats(self) -> Dict:
        """
        获取系统统计数据（用于 OPC Dashboard 指挥大盘）
        
        返回格式：
        {
            "total_agents": 22,
            "active_agents": 5,
            "tasks_today": 18,
            "tasks_completed_today": 12,
            "pending_approvals": 2,
            "token_usage_today": 125000,
            "token_usage_this_month": 1250000
        }
        """
        data = self._request("GET", "/api/v1/dashboard/stats")
        return data.get("data", {})

    def get_activity_feed(self, limit: int = 20) -> List[Dict]:
        """获取最近活动流（用于 OPC Dashboard 活动流组件）"""
        data = self._request("GET", "/api/v1/activities", params={"limit": limit})
        return data.get("data", {}).get("list", [])

    # =========================================================================
    # Cron 定时任务
    # =========================================================================

    def list_cron_tasks(self) -> List[Dict]:
        """获取所有定时任务"""
        data = self._request("GET", "/api/v1/cron-tasks")
        return data.get("data", {}).get("list", [])

    def create_cron_task(
        self,
        name: str,
        agent_id: str,
        cron_expression: str,
        task_content: str,
        enabled: bool = True,
    ) -> Dict:
        """
        创建定时任务
        
        示例（Scout 每日执行）：
            create_cron_task(
                name="Scout 每日线索挖掘",
                agent_id="agent_scout_id",
                cron_expression="0 9 * * 1-5",
                task_content="从 Product Hunt、LinkedIn、Twitter、Hacker News 抓取今日高质量线索"
            )
        """
        payload = {
            "name": name,
            "agentId": agent_id,
            "cronExpression": cron_expression,
            "taskContent": task_content,
            "enabled": enabled,
        }
        data = self._request("POST", "/api/v1/cron-tasks", json=payload)
        return data.get("data", {})


# =============================================================================
# 批量导入脚本入口
# =============================================================================

def main():
    """批量导入 OPC 数字员工到 MateClaw"""
    import argparse

    parser = argparse.ArgumentParser(description="OPC Agent 批量导入工具")
    parser.add_argument("--url", default=os.getenv("MATECLAW_URL", "http://localhost:8080"), help="MateClaw 服务地址")
    parser.add_argument("--username", default=os.getenv("MATECLAW_USERNAME", "admin"), help="管理员用户名")
    parser.add_argument("--password", default=os.getenv("MATECLAW_PASSWORD", ""), help="管理员密码")
    parser.add_argument("--import-file", default="../agents/opc_agents_import.json", help="导入文件路径")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    client = MateClawClient(base_url=args.url, username=args.username, password=args.password)

    print("\n===== OPC Agent 批量导入工具 =====")
    print(f"目标服务器: {args.url}")
    print(f"导入文件: {args.import_file}")
    print("=" * 35)

    # 测试连接
    try:
        client._login()
        print("✅ 连接成功，开始导入...\n")
    except MateClawAPIError as e:
        print(f"❌ 连接失败: {e}")
        return

    # 执行批量导入
    import_file = os.path.join(os.path.dirname(__file__), args.import_file)
    results = client.batch_import_agents(import_file)

    print(f"\n===== 导入结果 =====")
    print(f"✅ 成功: {len(results['success'])} 个")
    for item in results["success"]:
        print(f"   - {item['name']} (ID: {item['id']})")

    if results["failed"]:
        print(f"\n❌ 失败: {len(results['failed'])} 个")
        for item in results["failed"]:
            print(f"   - {item['name']}: {item['error']}")

    print("\n导入完成！请登录 MateClaw 控制台验证结果。")


if __name__ == "__main__":
    main()
