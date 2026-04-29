# 用 LLM + Obsidian 构建个人知识库

## 来源链接
https://x.com/yanhua1010/status/2039966047378583815

## 核心摘要
基于 Karpathy 的"LLM Knowledge Bases"工作流，介绍如何用 LLM 编译 Obsidian 笔记库。核心概念：把原始资料"编译"成结构化知识。

## 关键内容

### 核心类比
- Obsidian Vault = 代码仓库
- LLM = 编译器
- 过程 = 编译（Compile）

### 软件工程 vs 知识库工程
```
软件工程          →  知识库工程
src/              →  raw/（原始资料）
build/            →  wiki/（知识条目）
logs/             →  outputs/（问答归档）
编译器             →  LLM
IDE               →  Obsidian
Lint / CI         →  健康检查
```

### 核心三件事
1. **分层**：原始资料、编译产物、运行时输出三层分开
2. **增量**：不用每次全量重建，只处理新增/变更
3. **可追溯**：每个知识条目能追到原始来源

### 目录结构示例
```
Vault/
├── raw/          # 原始资料，不改
├── wiki/         # 编译产物，LLM 维护
└── outputs/      # 运行时输出
```

## 标签
#llm #obsidian #知识库 #karpathy #ai #笔记
