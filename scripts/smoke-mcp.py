#!/usr/bin/env python3
"""验证 MCP Adapter → Gateway → Hindsight 的真实工具链。"""

import asyncio
import json
import time

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "http://127.0.0.1:8000/mcp"
TEST_FACT = "外置记忆第一阶段优先测试手动调用效率。"


async def call(session: ClientSession, name: str, arguments: dict) -> None:
    started = time.perf_counter()
    result = await session.call_tool(name, arguments=arguments)
    elapsed = round((time.perf_counter() - started) * 1000, 1)
    print(f"\n{name}: {elapsed} ms")
    if result.isError:
        raise RuntimeError(f"{name} failed: {result.content}")
    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        print(json.dumps(structured, ensure_ascii=False, indent=2))
    else:
        print(result.content)


async def main() -> None:
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream, *_):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            required = {"memory_retain", "memory_recall", "memory_reflect"}
            missing = required - set(names)
            if missing:
                raise RuntimeError(f"缺少 MCP tools: {sorted(missing)}")
            print(f"[✓] MCP tools: {', '.join(sorted(required))}")

            await call(session, "memory_retain", {"content": TEST_FACT})
            await call(session, "memory_recall", {"query": "外置记忆第一阶段优先测试什么？", "max_results": 5})
            await call(session, "memory_reflect", {"query": "为什么外置记忆第一阶段先测试手动调用效率？"})

    print("\n[✓] MCP Adapter → Gateway → Hindsight 三条核心路径已完成调用。")


if __name__ == "__main__":
    asyncio.run(main())
