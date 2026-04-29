# Claude Code源码泄露分析

## 来源链接
https://x.com/alchainhust/status/2038944798816505991

## 核心摘要
花叔分析Claude Code 1902个源文件泄露事件，揭示harness engineering的核心设计

## 关键内容

### 事件背景
- Anthropic在更新npm包时不慎留下了60MB的source map调试文件
- 任何人都可以还原出Claude Code完整的TypeScript源码
- 这是Anthropic第二次犯同样的错误（2025年2月也发生过）

### Claude Code好用的原因
- 60%靠Opus模型本身的能力
- 40%靠围绕模型搭建的工程系统（harness）

### 8个核心设计发现

1. **System Prompt构建**
   - 静态部分（共享缓存）+ 动态部分（用户独立）
   - 每个MCP服务器固定消耗4000-6000 tokens

2. **四层安全权限系统**
   - 主AI + 独立AI分类器做安全审查
   - 熔断机制：连续3次被拒降级为手动确认

3. **记忆系统**
   - 只记偏好，不记代码（代码会变，记忆不更新）
   - 分为四类：user/feedback/project/reference
   - autoDream功能自动整理记忆

4. **9段式上下文压缩**
   - 核心请求、关键概念、文件和代码、错误修复、解决过程...
   - 所有用户消息必须完整保留

5. **虚拟宠物系统**
   - src/buddy/ 目录下未发布的宠物系统
   - 18种物种、6种眼睛样式、稀有度系统

6. **多Agent协作框架**
   - Team有Leader和多个Teammate
   - 支持三种执行方式（同进程/tmux/iTerm2）
   - 权限冒泡机制

7. **内部版vs外部版**
   - 内部版要求更严格（不写注释、诚实性、验证Agent）
   - 外部版要求简洁直接

8. **搜索用的是grep**
   - 最朴素的文本搜索，没有向量数据库
   - 原则：与其每个环节都复杂，不如一个环节足够强

### 源码仓库
https://github.com/instructkr/claude-code

## 标签
#claude #代码泄露 #harness #ai #工程设计 #安全系统
