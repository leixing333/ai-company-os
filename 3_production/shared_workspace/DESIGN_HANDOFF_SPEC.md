# 设计交接规范 (Design Handoff Specification)

本规范定义了设计团队（小运）向开发团队（FE）交接设计资产的标准格式。**FE 在开工前必须检查以下三个文件是否存在，缺失则拒绝开工并触发 Escalation。**

---

## 交接目录结构

每个项目的设计资产必须存放在以下路径：

```
3_production/shared_workspace/design_handoffs/{Project_ID}/
├── assets/          # 所有导出的图片资产 (PNG/SVG/WebP)
│   ├── hero_bg.png
│   ├── logo.svg
│   └── ...
├── tokens.json      # Design Tokens（颜色、字体、间距）
├── layout.md        # 页面结构的 Markdown 描述（各区块内容与层级）
└── HANDOFF_READY    # 空文件，由小运创建，表示交接完成
```

---

## tokens.json 标准格式

```json
{
  "colors": {
    "primary": "#4F46E5",
    "secondary": "#7C3AED",
    "background": "#FFFFFF",
    "text_primary": "#111827",
    "text_secondary": "#6B7280"
  },
  "typography": {
    "font_family": "Inter, sans-serif",
    "heading_size": "48px",
    "body_size": "16px",
    "line_height": "1.6"
  },
  "spacing": {
    "section_padding": "80px",
    "container_max_width": "1200px"
  }
}
```

---

## layout.md 标准格式

```markdown
# 页面布局：{Project_ID}

## Section 1: Hero
- 标题：[H1 文案]
- 副标题：[副标题文案]
- CTA 按钮：[按钮文案] -> [跳转到 #pricing]
- 背景图：assets/hero_bg.png

## Section 2: How it Works
- 三步流程：Subscribe / Request / Receive
- 每步包含图标和说明文字

## Section 3: Pricing
- 单一定价卡片：$999/次
- 包含功能列表和 CTA 按钮
```

---

## 验收规则

设计团队（小运）在完成交接时，必须确认：

1. `assets/` 目录下所有图片均已导出为 WebP 格式（兼容 PNG 备用）。
2. `tokens.json` 中的所有颜色值均为 HEX 格式。
3. `layout.md` 中每个 Section 都有对应的文案（不允许留空）。
4. 创建 `HANDOFF_READY` 空文件，触发 FE 开始工作。
