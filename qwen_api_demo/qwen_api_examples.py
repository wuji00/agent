"""
基于阿里云 Model Studio Qwen 接口的 Python 示例。

- 采用与 OpenAI 兼容的 `/compatible-mode/v1/chat/completions` 端点。
- 通过不同函数演示常用推理参数的组合和差异。
- 所有示例都使用中文注释，便于快速对照官方文档。
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

import requests


class QwenClient:
    """简单的 Qwen HTTP 客户端封装。

    参数说明:
        api_key: 从环境变量或配置中心获得的 Bearer Token。
        base_url: 兼容 OpenAI 的 Chat Completions 端点。
    """

    def __init__(self, api_key: str | None = None, *, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY") or os.getenv("QWEN_API_KEY")
        if not self.api_key:
            raise RuntimeError("请在环境变量 DASHSCOPE_API_KEY 或 QWEN_API_KEY 中配置 API Key")

        # 文档提供的兼容模式地址，适合大多数聊天/推理调用。
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def chat(self, messages: List[Dict[str, str]], **params: Any) -> Dict[str, Any]:
        """非流式调用，返回完整 JSON。

        常用参数(详见官方参考):
            model: 指定模型名称，如 `qwen-plus`、`qwen-max`、`qwen-turbo` 等。
            temperature/top_p: 控制随机性与采样范围。
            max_tokens: 限制回复长度，防止超长输出。
            stop: 提前终止生成的停止词列表。
            presence_penalty/frequency_penalty: 惩罚重复，鼓励多样性。
            seed: 设定随机种子，便于结果复现。
        """

        payload = {"model": params.pop("model", "qwen-plus"), "messages": messages, **params}
        response = self.session.post(self.base_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def stream_chat(self, messages: List[Dict[str, str]], **params: Any) -> Iterable[Dict[str, Any]]:
        """流式推理示例，逐段读取返回的 SSE 数据行。

        - 设置 `stream=True` 后，接口会以 `data: ...` 的形式持续返回。
        - 本函数演示如何解析每行 JSON，并在遇到 `[DONE]` 时结束。
        """

        payload = {
            "model": params.pop("model", "qwen-plus"),
            "messages": messages,
            "stream": True,
            **params,
        }
        with self.session.post(self.base_url, json=payload, stream=True, timeout=30) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                if line.strip() == b"data: [DONE]":
                    break
                if not line.startswith(b"data: "):
                    continue
                chunk = json.loads(line[len(b"data: ") :])
                yield chunk


# ============================ 示例调用区域 ============================

def run_minimal_chat(client: QwenClient) -> Dict[str, Any]:
    """最小化示例：默认模型、默认温度，关注正确性和速度。"""

    messages = [
        {"role": "system", "content": "你是一位乐于解释的中文助理"},
        {"role": "user", "content": "简要介绍下阿里云 Model Studio 是什么？"},
    ]
    return client.chat(messages)


def run_precise_inference(client: QwenClient) -> Dict[str, Any]:
    """精确推理：降低随机性，限制回复长度。"""

    messages = [{"role": "user", "content": "给出 3 条适合初学者的 prompt 编写技巧。"}]
    return client.chat(
        messages,
        model="qwen-turbo",
        temperature=0.2,  # 越低越趋向确定性
        top_p=0.7,  # 限制采样范围，避免离谱答案
        max_tokens=256,
        presence_penalty=0.0,
        frequency_penalty=0.5,  # 惩罚重复，减少啰嗦
        seed=42,  # 固定随机种子，便于复现
    )


def run_creative_writing(client: QwenClient) -> Dict[str, Any]:
    """创意写作：提高温度和采样多样性。"""

    messages = [
        {"role": "system", "content": "请用活泼的语气"},
        {"role": "user", "content": "写一首关于云计算的四行短诗"},
    ]
    return client.chat(
        messages,
        model="qwen-plus",
        temperature=0.95,
        top_p=0.9,
        max_tokens=128,
    )


def run_stop_words_example(client: QwenClient) -> Dict[str, Any]:
    """使用 stop 词提前截断输出，便于格式控制。"""

    messages = [
        {
            "role": "user",
            "content": "按照“标题：\n内容：”的格式输出一段介绍，生成时遇到“内容：”后立即停止。",
        }
    ]
    return client.chat(
        messages,
        stop=["内容："],
        max_tokens=200,
    )


def run_streaming_demo(client: QwenClient) -> List[str]:
    """演示流式推理，将模型逐步输出的内容收集为字符串列表。"""

    messages = [
        {"role": "user", "content": "逐步解释大模型推理的温度与 top_p 的区别。"}
    ]
    chunks: List[str] = []
    for event in client.stream_chat(messages, temperature=0.6, top_p=0.8):
        # 每个 event 的结构与非流式类似，但内容在 choices 中分段出现
        delta = event.get("choices", [{}])[0].get("delta", {}).get("content")
        if delta:
            chunks.append(delta)
    return chunks


if __name__ == "__main__":
    # 提示：正式使用前请将 DASHSCOPE_API_KEY / QWEN_API_KEY 配置到环境变量。
    client = QwenClient()

    print("\n[1] 最小化调用示例")
    minimal = run_minimal_chat(client)
    print(json.dumps(minimal, ensure_ascii=False, indent=2))

    print("\n[2] 精确推理示例")
    precise = run_precise_inference(client)
    print(json.dumps(precise, ensure_ascii=False, indent=2))

    print("\n[3] 创意写作示例")
    creative = run_creative_writing(client)
    print(json.dumps(creative, ensure_ascii=False, indent=2))

    print("\n[4] stop 词截断示例")
    truncated = run_stop_words_example(client)
    print(json.dumps(truncated, ensure_ascii=False, indent=2))

    print("\n[5] 流式推理示例 (打印组装后的文本)")
    stream_chunks = run_streaming_demo(client)
    print("".join(stream_chunks))
