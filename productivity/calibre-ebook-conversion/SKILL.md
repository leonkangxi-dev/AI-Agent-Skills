---
name: calibre-ebook-conversion
description: Calibre 安装与使用流程（macOS 电子书格式转换 AZW3/MOBI → EPUB）
category: productivity
---
# Calibre 电子书转换（macOS）

## 使用场景
将 AZW3/MOBI/EPUB 等格式相互转换，支持直接用 Apple Books 打开阅读。

## 安装
```bash
brew install --cask calibre
```

## 转换命令
```bash
# AZW3 → EPUB
ebook-convert "书名.azw3" "书名.epub"

# MOBI → EPUB
ebook-convert "书名.mobi" "书名.epub"

# 直接用 Apple Books 打开
open -a Books ~/Desktop/ebook/*.epub
```

## 注意事项
- **不要使用 `--embed-fonts` 参数**（该参数不存在，会报错）
- 书名有空格时必须用引号包裹路径
- 批量转换建议逐个执行，避免路径解析问题
- Calibre GUI 也可直接拖拽转换

## 验证
转换完成后确认输出文件存在：
```bash
ls -lh ~/Desktop/ebook/*.epub
```

## 相关工具
- Apple Books（系统自带，支持 EPUB）
- Kindle App（支持 MOBI/AZW3/EPUB）
