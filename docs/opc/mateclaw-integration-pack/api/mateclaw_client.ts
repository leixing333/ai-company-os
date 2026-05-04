/**
 * MateClaw REST API TypeScript 客户端
 * 用于 OPC Dashboard 前端与 MateClaw 的数据对接
 *
 * 使用方法：
 *   import { MateClawClient } from './mateclaw_client';
 *   const client = new MateClawClient({ baseUrl: 'http://localhost:8080' });
 *   await client.login('admin', 'password');
 *   const agents = await client.listAgents();
 */

// =============================================================================
// 类型定义
// =============================================================================

export type AgentStatus = "idle" | "running" | "waiting_approval" | "error" | "offline";
export type TaskStatus = "pending" | "running" | "waiting_approval" | "completed" | "failed" | "cancelled";
export type TaskPriority = "low" | "normal" | "high" | "urgent";
export type ApprovalAction = "approve" | "reject";

export interface Workspace {
  id: string;
  name: string;
  description: string;
  icon: string;
  agentCount: number;
  createdAt: string;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  description: string;
  model: string;
  workspaceId: string;
  workspaceName: string;
  tags: string[];
  approvalRequired: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AgentStatusInfo {
  agentId: string;
  name: string;
  role: string;
  workspaceId: string;
  status: AgentStatus;
  currentTaskId: string | null;
  lastActiveAt: string;
  tokenUsageToday: number;
  tokenUsageThisMonth: number;
}

export interface Task {
  id: string;
  title: string;
  content: string;
  agentId: string;
  agentName: string;
  status: TaskStatus;
  priority: TaskPriority;
  context: Record<string, unknown>;
  result: string | null;
  createdAt: string;
  updatedAt: string;
  completedAt: string | null;
}

export interface TaskLog {
  id: string;
  taskId: string;
  agentId: string;
  agentName: string;
  type: "thought" | "action" | "observation" | "delegation" | "approval_request" | "result";
  content: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface ApprovalRequest {
  approvalId: string;
  taskId: string;
  agentId: string;
  agentName: string;
  reason: string;
  content: string;
  status: "pending" | "approved" | "rejected";
  createdAt: string;
  reviewedAt: string | null;
  reviewComment: string | null;
}

export interface DashboardStats {
  totalAgents: number;
  activeAgents: number;
  tasksToday: number;
  tasksCompletedToday: number;
  pendingApprovals: number;
  tokenUsageToday: number;
  tokenUsageThisMonth: number;
  estimatedCostToday: number;
  estimatedCostThisMonth: number;
}

export interface ActivityItem {
  id: string;
  type: "task_created" | "task_completed" | "task_failed" | "approval_requested" | "approval_resolved" | "agent_started" | "agent_stopped";
  agentId: string;
  agentName: string;
  taskId: string | null;
  description: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  list: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface MateClawClientConfig {
  baseUrl?: string;
  timeout?: number;
  onTokenExpired?: () => void;
}

// =============================================================================
// 客户端实现
// =============================================================================

export class MateClawAPIError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public responseBody?: Record<string, unknown>
  ) {
    super(`[${statusCode}] ${message}`);
    this.name = "MateClawAPIError";
  }
}

export class MateClawClient {
  private baseUrl: string;
  private token: string | null = null;
  private tokenExpiresAt: number = 0;
  private timeout: number;
  private onTokenExpired?: () => void;

  constructor(config: MateClawClientConfig = {}) {
    this.baseUrl = (config.baseUrl || "http://localhost:8080").replace(/\/$/, "");
    this.timeout = config.timeout || 30000;
    this.onTokenExpired = config.onTokenExpired;
  }

  // ---------------------------------------------------------------------------
  // 认证
  // ---------------------------------------------------------------------------

  async login(username: string, password: string): Promise<void> {
    const resp = await this._rawRequest("POST", "/api/v1/auth/login", {
      body: JSON.stringify({ username, password }),
    });
    const data = await resp.json();
    const token = data?.data?.token || data?.token;
    if (!token) {
      throw new MateClawAPIError(200, "登录响应中未找到 token 字段", data);
    }
    this.token = token;
    this.tokenExpiresAt = Date.now() + 23 * 3600 * 1000;
  }

  setToken(token: string): void {
    this.token = token;
    this.tokenExpiresAt = Date.now() + 23 * 3600 * 1000;
  }

  isAuthenticated(): boolean {
    return !!this.token && Date.now() < this.tokenExpiresAt - 60000;
  }

