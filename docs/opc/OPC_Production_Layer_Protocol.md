# OPC 生产层双团队协同协议 (Production Layer Protocol)

> 本文档定义了龙虾军团内部（设计团队与开发团队）在 OPC 商业闭环中的协同机制，确保从设计到开发的无缝衔接。

---

## 1. 生产层整体工作流

当公司层（小销）触发生产（`PRODUCTION_STARTED`）后，龙虾军团接管项目，执行以下流程：

```
[公司层触发]
active_projects/P-XXX/status.json -> current_status: "PRODUCTION_STARTED"

[CoS 调度]
CoS 读取 brief.md
    → 拆解为设计任务和开发任务
    → 更新状态: DESIGNING

[设计团队执行]
小管 (ProjectManager) 接单
    → 小研 (调研) → 小策 (线框图) → 小设 (视觉稿) → 小文 (文案) → 小牌 (品牌审核)
    → 产出物写入: 3_production/shared_workspace/design_handoffs/P-XXX/
    → 更新状态: DEVELOPING

[开发团队执行]
CTO 接单
    → 读取 design_handoffs/P-XXX/ 中的设计稿和标注
    → BE (后端 API) → FE (前端页面，对接设计稿)
    → QA (自动化测试)
    → 产出物写入: 4_operations/deliverables/P-XXX/
    → 更新状态: READY_FOR_DELIVERY

[交还公司层]
小服 (CSM) 监听到 READY_FOR_DELIVERY，接管项目进行交付。
```

---

## 2. 跨团队交接规范 (Design Handoff Spec)

设计团队与开发团队之间**不通过自然语言沟通**，完全通过结构化文件进行交接。交接目录为：`3_production/shared_workspace/design_handoffs/P-XXX/`

### 2.1 必须包含的交接文件

设计团队（小运）在完成设计后，必须在该目录下生成以下 4 类文件，开发团队（FE）才能开始工作：

1. **`design_tokens.json`** (设计令牌)
   - 包含所有全局颜色、字体、间距、阴影等变量。
   - FE 将直接读取此文件生成 Tailwind 配置。

2. **`assets/`** (切图资源)
   - 包含所有导出的图片、图标（SVG/PNG/WebP）。
   - 命名规范：`[类型]_[位置]_[名称].[格式]`，如 `icon_header_logo.svg`。

3. **`layout_specs.md`** (布局与交互标注)
   - 详细说明每个区块的 Flex/Grid 布局结构。
   - 说明 Hover、Click 等交互动画效果。

4. **`copywriting.json`** (文案映射表)
   - 包含页面上所有的文本内容，按区块结构化。
   - FE 将直接读取此文件渲染文本，实现文案与代码解耦。

### 2.2 交接文件示例

**`design_tokens.json` 示例：**
```json
{
  "colors": {
    "primary": "#4F46E5",
    "secondary": "#10B981",
    "background": "#F9FAFB",
    "text_main": "#111827"
  },
  "typography": {
    "font_family_sans": "Inter, sans-serif",
    "h1": { "size": "3.75rem", "weight": "800", "line_height": "1.2" }
  }
}
```

**`copywriting.json` 示例：**
```json
{
  "hero_section": {
    "headline": "Build your OPC in 72 hours",
    "subheadline": "The only multi-agent OS you need.",
    "cta_primary": "Get Started",
    "cta_secondary": "Book a Demo"
  }
}
```

---

## 3. 异常与打回机制 (Feedback Loop)

在生产过程中，如果开发团队发现设计稿存在问题（如缺少切图、逻辑不通），触发打回机制：

1. **FE 发现问题**：在 `design_handoffs/P-XXX/` 下创建 `ISSUE_REPORT.md`，详细描述缺失或错误的内容。
2. **状态回退**：FE 将 `status.json` 的状态从 `DEVELOPING` 改回 `DESIGNING`。
3. **设计团队返工**：小管监听到状态回退，读取 `ISSUE_REPORT.md`，安排小设/小文修复。
4. **重新交接**：修复完成后，小运更新交接文件，删除 `ISSUE_REPORT.md`，将状态改回 `DEVELOPING`。

---

## 4. 交付物打包规范

开发团队（Ops）在完成所有工作后，必须将最终产物打包到 `4_operations/deliverables/P-XXX/` 目录，供小服 (CSM) 发送给客户。

**交付物目录结构：**
```
4_operations/deliverables/P-XXX/
├── source_code.zip          ← 完整的前后端源代码
├── design_assets.zip        ← 原始设计稿与切图
├── deployment_guide.md      ← 部署说明文档
└── README.md                ← 项目总结与使用说明
```

*注：当 `source_code.zip` 生成完毕后，Ops 才能将状态更新为 `READY_FOR_DELIVERY`。*
