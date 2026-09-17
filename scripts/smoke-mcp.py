#!/usr/bin/env python3
"""验证 MCP Adapter → Gateway → Hindsight 的真实工具链。"""

import asyncio
import json
import time

from mcp import Client

MCP_URL = "http://127.0.0.1:8000/mcp"
TEST_FACT = "外置记忆第一阶段优先测试手动调用效率。"


async def call(client: Client, name: str, arguments: dict) -> None:
    started = time.perf_counter()
    result = await client.call_tool(name, arguments)
    elapsed = round((time.perf_counter() - started) * 1000, 1)
    print(f"\n{name}: {elapsed} ms")
    if result.is_error:
        raise RuntimeError(f"{name} failed: {result.content}")
    if result.structured_content is not None:
        print(json.dumps(result.structured_content, ensure_ascii=False, indent=2))
    else:
        print(result.content)


async def main() -> None:
    async with Client(MCP_URL) as client:
        tools = await client.list_tools()
        names = [tool.name for tool in tools.tools]
        required = {"memory_retain", "memory_recall", "memory_reflect"}
        missing = required - set(names)
        if missing:
            raise RuntimeError(f"缺少 MCP tools: {sorted(missing)}")
        print(f"[✓] MCP tools: {', '.join(sorted(required))}")

        await call(client, "memory_retain", {"content": TEST_FACT})
        await call(client, "memory_recall", {"query": "外置记忆第一阶段优先测试什么？", "max_results": 5})
        await call(client, "memory_reflect", {"query": "为什么外置记忆第一阶段先测试手动调用效率？"})

    print("\n[✓] MCP Adapter → Gateway → Hindsight 三条核心路径已完成调用。")


if __name__ == "__main__":
    asyncio.run(main())