  private async _rawRequest(method: string, path: string, options: RequestInit = {}): Promise<Response> {
    const url = `${this.baseUrl}${path}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const resp = await fetch(url, {
        method,
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          ...(options.headers || {}),
        },
        ...options,
      });
      return resp;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async _request<T>(method: string, path: string, options: RequestInit = {}): Promise<T> {
    if (!this.token) {
      throw new MateClawAPIError(401, "未登录，请先调用 login() 方法");
    }

    const headers = {
      Authorization: `Bearer ${this.token}`,
      ...(options.headers || {}),
    };

    let resp = await this._rawRequest(method, path, { ...options, headers });

    // Token 过期，触发回调
    if (resp.status === 401) {
      this.token = null;
      this.onTokenExpired?.();
      throw new MateClawAPIError(401, "Token 已过期，请重新登录");
    }

    if (!resp.ok) {
      let body: Record<string, unknown> = {};
      try {
        body = await resp.json();
      } catch {
        body = { raw: await resp.text() };
      }
      throw new MateClawAPIError(resp.status, (body.message as string) || resp.statusText, body);
    }

    const data = await resp.json();
    return (data.data ?? data) as T;
  }

  private buildQuery(params: Record<string, unknown>): string {
    const filtered = Object.entries(params).filter(([, v]) => v !== undefined && v !== null);
    if (!filtered.length) return "";
    return "?" + new URLSearchParams(filtered.map(([k, v]) => [k, String(v)])).toString();
  }

  // ---------------------------------------------------------------------------
  // 工作空间
  // ---------------------------------------------------------------------------

  async listWorkspaces(): Promise<Workspace[]> {
    const data = await this._request<{ list: Workspace[] } | Workspace[]>("GET", "/api/v1/workspaces");
    return Array.isArray(data) ? data : (data as { list: Workspace[] }).list;
  }

  async getWorkspace(workspaceId: string): Promise<Workspace> {
    return this._request<Workspace>("GET", `/api/v1/workspaces/${workspaceId}`);
  }

  async createWorkspace(name: string, description = "", icon = ""): Promise<Workspace> {
    return this._request<Workspace>("POST", "/api/v1/workspaces", {
      body: JSON.stringify({ name, description, icon }),
    });
  }

  // ---------------------------------------------------------------------------
  // Agent 管理
  // ---------------------------------------------------------------------------

  async listAgents(params: { workspaceId?: string; page?: number; pageSize?: number } = {}): Promise<PaginatedResponse<Agent>> {
    const query = this.buildQuery({ workspaceId: params.workspaceId, page: params.page ?? 1, pageSize: params.pageSize ?? 50 });
    return this._request<PaginatedResponse<Agent>>("GET", `/api/v1/agents${query}`);
  }

  async getAgent(agentId: string): Promise<Agent> {
    return this._request<Agent>("GET", `/api/v1/agents/${agentId}`);
  }

  async getAgentStatus(agentId: string): Promise<AgentStatusInfo> {
    return this._request<AgentStatusInfo>("GET", `/api/v1/agents/${agentId}/status`);
  }

  /**
   * 获取所有 Agent 的实时状态（用于 OPC Dashboard 星系视图）
   * 并发请求所有 Agent 的状态，最大化性能
   */
  async listAllAgentStatuses(): Promise<AgentStatusInfo[]> {
    const agentsData = await this.listAgents({ pageSize: 100 });
    const statusPromises = agentsData.list.map(async (agent) => {
      try {
        const status = await this.getAgentStatus(agent.id);
        return { ...status, name: agent.name, role: agent.role, workspaceId: agent.workspaceId };
      } catch {
        return {
          agentId: agent.id,
          name: agent.name,
          role: agent.role,
          workspaceId: agent.workspaceId,
          status: "offline" as AgentStatus,
          currentTaskId: null,
          lastActiveAt: "",
          tokenUsageToday: 0,
          tokenUsageThisMonth: 0,
        };
      }
    });
    return Promise.all(statusPromises);
  }

  // ---------------------------------------------------------------------------
  // 任务管理
  // ---------------------------------------------------------------------------

  async createTask(params: {
    agentId: string;
    content: string;
    title?: string;
    context?: Record<string, unknown>;
    priority?: TaskPriority;
  }): Promise<Task> {
    return this._request<Task>("POST", "/api/v1/tasks", {
      body: JSON.stringify({
        agentId: params.agentId,
        title: params.title || params.content.slice(0, 50),
        content: params.content,
        context: params.context || {},
        priority: params.priority || "normal",
      }),
    });
  }

  async getTask(taskId: string): Promise<Task> {
    return this._request<Task>("GET", `/api/v1/tasks/${taskId}`);
  }

  async listTasks(params: {
    agentId?: string;
    status?: TaskStatus;
    page?: number;
    pageSize?: number;
  } = {}): Promise<PaginatedResponse<Task>> {
    const query = this.buildQuery({
      agentId: params.agentId,
      status: params.status,
      page: params.page ?? 1,
      pageSize: params.pageSize ?? 20,
    });
    return this._request<PaginatedResponse<Task>>("GET", `/api/v1/tasks${query}`);
  }

  async cancelTask(taskId: string, reason = ""): Promise<void> {
    await this._request("POST", `/api/v1/tasks/${taskId}/cancel`, {
      body: JSON.stringify({ reason }),
    });
  }

  async getTaskLogs(taskId: string): Promise<TaskLog[]> {
    const data = await this._request<{ list: TaskLog[] }>("GET", `/api/v1/tasks/${taskId}/logs`);
    return data.list;
  }

  // ---------------------------------------------------------------------------
  // 审批管理（Escalation）
  // ---------------------------------------------------------------------------

  async listPendingApprovals(): Promise<ApprovalRequest[]> {
    const data = await this._request<{ list: ApprovalRequest[] }>(
      "GET",
      "/api/v1/approvals" + this.buildQuery({ status: "pending" })
    );
    return data.list;
  }

  async listAllApprovals(params: { status?: string; page?: number; pageSize?: number } = {}): Promise<PaginatedResponse<ApprovalRequest>> {
    const query = this.buildQuery({ status: params.status, page: params.page ?? 1, pageSize: params.pageSize ?? 20 });
    return this._request<PaginatedResponse<ApprovalRequest>>("GET", `/api/v1/approvals${query}`);
  }

  async approve(approvalId: string, comment = "CEO 已审批"): Promise<void> {
    await this._request("POST", `/api/v1/approvals/${approvalId}/review`, {
      body: JSON.stringify({ action: "approve", comment }),
    });
  }

  async reject(approvalId: string, reason: string): Promise<void> {
    await this._request("POST", `/api/v1/approvals/${approvalId}/review`, {
      body: JSON.stringify({ action: "reject", comment: reason }),
    });
  }

  // ---------------------------------------------------------------------------
  // 系统统计（OPC Dashboard 大盘数据）
  // ---------------------------------------------------------------------------

  async getDashboardStats(): Promise<DashboardStats> {
    return this._request<DashboardStats>("GET", "/api/v1/dashboard/stats");
  }

  async getActivityFeed(limit = 20): Promise<ActivityItem[]> {
    const data = await this._request<{ list: ActivityItem[] }>(
      "GET",
      `/api/v1/activities${this.buildQuery({ limit })}`
    );
    return data.list;
  }

  // ---------------------------------------------------------------------------
  // Cron 定时任务
  // ---------------------------------------------------------------------------

  async listCronTasks(): Promise<unknown[]> {
    const data = await this._request<{ list: unknown[] }>("GET", "/api/v1/cron-tasks");
    return data.list;
  }

  async createCronTask(params: {
    name: string;
    agentId: string;
    cronExpression: string;
    taskContent: string;
    enabled?: boolean;
  }): Promise<unknown> {
    return this._request("POST", "/api/v1/cron-tasks", {
      body: JSON.stringify({
        name: params.name,
        agentId: params.agentId,
        cronExpression: params.cronExpression,
        taskContent: params.taskContent,
        enabled: params.enabled ?? true,
      }),
    });
  }
}

// =============================================================================
// React Hook（用于 OPC Dashboard 组件）
// =============================================================================

/**
 * 在 OPC Dashboard 中使用 MateClaw 客户端的示例 React Hook
 *
 * 使用方法（在 OPC Dashboard 组件中）：
 *   const { client, stats, agentStatuses, pendingApprovals } = useMateClaw();
 */
export function createMateClawHooks(client: MateClawClient) {
  return {
    /**
     * 获取大盘统计数据
     * 用于 DashboardView 的 KPI 卡片
     */
    async fetchDashboardStats(): Promise<DashboardStats> {
      return client.getDashboardStats();
    },

    /**
     * 获取所有 Agent 状态
     * 用于 GalaxyView 的星系视图
     */
    async fetchAgentStatuses(): Promise<AgentStatusInfo[]> {
      return client.listAllAgentStatuses();
    },

    /**
     * 获取待审批列表
     * 用于 DashboardView 的硬停警报抽屉
     */
    async fetchPendingApprovals(): Promise<ApprovalRequest[]> {
      return client.listPendingApprovals();
    },

    /**
     * 向 CoS 发布任务
     * 用于 ⌘K 命令面板的"发布任务"命令
     */
    async publishTask(cosAgentId: string, content: string, priority: TaskPriority = "normal"): Promise<Task> {
      return client.createTask({ agentId: cosAgentId, content, priority });
    },

    /**
     * CEO 审批通过
     * 用于 DashboardView 的审批弹窗
     */
    async approveRequest(approvalId: string): Promise<void> {
      return client.approve(approvalId);
    },

    /**
     * CEO 审批拒绝
     * 用于 DashboardView 的审批弹窗
     */
    async rejectRequest(approvalId: string, reason: string): Promise<void> {
      return client.reject(approvalId, reason);
    },

    /**
     * 获取活动流
     * 用于 DashboardView 的最近活动列表
     */
    async fetchActivityFeed(): Promise<ActivityItem[]> {
      return client.getActivityFeed(20);
    },
  };
}

// =============================================================================
// 全局单例（在 OPC Dashboard 中使用）
// =============================================================================

let _globalClient: MateClawClient | null = null;

export function initMateClawClient(config: MateClawClientConfig & { username: string; password: string }): MateClawClient {
  _globalClient = new MateClawClient(config);
  return _globalClient;
}

export function getMateClawClient(): MateClawClient {
  if (!_globalClient) {
    throw new Error("MateClaw 客户端未初始化，请先调用 initMateClawClient()");
  }
  return _globalClient;
}
