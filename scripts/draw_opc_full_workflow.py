#!/usr/bin/env python3
"""
OPC 完整工作流可视化图
清晰大字体版本，展示从线索到交付的全链路
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# 字体设置
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ── 颜色主题 ──────────────────────────────────────────
C = {
    'bg':        '#0D1117',
    'ceo':       '#7C3AED',
    'ceo_light': '#EDE9FE',
    'mkt':       '#0EA5E9',
    'mkt_light': '#E0F2FE',
    'dev':       '#2563EB',
    'dev_light': '#DBEAFE',
    'design':    '#059669',
    'design_light': '#D1FAE5',
    'ops':       '#D97706',
    'ops_light': '#FEF3C7',
    'state':     '#374151',
    'state_light': '#F3F4F6',
    'file':      '#6B7280',
    'file_light': '#F9FAFB',
    'arrow':     '#94A3B8',
    'white':     '#FFFFFF',
    'gray1':     '#1F2937',
    'gray2':     '#374151',
    'gray3':     '#6B7280',
    'gold':      '#F59E0B',
    'red':       '#EF4444',
}

fig = plt.figure(figsize=(52, 34), facecolor=C['bg'])
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 52)
ax.set_ylim(0, 34)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor(C['bg'])

# ── 辅助函数 ──────────────────────────────────────────

def card(x, y, w, h, color, label, sublabel='', icon='', radius=0.35):
    """绘制圆角卡片"""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=color, edgecolor='none', zorder=3)
    ax.add_patch(box)
    # 顶部色带
    top = FancyBboxPatch((x, y+h-0.28), w, 0.28,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=darken(color, 0.25), edgecolor='none', zorder=4)
    ax.add_patch(top)
    # 主标签
    ty = y + h/2 + (0.12 if sublabel else 0)
    ax.text(x + w/2, ty, (icon+' ' if icon else '') + label,
            ha='center', va='center', fontsize=13, fontweight='bold',
            color=C['white'], zorder=5)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.25, sublabel,
                ha='center', va='center', fontsize=9.5, color='#CBD5E1', zorder=5)

def darken(hex_color, factor=0.2):
    """颜色加深"""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    r = max(0, int(r*(1-factor)))
    g = max(0, int(g*(1-factor)))
    b = max(0, int(b*(1-factor)))
    return f'#{r:02x}{g:02x}{b:02x}'

def zone(x, y, w, h, color, title, alpha=0.08):
    """绘制区域背景"""
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0,rounding_size=0.5",
                          facecolor=color, edgecolor=color,
                          linewidth=1.5, alpha=alpha, zorder=1)
    ax.add_patch(rect)
    border = FancyBboxPatch((x, y), w, h,
                            boxstyle="round,pad=0,rounding_size=0.5",
                            facecolor='none', edgecolor=color,
                            linewidth=1.5, alpha=0.4, zorder=2)
    ax.add_patch(border)
    ax.text(x + 0.35, y + h - 0.35, title,
            ha='left', va='top', fontsize=11, fontweight='bold',
            color=color, alpha=0.9, zorder=5)

def arrow(x1, y1, x2, y2, color=None, lw=2, label='', dashed=False):
    """绘制箭头"""
    c = color or C['arrow']
    ls = '--' if dashed else '-'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=c,
                               lw=lw, linestyle=ls,
                               connectionstyle='arc3,rad=0'),
                zorder=6)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.1, my+0.1, label, ha='left', va='bottom',
                fontsize=8.5, color=c, zorder=7,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=C['bg'],
                         edgecolor='none', alpha=0.8))

def state_badge(x, y, text, color):
    """绘制状态徽章"""
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
            color=C['white'], fontweight='bold', zorder=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color,
                     edgecolor='none', alpha=0.95))

def file_node(x, y, text, w=2.8, h=0.55):
    """绘制文件节点"""
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                         boxstyle="round,pad=0,rounding_size=0.18",
                         facecolor='#1E293B', edgecolor='#475569',
                         linewidth=1, zorder=4)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
            color='#94A3B8', zorder=5)

def step_num(x, y, n, color):
    """绘制步骤编号圆圈"""
    circle = plt.Circle((x, y), 0.22, color=color, zorder=8)
    ax.add_patch(circle)
    ax.text(x, y, str(n), ha='center', va='center',
            fontsize=10, fontweight='bold', color=C['white'], zorder=9)

# ═══════════════════════════════════════════════════════
# 标题区
# ═══════════════════════════════════════════════════════
title_bg = FancyBboxPatch((0.4, 31.8), 51.2, 1.9,
                           boxstyle="round,pad=0,rounding_size=0.4",
                           facecolor='#1E1B4B', edgecolor='#7C3AED',
                           linewidth=2, zorder=2)
ax.add_patch(title_bg)
ax.text(26, 33.15, 'OPC (One Person Company)  多智能体商业闭环全流程',
        ha='center', va='center', fontsize=22, fontweight='bold',
        color=C['white'], zorder=5)
ax.text(26, 32.55, 'ai-company-os v1.0  |  20 Agents  |  6 阶段  |  全自动商业闭环  |  CEO 仅需 5 秒审批',
        ha='center', va='center', fontsize=12, color='#A5B4FC', zorder=5)

# ═══════════════════════════════════════════════════════
# 区域背景
# ═══════════════════════════════════════════════════════
zone(0.4, 29.0, 51.2, 2.5, C['ceo'],   'CEO 层 — 战略决策与路由')
zone(0.4, 22.2, 51.2, 6.5, C['mkt'],   '公司层 — 流量与转化引擎 (2_marketing)')
zone(0.4,  7.2, 24.8, 14.7, C['design'], '设计团队 — 创意生产 (design_team)')
zone(26.0,  7.2, 25.6, 14.7, C['dev'],   '开发团队 — 工程实现 (dev_team)')
zone(0.4,  1.0, 51.2, 5.9, C['ops'],   '运营层 — 交付与归档 (4_operations)')

# ═══════════════════════════════════════════════════════
# CEO 层
# ═══════════════════════════════════════════════════════
card(22.5, 29.4, 7.0, 1.8, C['ceo'], 'CEO', '战略决策 | 审批 | 路由')
step_num(22.5, 31.2, '★', C['gold'])

# CEO 审批说明
ax.text(10.5, 30.3, '路径 A: Stripe 支付成功', ha='center', va='center',
        fontsize=10, color='#A5B4FC',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E1B4B',
                 edgecolor='#7C3AED', linewidth=1, alpha=0.9))
ax.text(41.5, 30.3, '路径 B: CEO 申请批准 (5秒)', ha='center', va='center',
        fontsize=10, color='#A5B4FC',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E1B4B',
                 edgecolor='#7C3AED', linewidth=1, alpha=0.9))

# ═══════════════════════════════════════════════════════
# 公司层 — 流量与转化
# ═══════════════════════════════════════════════════════

# 阶段 1：小探
card(1.2, 26.0, 6.0, 1.7, C['mkt'], '小探 (Scout)', '线索抓取 | 评分 | 分类')
step_num(1.2, 27.7, '1', C['mkt'])
file_node(4.2, 25.3, 'leads/LEAD-xxx.json')

# 阶段 2：小播
card(9.0, 26.0, 6.0, 1.7, C['mkt'], '小播 (Broadcaster)', '内容生成 | 自动发布')
step_num(9.0, 27.7, '2', C['mkt'])
file_node(12.0, 25.3, 'content/post_xxx.md')

# 阶段 3：小销
card(18.5, 26.0, 6.5, 1.7, C['mkt'], '小销 (Closer)', '冷邮件 | 报价 | 转化')
step_num(18.5, 27.7, '3', C['mkt'])
file_node(21.75, 25.3, 'ESCALATIONS/CEO_REQ.json')

# CEO 申请 → CEO 审批
arrow(21.75, 29.4, 25.5, 29.4, C['ceo'], lw=2, label='CEO 申请')
arrow(25.5, 29.4, 21.75, 29.4, C['gold'], lw=2, label='批准/拒绝', dashed=True)

# 阶段 4：CoS 接单
card(29.0, 26.0, 6.5, 1.7, C['dev'], 'CoS 幕僚长', 'QAPS 拆解 | 任务分配')
step_num(29.0, 27.7, '4', C['dev'])
file_node(32.25, 25.3, 'active_projects/P-xxx/status.json')

# 公司层内部流转箭头
arrow(7.2, 26.85, 9.0, 26.85, C['mkt'], lw=2)
arrow(15.0, 26.85, 18.5, 26.85, C['mkt'], lw=2)
arrow(25.0, 26.85, 29.0, 26.85, C['dev'], lw=2.5, label='触发生产')

# 小探→小播 数据流
arrow(4.2, 25.3, 4.2, 24.5, C['mkt'], lw=1.5, dashed=True)

# ═══════════════════════════════════════════════════════
# 设计团队（左侧）
# ═══════════════════════════════════════════════════════

design_agents = [
    ('小管', 'ProjectManager', '接单 | 排期 | 协调'),
    ('小研', 'Researcher',     '市场调研 | 竞品分析'),
    ('小策', 'Planner',        '设计方向 | 线框图'),
    ('小设', 'Designer',       'NanaBanana | Stitch'),
    ('小文', 'Copywriter',     '文案 | 双语内容'),
    ('小牌', 'Brand',          '品牌合规 | 视觉审查'),
    ('CDO',  'Chief Design',   '最终审批 | 质量把关'),
    ('小运', 'Operations',     '归档 | 资产整理'),
]

dy_start = 21.5
dy_step = 1.72
for i, (name, role, desc) in enumerate(design_agents):
    y = dy_start - i * dy_step
    card(1.0, y, 10.5, 1.5, C['design'], f'{name} ({role})', desc)
    step_num(1.0, y+1.5, str(i+1), C['design'])
    if i < len(design_agents)-1:
        arrow(6.25, y, 6.25, y-0.22, C['design'], lw=1.8)

# 设计产出文件（右侧标注）
design_files = [
    (21.5, 'brief.md'),
    (19.78, 'research_report.md'),
    (18.06, 'layout_specs.md'),
    (16.34, 'assets/ + design_tokens.json'),
    (14.62, 'copywriting.json'),
    (12.90, 'brand_check.md'),
    (11.18, 'CDO_APPROVED'),
    (9.46, 'design_output/ → shared'),
]
for y, fname in design_files:
    file_node(14.5, y+0.75, fname, w=3.8)
    arrow(11.5, y+0.75, 12.6, y+0.75, C['design'], lw=1.2, dashed=True)

# ═══════════════════════════════════════════════════════
# 开发团队（右侧）
# ═══════════════════════════════════════════════════════

dev_agents = [
    ('CoS', 'Chief of Staff', 'QAPS 拆解 | 任务调度'),
    ('CTO', 'Tech Lead',      'ADR 架构决策 | 技术评审'),
    ('Researcher', 'Research', '技术调研 | 方案评估'),
    ('BE',  'Backend',        'API 开发 | 数据库设计'),
    ('FE',  'Frontend',       'React | Tailwind | 动效'),
    ('QA',  'Quality',        '自动化测试 | Bug 追踪'),
    ('Ops', 'DevOps',         'CI/CD | Vercel 部署'),
    ('KO',  'Knowledge',      'SKILL.md | 经验沉淀'),
]

for i, (name, role, desc) in enumerate(dev_agents):
    y = dy_start - i * dy_step
    card(26.5, y, 10.5, 1.5, C['dev'], f'{name} ({role})', desc)
    step_num(26.5, y+1.5, str(i+1), C['dev'])
    if i < len(dev_agents)-1:
        arrow(31.75, y, 31.75, y-0.22, C['dev'], lw=1.8)

# 开发产出文件（右侧标注）
dev_files = [
    (21.5, 'tasks/TASK-xxx.md'),
    (19.78, 'ADR-xxx.md'),
    (18.06, 'research_report.md'),
    (16.34, 'src/api/*.ts'),
    (14.62, 'src/components/*.jsx'),
    (12.90, 'tests/qa_report.json'),
    (11.18, 'deploy_log.md'),
    (9.46, 'skills/SKILL.md'),
]
for y, fname in dev_files:
    file_node(39.5, y+0.75, fname, w=3.8)
    arrow(37.0, y+0.75, 37.6, y+0.75, C['dev'], lw=1.2, dashed=True)

# ═══════════════════════════════════════════════════════
# 跨团队交接箭头（设计 → 开发）
# ═══════════════════════════════════════════════════════
arrow(11.5, 12.5, 26.5, 12.5, C['gold'], lw=3, label='设计交接 (4类文件)')
ax.text(19.0, 12.85, 'design_tokens.json  |  layout_specs.md  |  copywriting.json  |  assets/',
        ha='center', va='bottom', fontsize=9, color=C['gold'])

# ═══════════════════════════════════════════════════════
# 运营层 — 交付
# ═══════════════════════════════════════════════════════

# 小服
card(10.0, 2.2, 8.5, 1.8, C['ops'], '小服 (CSM)', '打包交付 | 发送客户 | 收集反馈')
step_num(10.0, 4.0, '6', C['ops'])

# 财务记录
card(22.0, 2.2, 8.5, 1.8, C['ops'], '财务记录', 'finance_tracker.csv | 收入统计')
file_node(26.25, 1.5, 'finance_tracker.csv', w=4.0)

# 知识库
card(34.0, 2.2, 8.5, 1.8, C['ops'], '知识沉淀 (KO)', 'SKILL.md | 经验归档 | 自我进化')
file_node(38.25, 1.5, 'knowledge-base/SKILL.md', w=4.2)

# 客户反馈 → 复购
card(44.5, 2.2, 6.8, 1.8, C['ceo'], '复购 / 口碑', '客户满意 → 续费 → 转介绍')

# 运营层内部箭头
arrow(18.5, 3.1, 22.0, 3.1, C['ops'], lw=2)
arrow(30.5, 3.1, 34.0, 3.1, C['ops'], lw=2)
arrow(42.5, 3.1, 44.5, 3.1, C['ceo'], lw=2)

# 开发团队 → 小服
arrow(31.75, 7.2, 14.25, 4.0, C['ops'], lw=2.5, label='READY_FOR_DELIVERY')

# 小服 → CEO (复购闭环)
arrow(47.85, 4.0, 26.0, 29.4, C['ceo'], lw=2, label='复购闭环', dashed=True)

# ═══════════════════════════════════════════════════════
# 状态机节点（中间列）
# ═══════════════════════════════════════════════════════
states = [
    (19.5, 26.85, 'LEAD_CAPTURED',      C['mkt']),
    (19.5, 25.0,  'NEGOTIATING',         C['mkt']),
    (19.5, 23.2,  'CEO_APPROVED',        C['ceo']),
    (19.5, 21.4,  'PRODUCTION_STARTED',  C['dev']),
    (19.5, 19.6,  'DESIGN_APPROVED',     C['design']),
    (19.5, 17.8,  'DEVELOPING',          C['dev']),
    (19.5, 16.0,  'QA_PASSED',           C['dev']),
    (19.5, 14.2,  'READY_FOR_DELIVERY',  C['ops']),
    (19.5, 12.4,  'DELIVERED',           C['ops']),
]
for x, y, text, color in states:
    state_badge(x, y, text, color)

# 状态机标题
ax.text(19.5, 22.1, 'STATUS\nMACHINE', ha='center', va='center',
        fontsize=9, color='#64748B', fontweight='bold')

# ═══════════════════════════════════════════════════════
# 图例
# ═══════════════════════════════════════════════════════
legend_y = 0.55
legend_items = [
    (C['ceo'],    'CEO 层'),
    (C['mkt'],    '公司层/流量'),
    (C['design'], '设计团队'),
    (C['dev'],    '开发团队'),
    (C['ops'],    '运营/交付'),
    (C['gold'],   '关键交接'),
]
lx = 1.5
for color, label in legend_items:
    rect = FancyBboxPatch((lx, legend_y-0.18), 0.7, 0.36,
                          boxstyle="round,pad=0,rounding_size=0.08",
                          facecolor=color, edgecolor='none', zorder=5)
    ax.add_patch(rect)
    ax.text(lx+0.85, legend_y, label, ha='left', va='center',
            fontsize=10, color='#CBD5E1', zorder=5)
    lx += 3.8

ax.text(26, 0.55, '全部 46 项工作流测试通过 (100%)  |  GitHub: github.com/leixing333/ai-company-os',
        ha='center', va='center', fontsize=10, color='#64748B')

# ═══════════════════════════════════════════════════════
# 保存
# ═══════════════════════════════════════════════════════
out = '/home/ubuntu/ai-company-os/docs/OPC_Full_Workflow_v3.png'
plt.savefig(out, dpi=150, bbox_inches='tight',
            facecolor=C['bg'], edgecolor='none')
plt.close()
print(f"已生成: {out}")
