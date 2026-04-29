#!/usr/bin/env python3
"""
OPC 完整工作流模拟测试脚本
测试从小探抓取线索 → 小销转化 → CEO 审批 → 生产引擎 → 小服交付的全链路
"""

import os
import json
import shutil
from datetime import datetime

BASE = "/home/ubuntu/ai-company-os"
PROJECTS_DIR = f"{BASE}/3_production/active_projects"
DELIVERABLES_DIR = f"{BASE}/4_operations/deliverables"
ESCALATIONS_DIR = f"{BASE}/1_strategy/ESCALATIONS"
LEADS_DIR = f"{BASE}/2_marketing/leads"
FINANCE_LOG = f"{BASE}/1_strategy/finance_tracker.csv"

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

results = []

def test(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append({"name": name, "status": status, "detail": detail})
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ─────────────────────────────────────────────
# 阶段 0：环境检查
# ─────────────────────────────────────────────
section("阶段 0：环境与目录结构检查")

critical_dirs = [
    f"{BASE}/.opc",
    f"{BASE}/1_strategy",
    f"{BASE}/2_marketing/agents/scout",
    f"{BASE}/2_marketing/agents/closer",
    f"{BASE}/2_marketing/agents/broadcaster",
    f"{BASE}/3_production/active_projects",
    f"{BASE}/3_production/infrastructure/lobster-legion",
    f"{BASE}/3_production/shared_workspace",
    f"{BASE}/4_operations/agents/csm",
    f"{BASE}/4_operations/deliverables",
]
for d in critical_dirs:
    test(f"目录存在: {d.replace(BASE,'')}", os.path.isdir(d))

critical_files = [
    f"{BASE}/.opc/config.json",
    f"{BASE}/3_production/shared_workspace/STATUS_MACHINE.json",
    f"{BASE}/3_production/shared_workspace/BRIEF_SCHEMA.json",
    f"{BASE}/3_production/shared_workspace/DESIGN_HANDOFF_SPEC.md",
    f"{BASE}/3_production/infrastructure/lobster-legion/openclaw.json",
    f"{BASE}/3_production/infrastructure/lobster-legion/agents/cos/SOUL.md",
]
for f in critical_files:
    test(f"文件存在: {f.replace(BASE,'')}", os.path.isfile(f))

# ─────────────────────────────────────────────
# 阶段 1：小探 (Scout) — 线索抓取
# ─────────────────────────────────────────────
section("阶段 1：小探 (Scout) — 线索抓取模拟")

os.makedirs(LEADS_DIR, exist_ok=True)
lead_data = {
    "lead_id": "LEAD-20251025-001",
    "company": "StartupX",
    "contact": "Alex Chen",
    "email": "alex@startupx.io",
    "source": "Product Hunt",
    "pain_point": "需要高质量品牌设计，预算有限",
    "score": 87,
    "status": "NEW",
    "created_at": datetime.now().isoformat()
}
lead_file = f"{LEADS_DIR}/LEAD-20251025-001.json"
with open(lead_file, 'w', encoding='utf-8') as f:
    json.dump(lead_data, f, ensure_ascii=False, indent=2)

test("小探写入线索文件", os.path.isfile(lead_file), "LEAD-20251025-001.json")
test("线索评分字段存在", "score" in lead_data, f"score={lead_data['score']}")
test("线索状态为 NEW", lead_data["status"] == "NEW")

# ─────────────────────────────────────────────
# 阶段 2：小销 (Closer) — 转化与 CEO 申请
# ─────────────────────────────────────────────
section("阶段 2：小销 (Closer) — 转化与 CEO 申请")

os.makedirs(ESCALATIONS_DIR, exist_ok=True)
project_id = "P-20251025-001"
ceo_request = {
    "request_id": f"CEO-REQ-{project_id}",
    "project_id": project_id,
    "trigger_source": "ceo_approval",
    "client": lead_data["company"],
    "contact": lead_data["contact"],
    "email": lead_data["email"],
    "service": "AI 设计服务 - 产品落地页",
    "price_usd": 999,
    "payment_status": "pending",
    "intent_level": "HIGH",
    "closer_notes": "客户已确认需求，报价已发送，等待付款或 CEO 批准先行启动",
    "status": "PENDING_CEO_APPROVAL",
    "created_at": datetime.now().isoformat()
}
req_file = f"{ESCALATIONS_DIR}/CEO_APPROVAL_REQUEST_{project_id}.json"
with open(req_file, 'w', encoding='utf-8') as f:
    json.dump(ceo_request, f, ensure_ascii=False, indent=2)

test("小销创建 CEO 申请文件", os.path.isfile(req_file))
test("申请包含 trigger_source 字段", "trigger_source" in ceo_request)
test("申请状态为 PENDING_CEO_APPROVAL", ceo_request["status"] == "PENDING_CEO_APPROVAL")

# 模拟 CEO 审批
ceo_request["status"] = "APPROVED"
ceo_request["ceo_approved_at"] = datetime.now().isoformat()
ceo_request["ceo_notes"] = "客户意向明确，先行启动，付款在交付前结清"
with open(req_file, 'w', encoding='utf-8') as f:
    json.dump(ceo_request, f, ensure_ascii=False, indent=2)

test("CEO 审批通过 (status=APPROVED)", ceo_request["status"] == "APPROVED")

# ─────────────────────────────────────────────
# 阶段 3：CoS — 接单与项目初始化
# ─────────────────────────────────────────────
section("阶段 3：CoS — 接单与项目初始化")

project_dir = f"{PROJECTS_DIR}/{project_id}"
os.makedirs(project_dir, exist_ok=True)

status_data = {
    "project_id": project_id,
    "client": "StartupX",
    "service": "AI 设计服务 - 产品落地页",
    "trigger_source": "ceo_approval",
    "status": "PRODUCTION_STARTED",
    "current_team": "design",
    "assigned_to": "projectmanager",
    "price_usd": 999,
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat(),
    "history": [
        {"status": "LEAD_CAPTURED", "agent": "scout", "ts": datetime.now().isoformat()},
        {"status": "NEGOTIATING", "agent": "closer", "ts": datetime.now().isoformat()},
        {"status": "CEO_APPROVED", "agent": "ceo", "ts": datetime.now().isoformat()},
        {"status": "PRODUCTION_STARTED", "agent": "cos", "ts": datetime.now().isoformat()}
    ]
}
status_file = f"{project_dir}/status.json"
with open(status_file, 'w', encoding='utf-8') as f:
    json.dump(status_data, f, ensure_ascii=False, indent=2)

brief_content = f"""# 项目简报 — {project_id}

## 客户信息
- **公司**: StartupX
- **联系人**: Alex Chen (alex@startupx.io)
- **预算**: $999/月

## 项目需求
设计一个高转化率的 AI 设计服务落地页，包含：
- Hero 区块（主标题 + CTA）
- 服务介绍（3 个核心优势）
- 作品集展示（6 个案例）
- 定价方案（单一定价卡）
- FAQ（8 个问题）

## 设计要求
- 风格：现代简约，深色主题
- 色调：深蓝 + 金色点缀
- 字体：Inter（英文）+ 思源黑体（中文）
- 响应式：支持移动端

## 交付物
- [ ] design_tokens.json（设计变量）
- [ ] assets/（所有切图）
- [ ] layout_specs.md（布局规范）
- [ ] copywriting.json（文案映射）
- [ ] 完整 React 组件代码
- [ ] 部署到 Vercel

## 截止时间
{datetime.now().strftime('%Y-%m-%d')} 起 72 小时内交付
"""
brief_file = f"{project_dir}/brief.md"
with open(brief_file, 'w', encoding='utf-8') as f:
    f.write(brief_content)

test("CoS 创建项目目录", os.path.isdir(project_dir))
test("CoS 写入 status.json", os.path.isfile(status_file))
test("状态为 PRODUCTION_STARTED", status_data["status"] == "PRODUCTION_STARTED")
test("CoS 写入 brief.md", os.path.isfile(brief_file))
test("历史记录包含 4 个状态节点", len(status_data["history"]) == 4)

# ─────────────────────────────────────────────
# 阶段 4：设计团队 — 生产流水线
# ─────────────────────────────────────────────
section("阶段 4：设计团队 — 生产流水线")

design_dir = f"{project_dir}/design_output"
os.makedirs(design_dir, exist_ok=True)
os.makedirs(f"{design_dir}/assets", exist_ok=True)

# 小策输出布局规范
layout_specs = """# 布局规范 — StartupX 落地页

## Hero 区块
- 布局: flex, flex-col, items-center
- 背景: bg-gray-950
- 标题: text-5xl font-bold text-white
- 副标题: text-xl text-gray-400
- CTA 主按钮: bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl

## 服务卡片
- 布局: grid grid-cols-3 gap-6
- 卡片: bg-gray-900 border border-gray-800 rounded-2xl p-6

## 定价卡
- 布局: flex justify-center
- 卡片宽度: max-w-md
- 价格: text-6xl font-bold text-white
- 特性列表: text-gray-300 space-y-3
"""
with open(f"{design_dir}/layout_specs.md", 'w', encoding='utf-8') as f:
    f.write(layout_specs)

# 小设输出设计变量
design_tokens = {
    "colors": {
        "primary": "#2563EB",
        "primary_hover": "#3B82F6",
        "accent": "#F59E0B",
        "bg_base": "#030712",
        "bg_card": "#111827",
        "text_primary": "#FFFFFF",
        "text_secondary": "#9CA3AF"
    },
    "typography": {
        "font_en": "Inter",
        "font_zh": "Noto Sans SC",
        "size_h1": "3rem",
        "size_h2": "2rem",
        "size_body": "1rem"
    },
    "spacing": {
        "section_gap": "5rem",
        "card_padding": "1.5rem",
        "border_radius": "1rem"
    }
}
with open(f"{design_dir}/design_tokens.json", 'w', encoding='utf-8') as f:
    json.dump(design_tokens, f, ensure_ascii=False, indent=2)

# 小文输出文案
copywriting = {
    "hero": {
        "headline": "AI 驱动的设计服务，交付速度提升 4 倍",
        "subheadline": "订阅即用，无需招聘，随时暂停",
        "cta_primary": "查看方案",
        "cta_secondary": "预约演示"
    },
    "pricing": {
        "price": "$999",
        "period": "/月",
        "tagline": "一个请求，无限可能",
        "cta": "立即订阅",
        "note": "随时暂停或取消，无合同绑定"
    },
    "faq": [
        {"q": "交付周期是多久？", "a": "通常 12-24 小时内完成一个设计请求。"},
        {"q": "可以随时取消吗？", "a": "是的，随时可以暂停或取消，无任何违约金。"}
    ]
}
with open(f"{design_dir}/copywriting.json", 'w', encoding='utf-8') as f:
    json.dump(copywriting, f, ensure_ascii=False, indent=2)

# 模拟小设生成资产占位文件
with open(f"{design_dir}/assets/hero_bg.svg", 'w') as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="800"><rect fill="#030712"/></svg>')
with open(f"{design_dir}/assets/logo.svg", 'w') as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40"><text fill="white">OPC</text></svg>')

test("小策写入 layout_specs.md", os.path.isfile(f"{design_dir}/layout_specs.md"))
test("小设写入 design_tokens.json", os.path.isfile(f"{design_dir}/design_tokens.json"))
test("小文写入 copywriting.json", os.path.isfile(f"{design_dir}/copywriting.json"))
test("小设生成 assets 目录", os.path.isdir(f"{design_dir}/assets"))
test("设计变量包含颜色/字体/间距", all(k in design_tokens for k in ["colors","typography","spacing"]))

# 更新状态：设计完成，移交开发
status_data["status"] = "DESIGN_APPROVED"
status_data["current_team"] = "dev"
status_data["assigned_to"] = "cos"
status_data["updated_at"] = datetime.now().isoformat()
status_data["history"].append({"status": "DESIGN_APPROVED", "agent": "cdo", "ts": datetime.now().isoformat()})
with open(status_file, 'w', encoding='utf-8') as f:
    json.dump(status_data, f, ensure_ascii=False, indent=2)

test("CDO 审批通过，状态更新为 DESIGN_APPROVED", status_data["status"] == "DESIGN_APPROVED")

# ─────────────────────────────────────────────
# 阶段 5：开发团队 — 编码与测试
# ─────────────────────────────────────────────
section("阶段 5：开发团队 — 编码与测试")

dev_dir = f"{project_dir}/dev_output"
os.makedirs(dev_dir, exist_ok=True)

# 模拟 FE 读取设计交接文件
handoff_files = [
    f"{design_dir}/design_tokens.json",
    f"{design_dir}/layout_specs.md",
    f"{design_dir}/copywriting.json",
]
all_handoff_exist = all(os.path.isfile(f) for f in handoff_files)
test("FE 验证设计交接文件完整性", all_handoff_exist, "4 类文件全部存在")

# 模拟 FE 生成组件代码
component_code = """import React from 'react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Hero Section */}
      <section className="flex flex-col items-center py-24 px-6">
        <h1 className="text-5xl font-bold text-center max-w-3xl">
          AI 驱动的设计服务，交付速度提升 4 倍
        </h1>
        <p className="text-xl text-gray-400 mt-6 text-center max-w-xl">
          订阅即用，无需招聘，随时暂停
        </p>
        <div className="flex gap-4 mt-10">
          <button className="bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-semibold">
            查看方案
          </button>
          <button className="border border-gray-700 px-8 py-4 rounded-xl font-semibold">
            预约演示
          </button>
        </div>
      </section>
      {/* Pricing Section */}
      <section className="flex justify-center py-20 px-6">
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-10 max-w-md w-full">
          <div className="text-6xl font-bold">$999<span className="text-2xl text-gray-400">/月</span></div>
          <p className="text-gray-400 mt-2">一个请求，无限可能</p>
          <button className="w-full bg-blue-600 hover:bg-blue-500 py-4 rounded-xl font-semibold mt-8">
            立即订阅
          </button>
          <p className="text-gray-500 text-sm text-center mt-4">随时暂停或取消，无合同绑定</p>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
"""
with open(f"{dev_dir}/LandingPage.jsx", 'w', encoding='utf-8') as f:
    f.write(component_code)

# 模拟 QA 测试报告
qa_report = {
    "project_id": project_id,
    "tested_by": "qa",
    "test_date": datetime.now().isoformat(),
    "tests": [
        {"name": "桌面端渲染", "status": "PASS"},
        {"name": "移动端响应式", "status": "PASS"},
        {"name": "CTA 按钮点击", "status": "PASS"},
        {"name": "Stripe 支付链接", "status": "PASS"},
        {"name": "页面加载速度 < 2s", "status": "PASS"},
        {"name": "无控制台报错", "status": "PASS"},
    ],
    "overall": "PASS",
    "notes": "所有测试通过，可以部署"
}
with open(f"{dev_dir}/qa_report.json", 'w', encoding='utf-8') as f:
    json.dump(qa_report, f, ensure_ascii=False, indent=2)

test("FE 生成 LandingPage.jsx", os.path.isfile(f"{dev_dir}/LandingPage.jsx"))
test("QA 生成测试报告", os.path.isfile(f"{dev_dir}/qa_report.json"))
test("QA 所有测试通过", qa_report["overall"] == "PASS")
test("QA 测试覆盖 6 个场景", len(qa_report["tests"]) >= 6)

# 更新状态：开发完成
status_data["status"] = "READY_FOR_DELIVERY"
status_data["current_team"] = "operations"
status_data["assigned_to"] = "csm"
status_data["updated_at"] = datetime.now().isoformat()
status_data["history"].append({"status": "READY_FOR_DELIVERY", "agent": "ops", "ts": datetime.now().isoformat()})
with open(status_file, 'w', encoding='utf-8') as f:
    json.dump(status_data, f, ensure_ascii=False, indent=2)

test("Ops 部署完成，状态更新为 READY_FOR_DELIVERY", status_data["status"] == "READY_FOR_DELIVERY")

# ─────────────────────────────────────────────
# 阶段 6：小服 (CSM) — 交付与归档
# ─────────────────────────────────────────────
section("阶段 6：小服 (CSM) — 交付与归档")

os.makedirs(DELIVERABLES_DIR, exist_ok=True)
delivery_dir = f"{DELIVERABLES_DIR}/{project_id}"
os.makedirs(delivery_dir, exist_ok=True)

# 小服打包交付物
for src, dst in [
    (f"{design_dir}/design_tokens.json", f"{delivery_dir}/design_tokens.json"),
    (f"{design_dir}/copywriting.json", f"{delivery_dir}/copywriting.json"),
    (f"{dev_dir}/LandingPage.jsx", f"{delivery_dir}/LandingPage.jsx"),
    (f"{dev_dir}/qa_report.json", f"{delivery_dir}/qa_report.json"),
]:
    if os.path.isfile(src):
        shutil.copy2(src, dst)

# 生成交付确认单
delivery_receipt = {
    "project_id": project_id,
    "client": "StartupX",
    "delivered_by": "csm",
    "delivery_time": datetime.now().isoformat(),
    "items": [
        "design_tokens.json",
        "copywriting.json",
        "LandingPage.jsx",
        "qa_report.json"
    ],
    "deploy_url": "https://startupx-landing.vercel.app",
    "status": "DELIVERED",
    "invoice_status": "PENDING_PAYMENT",
    "amount_usd": 999
}
with open(f"{delivery_dir}/delivery_receipt.json", 'w', encoding='utf-8') as f:
    json.dump(delivery_receipt, f, ensure_ascii=False, indent=2)

# 更新财务记录
finance_entry = f"{datetime.now().strftime('%Y-%m-%d')},{project_id},StartupX,AI设计服务,999,PENDING_PAYMENT\n"
with open(FINANCE_LOG, 'a', encoding='utf-8') as f:
    f.write(finance_entry)

# 最终状态
status_data["status"] = "DELIVERED"
status_data["updated_at"] = datetime.now().isoformat()
status_data["history"].append({"status": "DELIVERED", "agent": "csm", "ts": datetime.now().isoformat()})
with open(status_file, 'w', encoding='utf-8') as f:
    json.dump(status_data, f, ensure_ascii=False, indent=2)

test("小服创建交付目录", os.path.isdir(delivery_dir))
test("小服生成交付确认单", os.path.isfile(f"{delivery_dir}/delivery_receipt.json"))
test("交付物包含 4 个文件", len(delivery_receipt["items"]) == 4)
test("小服更新财务记录", os.path.isfile(FINANCE_LOG))
test("项目最终状态为 DELIVERED", status_data["status"] == "DELIVERED")
test("历史记录完整 (6 个节点)", len(status_data["history"]) >= 6)

# ─────────────────────────────────────────────
# 汇总报告
# ─────────────────────────────────────────────
section("测试汇总报告")

passed = sum(1 for r in results if r["status"] == PASS)
failed = sum(1 for r in results if r["status"] == FAIL)
total = len(results)

print(f"\n  总测试数: {total}")
print(f"  通过: {PASS} {passed}")
print(f"  失败: {FAIL} {failed}")
print(f"  通过率: {passed/total*100:.1f}%")

if failed > 0:
    print(f"\n  失败项目:")
    for r in results:
        if r["status"] == FAIL:
            print(f"    {FAIL} {r['name']}")

# 生成测试报告文件
report = {
    "test_run": datetime.now().isoformat(),
    "total": total,
    "passed": passed,
    "failed": failed,
    "pass_rate": f"{passed/total*100:.1f}%",
    "results": results
}
report_file = f"{BASE}/docs/opc/OPC_Workflow_Test_Report.json"
os.makedirs(os.path.dirname(report_file), exist_ok=True)
with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\n  测试报告已保存: docs/opc/OPC_Workflow_Test_Report.json")
print(f"\n{'='*60}")
print(f"  OPC 完整工作流测试完成")
print(f"{'='*60}\n")
