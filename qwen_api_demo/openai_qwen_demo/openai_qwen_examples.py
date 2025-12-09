"""使用 OpenAI Python SDK 调用通义千问 OpenAI 兼容接口的示例。

涵盖：
1. 纯文本对话（非流式与流式）。
2. 多模态（图文）对话。
3. 思考/推理型模型调用示例。

运行前请先设置环境变量：
- QWEN_OPENAI_BASE_URL：可选，默认为阿里云 DashScope OpenAI 兼容地址。
- QWEN_OPENAI_API_KEY：必填，阿里云控制台获取的 API Key。
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Iterable

from openai import OpenAI


# 允许用户通过环境变量覆盖 base_url，方便本地代理或不同地域的网关。
DEFAULT_BASE_URL = os.getenv(
    "QWEN_OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
)
DEFAULT_API_KEY = os.getenv("QWEN_OPENAI_API_KEY")


class QwenOpenAIClient:
    """轻量封装 OpenAI SDK，便于切换模型与参数。"""

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        if not (api_key or DEFAULT_API_KEY):
            raise RuntimeError(
                "请先在环境变量 QWEN_OPENAI_API_KEY 中配置 DashScope/通义千问的 API Key。"
            )
        self.client = OpenAI(base_url=base_url or DEFAULT_BASE_URL, api_key=api_key or DEFAULT_API_KEY)

    # -------- 纯文本示例 --------
    def basic_chat(self) -> str:
        """非流式对话：演示温度、top_p、stop、max_tokens 等常用参数。"""

        completion = self.client.chat.completions.create(
            model="qwen-plus",  # 可换为 qwen-turbo / qwen-max
            messages=[
                {"role": "system", "content": "你是一名精简、可靠的中文助理"},
                {"role": "user", "content": "用三句话解释温度与 top_p 的差异"},
            ],
            temperature=0.4,  # 降低随机性，保证回答稳定
            top_p=0.8,  # 核采样限制概率质量，避免过度发散
            max_tokens=240,  # 控制回复长度
            stop=["注意事项："],  # 命中后提前终止，控制格式
            seed=42,  # 固定随机种子，便于复现
            presence_penalty=0.1,  # 鼓励覆盖更多要点
            frequency_penalty=0.2,  # 减少重复措辞
        )
        return completion.choices[0].message.content or ""

    def streaming_chat(self) -> str:
        """流式对话：演示边生成边消费，适合实时渲染。"""

        stream = self.client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "以对话语气回答"},
                {"role": "user", "content": "推荐 3 本适合周末放松的科幻小说"},
            ],
            stream=True,
            temperature=0.8,
            top_p=0.9,
        )
        # 按增量片段组装完整回复
        chunks: Iterable[str] = (
            chunk.choices[0].delta.content or "" for chunk in stream if chunk.choices
        )
        return "".join(chunks)

    # -------- 多模态示例 --------
    def multimodal_chat(self, image_path: str | Path | None = None) -> str:
        """图文对话：向通义千问多模态模型发送图片与文本提示。"""

        # 如果未提供图片，则使用内置的 1x1 白色 PNG base64（尺寸极小，方便示例）。
        if image_path:
            image_bytes = Path(image_path).read_bytes()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        else:
            image_base64 = (
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/P6N6GAAAAABJRU5ErkJggg=="
            )

        completion = self.client.chat.completions.create(
            model="qwen-vl-plus",  # 通义千问多模态模型（图文理解）
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请描述图片颜色，并给一句小诗"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                        },
                    ],
                }
            ],
            max_tokens=200,
        )
        return completion.choices[0].message.content or ""

    # -------- 思考/推理模型示例 --------
    def reasoning_chat(self) -> str:
        """调用加强推理/思考的模型，通过思维链提示引导更详尽的中间推导。"""

        completion = self.client.chat.completions.create(
            # 若控制台开通了“思考/推理”型号，可替换为官方提供的名称，例如 qwen-max 或 qwen-max-0403。
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": "你是一名谨慎的数学助理，回答前会逐步推理并检查答案。",
                },
                {
                    "role": "user",
                    "content": "一家咖啡店每杯拿铁售价 32 元，今日卖出 87 杯，原料成本占售价的 35%，净利润是多少？",
                },
            ],
            temperature=0.2,  # 降低随机性，强调严谨性
            max_tokens=300,
            # openai 兼容接口的思考模型通常支持返回推理过程，可通过 system 提示要求“先思考再给最终答案”。
        )
        return completion.choices[0].message.content or ""


def main() -> None:
    client = QwenOpenAIClient()

    print("【非流式】温度/Top-P/停止词示例：")
    print(client.basic_chat())
    print("\n【流式】增量输出示例：")
    print(client.streaming_chat())
    print("\n【多模态】图文理解示例：")
    print(client.multimodal_chat())
    print("\n【思考模型】逐步推理示例：")
    print(client.reasoning_chat())


if __name__ == "__main__":
    main()
