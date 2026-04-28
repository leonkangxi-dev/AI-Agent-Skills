---
name: business-trip-auditor
description: 出差财务记账助手 — 解析发票/收据/事由，写入 Travel_Logs 月报，并在每月汇总中分类统计
triggers: ["出差", "发票", "差旅", "报销", "本月出差明细", "出差汇总"]
tags: ["obsidian", "finance", "travel", "expense"]
---

# Business_Trip_Auditor 出差财务审计技能

## 触发条件
- 用户发送发票图片、收据、或费用事描述时
- 用户询问"本月出差明细"、"X月出差汇总"等查询指令

## 核心路径
- **Obsidian 根目录：** `~/Documents/Obsidian/`
- **出差日志目录：** `~/Documents/Obsidian/Projects/Finance/Travel_Logs/`
- **每月归档：** `Travel_Logs/YYYY-MM.md`（按年月命名）

---

## 记账动作流程

### Step 1：解析信息
从用户输入中提取：
- `日期`（必填）
- `出差人`
- `目的地`
- `事由`
- `费用明细`：交通、住宿、餐饮、其他
- `发票状态`：✅已收 / ❌未收
- `支付方式`：现金/微信/支付宝/银行卡/公司信用卡
- `备注`

### Step 2：写入 Obsidian
写入路径：`~/Documents/Obsidian/Projects/Finance/Travel_Logs/YYYY-MM.md`

### Step 3：追加到月报
将单笔记录追加到当月 `.md` 文件底部。

### Step 4：完成提醒
回复用户：
> ✅ 账目已写入 Obsidian：`Projects/Finance/Travel_Logs/YYYY-MM.md`
> 请在 GitHub Desktop 中提交变更以完成云端备份。

---

## 查询动作流程

当用户询问"本月出差明细"时：

### Step 1：扫描当月文件
路径：`~/Documents/Obsidian/Projects/Finance/Travel_Logs/YYYY-MM.md`

### Step 2：分类汇总
按以下维度汇总：
- 按出差人统计
- 按目的地统计
- 按费用类别统计
- 发票汇总（已收/未收）
- 总计金额

### Step 3：输出格式
```
## YYYY年MM月出差明细

| 日期 | 出差人 | 目的地 | 事由 | 金额 | 发票 |
|------|--------|--------|------|------|------|
| ... | ... | ... | ... | ¥X | ✅/❌ |

**本月合计：** ¥X 元
**发票已收：** X / Y 张
```

---

## 字段规范
- 金额单位：**元（人民币）**
- 日期格式：`YYYY-MM-DD`
- 货币：默认 RMB，若外币需标注汇率
- 未提供的信息字段留空，不虚构

## 发票图片处理
- 若用户发送发票截图，保存至：`~/Documents/Obsidian/Projects/Finance/Attachments/YYYY-MM/`
- 在对应记录中用 `📎` 标注附件路径

### ⚠️ OCR 识别注意事项（经验总结）

**图片识别已知局限：**
- `vision_analyze` 工具在当前 session 中无法识别通过 `/Users/jiang/.hermes/image_cache/` 路径的图片（文件存在但工具报告"看不到"）
- tesseract 终端命令在 macOS 上对中文发票识别率低（可能缺少 chi_sim 训练数据，或图片为拍照扫描导致对比度不足）

**PDF 发票处理（推荐）：**
- PDF 发票用 `pdftotext` 命令提取文本，准确率接近 100%：
  ```bash
  pdftotext "/path/to/invoice.pdf" -
  ```
- `vision_analyze` 无法处理 PDF 文件（只支持图片）
- `pdfminer` Python 库可作为备选：
  ```python
  from pdfminer.high_level import extract_text
  text = extract_text("/path/to/invoice.pdf")
  ```

**推荐工作流：**
1. 用户发送发票图片后，先将图片保存到缓存（`~/.hermes/image_cache/` 目录已自动缓存）
2. 直接请用户口述发票金额/关键信息（最快最准）
3. 如必须 OCR，优先尝试 `tesseract` 并指定 `-l chi_sim+eng`，若输出为空则人工询问
4. 图片作为附件存档，供后续人工复核

**图片文件路径规律：**
- Telegram 图片缓存：`/Users/jiang/.hermes/image_cache/img_<hash>.jpg`
- 文件大小 > 0 表示上传成功，可直接引用

---

*由 Hermes Agent 自动生成 | 出差财务助手协议*
