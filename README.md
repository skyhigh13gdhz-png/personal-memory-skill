# Personal Memory Skill

面向 AI 客户端的个人外置记忆接入层。

当前第一阶段只验证一件事：

> ChatGPT 手动触发记忆能力 → Memory Gateway → Hindsight → 返回 ChatGPT

目标不是证明“能用”，而是测清楚整条链路是否足够快、足够省操作，值得长期日常使用。

## 第一阶段范围

- `retain`：明确要求“记住/记录”时写入外置记忆。
- `recall`：查询历史事实、决定、进度和讨论。
- `reflect`：需要综合多条长期记忆时使用。
- 不做项目级自动触发。
- 不做每轮自动 Recall/Retain。
- 不在仓库保存 Gateway Token、个人记忆、服务器凭据或其他秘密。

## 架构

```text
ChatGPT
   ↓ 手动触发 Skill / App
Personal Memory Skill
   ↓
Memory App / MCP Adapter
   ↓ HTTPS
Memory Gateway
   ↓
Hindsight
   ↓
Memory LLM
```

Skill 负责工作流与调用规则；真正访问外部 Gateway 需要 ChatGPT 可调用的 App/MCP 工具。Gateway 和 Hindsight 保持独立。

## 验收重点

不是只看 HTTP 200，而是记录：

1. 用户为了“记住一次/回忆一次”需要几步操作；
2. Retain / Recall / Reflect 的端到端耗时；
3. Gateway 与 Hindsight 各自耗时；
4. 返回结果是否足够相关；
5. 连续使用时是否出现明显等待、重复确认或其他摩擦。

## 当前状态

- [x] 仓库建立
- [x] 第一版 `SKILL.md`
- [x] 明确 Skill 与外部 App/MCP 的职责边界
- [ ] Gateway 暴露 ChatGPT 可调用的 MCP 接口
- [ ] 安全远程连接方式
- [ ] ChatGPT 实际安装/调用
- [ ] Retain / Recall / Reflect 端到端性能测试

> 注意：ChatGPT 的 Skills、Custom Apps 和完整 MCP 能力受套餐、workspace、surface 和 rollout 影响。仓库本身不假设某个 ChatGPT 套餐一定支持写入型 MCP。
