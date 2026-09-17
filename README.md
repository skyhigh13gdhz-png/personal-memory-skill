# Personal Memory Skill

面向 AI 客户端的个人外置记忆**使用策略层**。本仓只保留 Skill 本身，不部署服务器、不保存 Token、不实现 MCP Server。

## 职责

- 用户明确要求“记住/记录” → 调用 `memory_retain`；
- 查询过去事实、决定、进度、历史讨论 → 调用 `memory_recall`；
- 需要综合多条长期记忆 → 调用 `memory_reflect`；
- 只有收到工具真实成功结果后，才能告诉用户已经写入；
- 普通闲聊不主动增加记忆开销。

## 架构

```text
AI Client
   ↓
Personal Memory Skill       ← 本仓：调用策略
   ↓ MCP
Memory MCP                  ← 独立 memory-mcp 仓：协议适配与部署
   ↓ HTTP
Memory Gateway
   ↓
Hindsight
```

服务端 MCP 的源码、systemd、一键部署、smoke test 全部属于 `memory-mcp`，不放在本仓。

## 第一阶段验收目标

先手动调用，不做项目级自动触发。真实测清：

1. 一次记住/回忆需要多少用户操作；
2. Retain / Recall / Reflect 端到端耗时；
3. 返回结果相关性；
4. 连续使用是否存在明显等待或额外摩擦。

只有手动链路足够高效，才继续自动触发、Raw Store 等后续层。

## 当前状态

- [x] Skill 与服务端职责拆分；
- [x] 第一版 `SKILL.md`；
- [x] MCP Server 已迁移到独立 `memory-mcp` 仓；
- [ ] Memory MCP 旧 VPS runtime 验证；
- [ ] 安全公网 MCP 接入；
- [ ] ChatGPT 实际手动调用；
- [ ] 真实用户体感与端到端性能验收。
