# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: Code Agent (编程助手)
记得你的习惯，更懂你的代码，无缝衔接你的每一次灵感

最佳实践说明：
1. 客户端和 Collection 初始化：
   - 客户端和 Collection 建议在应用启动时初始化一次，全局复用
   - 避免在每次请求时重复创建，可以显著降低调用成本

2. 批量添加会话：
   - 建议收集多条消息后批量调用 add_session，而非每条消息单独调用
   - 可以减少网络往返次数，降低延迟和成本

3. 调用间隔控制：
   - add_session 调用后建议等待 30 秒再进行下一次操作
   - 给服务端足够时间处理和索引数据，避免并发冲突

4. 搜索优化：
   - 使用 search_event_memory 和 search_profile_memory 分别搜索
   - 只在需要时调用对应的搜索方法，避免不必要的查询
   - 合理设置 limit 参数，避免返回过多数据

 5. Session 管理：
    - 相同用户的多轮对话建议使用相同的 session_id
    - 便于服务端关联和检索相关上下文
"""

import os
import time

from vikingdb import IAM
from vikingdb.memory import VikingMem


YOUR_COLLECTION_NAME = "your_collection_name"

EVENT_TEMPLATES = []
PROFILE_TEMPLATES = ["profile_code_agent_v1"]


_auth = IAM(
    ak=os.getenv("VIKINGDB_AK", "your_ak"),
    sk=os.getenv("VIKINGDB_SK", "your_sk"),
)
client = VikingMem(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    region="cn-beijing",
    auth=_auth,
    scheme="http",
)

collection = client.get_collection(collection_name=YOUR_COLLECTION_NAME)


def add_code_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {
            "role": "system",
            "content": "你是编程助手（Code Agent）。你会记住用户的代码风格与习惯：偏好小步迭代、先跑通再优化、输出可复制的最小可用代码。沟通风格：vibe coding——快速、直接、边写边试、用TODO推进。默认：Python 3.11；允许给出替代实现与权衡，但不要长篇说教。",
        },
        {
            "role": "user",
            "content": "我想做一个超轻量的命令行工具：把一个目录里的所有 .md 文件合并成一个 docs.md，并生成目录（TOC）。不需要很完美，但要能用。你带我 vibe coding 一下。",
        },
        {
            "role": "assistant",
            "content": "OK，vibe 起来：先做 **MVP**（能跑、输出正确），然后再加 TOC。\n\n**目标**\n- 输入：`root_dir`\n- 找到所有 `*.md`（递归）\n- 合并成 `docs.md`\n- 每个文件加一个二级标题做分隔（用相对路径当标题）\n- 生成简单 TOC（链接到标题锚点）\n\n先问你两个偏好（不影响开写）：\n1) 合并顺序：按文件名排序可以吗？\n2) 要不要跳过 `README.md` 或 `_build/`、`.git/` 这类目录？\n\n我先按按路径排序 + 跳过隐藏目录写最小版。",
        },
        {
            "role": "assistant",
            "content": '先上可跑代码：`merge_md.py`。你复制保存后跑一下：\n\n```python\n#!/usr/bin/env python3\nfrom __future__ import annotations\n\nimport argparse\nimport re\nfrom pathlib import Path\n\n\ndef slugify_heading(text: str) -> str:\n    # GitHub 风格锚点的极简近似：小写，非字母数字变 -，压缩连续 -\n    s = text.strip().lower()\n    s = re.sub(r"[^a-z0-9\\u4e00-\\u9fff]+", "-", s)\n    s = re.sub(r"-+", "-", s).strip("-")\n    return s or "section"\n\n\ndef iter_md_files(root: Path) -> list[Path]:\n    files = []\n    for p in root.rglob("*.md"):\n        if not p.is_file():\n            continue\n        # 跳过隐藏目录（.git/.xxx）\n        if any(part.startswith(".") for part in p.relative_to(root).parts):\n            continue\n        files.append(p)\n    return sorted(files, key=lambda x: str(x).lower())\n\n\ndef merge(root: Path, out: Path) -> None:\n    md_files = iter_md_files(root)\n\n    toc_lines: list[str] = ["# 目录\\n"]\n    body_lines: list[str] = []\n\n    for f in md_files:\n        rel = f.relative_to(root).as_posix()\n        title = rel.removesuffix(".md")\n        anchor = slugify_heading(title)\n\n        toc_lines.append(f"- [{title}](#{anchor})\\n")\n\n        body_lines.append(f"\\n\\n## {title}\\n")\n        body_lines.append(f"<!-- source: {rel} -->\\n\\n")\n        body_lines.append(f.read_text(encoding="utf-8", errors="replace"))\n        body_lines.append("\\n")\n\n    content = "".join(toc_lines) + "\\n" + "".join(body_lines)\n    out.write_text(content, encoding="utf-8")\n\n\ndef main():\n    ap = argparse.ArgumentParser(description="Merge markdown files into one with a simple TOC")\n    ap.add_argument("root", type=str, help="root directory")\n    ap.add_argument("--out", type=str, default="docs.md", help="output markdown")\n    args = ap.parse_args()\n\n    root = Path(args.root).resolve()\n    out = Path(args.out).resolve()\n    if not root.exists() or not root.is_dir():\n        raise SystemExit(f"root not found: {root}")\n\n    merge(root, out)\n    print(f"Merged {len(md_files)} files to {out}")\n\n\nif __name__ == "__main__":\n    main()\n```',
        },
        {
            "role": "user",
            "content": "我跑了，能合并，但 TOC 有些跳不过去，可能是中文标题锚点不一致。",
        },
        {
            "role": "assistant",
            "content": '懂了：不同渲染器对中文锚点规则不一致。我们先用**稳妥方案**：不赌渲染器的自动的锚点，直接插入显式 HTML 锚点。\n\n改法很小：\n- TOC 链接用 `#sec-<hash>`\n- 每个 section 前插入 `<a id="sec-..."></a>`\n\n我给你一个极简 patch（把 anchor 生成改成稳定哈希）：\n\n```python\nimport hashlib\n\ndef stable_anchor(text: str) -> str:\n    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]\n    return f"sec-{h}"\n```\n\n然后循环里`把 anchor = slugify_heading(title)` 换成：\n```python\nanchor = stable_anchor(title)\n```\n\n并在写标题前插入：\n```python\nbody_lines.append(f"\\n\\n<a id=\\"{anchor}\\"></a>\\n")\nbody_lines.append(f"\\n## {title}\\n")\n```\n\n你改完再跑一次，TOC 应该 100% 能跳。\n\n下一步你想加哪个 vibe 功能？（选一个）\n1) `--exclude` 支持多次传参\n2) README 优先合并（每个目录 README 放最前）\n3) 支持把一级标题统一成 `#`、二级 `##`（避免层级乱）',
        },
    ]

    result = collection.add_session(
        session_id="code_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_code_001",
            "default_user_name": "Developer",
            "default_assistant_id": "assistant_code_001",
            "default_assistant_name": "Code Agent",
            "time": now_ts,
        },
    )

    return result


def search_code_memories():
    event_result = None
    profile_result = None

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_code_001",
            "assistant_id": "assistant_code_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== Code Agent Best Practice ===\n")

    print("Step 1: Adding code session...")
    add_result = add_code_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching code memories...")
    search_result = search_code_memories()
    print(f"Search result: {search_result}\n")

    print("✅ Code Agent workflow completed")
