# ChatGPT 接入说明

## 关键边界

`SKILL.md` 负责告诉 ChatGPT **什么时候、为什么、以什么方式**使用个人记忆；它本身不等于一个可访问外部 HTTP API 的连接器。

要访问 Memory Gateway，需要 ChatGPT 能调用的外部工具层：

```text
Skill
  ↓
ChatGPT App / MCP tool
  ↓
Memory Gateway
  ↓
Hindsight
```

因此第一阶段真正需要打通的是 **Skill + MCP Adapter + Gateway + Hindsight**，而不是让 Skill 在说明文件里硬编码服务器 URL 或 Token。

## 安全原则

- Gateway 继续只在本机回环地址监听；不直接把 `8787` 暴露公网。
- Hindsight `8888` 永不直接暴露给 ChatGPT。
- Token、OAuth Secret、服务器凭据不进入 Git。
- 如果采用公网 HTTPS，只暴露受认证的 MCP/入口层。
- 如果 ChatGPT 当前 surface 支持 Secure MCP Tunnel，可优先评估 tunnel，避免直接暴露 Gateway。

## 套餐/Surface 现实约束

OpenAI 当前的 Skills、Custom Apps、完整 MCP 写入能力并非所有套餐和 surface 都一致。正式验收前必须以实际 ChatGPT 账号 UI 为准确认：

1. 能否安装/手动选择该 Skill；
2. 能否创建或连接自定义 App/MCP；
3. MCP 是否允许 `retain` 这种写入动作；
4. 当前测试是在 Web 还是其他客户端。

不要因为仓库代码完成就声称 ChatGPT 端链路已经完成。

## 第一阶段用户体验

理想调用：

- `记住这个：...`
- `查一下我的记忆：...`
- `结合以前的记忆想一下：...`

用户不应看到或填写 `bank_id`、Gateway Token、Hindsight URL 等内部参数。
