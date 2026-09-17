# 第一阶段端到端验收

## 目标

判断 Personal Memory 是否真的适合日常使用，而不是只判断接口能否跑通。

## 三条测试路径

### 1. Retain

用户：`记住：外置记忆第一阶段优先测试手动调用效率。`

期望：
- 只发生一次必要的写入路径；
- Gateway 返回真实成功结果后才能确认“已记录”；
- 随后 Recall 可以找回该事实。

### 2. Recall

用户：`查一下我的记忆：外置记忆第一阶段优先测试什么？`

期望：
- 使用 Recall，不使用 Reflect；
- 找回刚才 Retain 的核心事实；
- 不要求用户填写 bank、ID、接口名等技术参数。

### 3. Reflect

用户：`结合以前的记忆，分析我们为什么先测试手动调用，而不是先做自动触发。`

期望：
- 使用 Reflect；
- 能综合多条相关记忆；
- 明确记录 Memory LLM 带来的额外耗时。

## 必须记录的数据

每次测试至少记录：

| 字段 | 含义 |
|---|---|
| operation | retain / recall / reflect |
| user_actions | 用户额外操作次数 |
| total_ms | 从触发到结果回到 ChatGPT 的总耗时 |
| gateway_ms | Gateway 自身处理耗时 |
| hindsight_ms | Hindsight 调用耗时 |
| result_ok | 结果是否正确 |
| friction | 是否出现确认、重复选择、参数输入等摩擦 |

## 第一阶段判断原则

- HTTP 成功不等于体验成功。
- Recall 是高频路径，必须优先追求低延迟。
- Reflect 是深度路径，可以比 Recall 慢，但必须单独统计，不能混淆。
- 如果每次都需要多步选择、重复授权或明显等待，即使功能正确也判定为体验问题。
- 不为了保住既有架构而美化测试结果；如果链路效率差，应重新评估 Gateway/Hindsight 或客户端接入方式。
