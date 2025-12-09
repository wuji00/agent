# Qwen API Python 示例与推理参数教程

本示例基于[阿里云 Model Studio Qwen API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference)编写，提供兼容 OpenAI Chat Completions 的 Python 代码，演示不同推理参数的组合与效果，并附上中文说明。

## 文件结构
- `qwen_api_examples.py`：包含 QwenClient 封装与多组参数示例（非流式与流式）。
- `notes.md`：编写过程中的工作记录。

## 环境准备（推荐使用 uv）
> 若尚未安装 [uv](https://github.com/astral-sh/uv)，可先执行 `pip install --upgrade uv`，或参考官方安装脚本。

1. 创建虚拟环境并激活：
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
   ```
2. 安装依赖：
   ```bash
   uv pip install requests
   ```
3. 配置密钥（两者取其一）：
   ```bash
   export DASHSCOPE_API_KEY="你的_API_Key"
   # 或
   export QWEN_API_KEY="你的_API_Key"
   ```

> 如果你已经有现成的虚拟环境，也可以直接在该环境里运行 `uv pip install requests`。

## 快速运行
直接运行脚本即可按顺序演示所有示例：
```bash
python qwen_api_examples.py
```

## 推理参数教程
以下参数均可在 `QwenClient.chat` 或 `QwenClient.stream_chat` 中传入，核心组合示例可在 `qwen_api_examples.py` 中查看。

### 1. 模型选择 `model`
- 常见取值：`qwen-turbo`（性价比）、`qwen-plus`（平衡）、`qwen-max`（高质量）。
- 影响回答质量、时延与费用，脚本中默认值为 `qwen-plus`。

### 2. 温度 `temperature`
- 作用：控制随机性，范围通常在 0~2。
- 低温度（如 0.2）：输出稳定、可复现，适用于精确问答。见 `run_precise_inference`。
- 高温度（如 0.95）：输出多样、富有创意，适用于写作。见 `run_creative_writing`。

### 3. 采样范围 `top_p`
- 作用：核采样限制概率质量总和，取值 0~1。
- 较低值（如 0.6~0.8）可减少离谱答案；较高值（0.9）提升想象力。
- 常与 `temperature` 联合调节，避免同时取极端值。

### 4. 最大长度 `max_tokens`
- 作用：限制返回 Token 数，防止输出过长或超额计费。
- 说明：包含所有 role 的最终回复长度，不含历史消息。
- 示例：`run_precise_inference` 与 `run_creative_writing` 将其限制在 128~256 之间。

### 5. 停止词 `stop`
- 作用：当模型生成的文本包含列表中的任一字符串时立即终止。
- 用法：传入字符串数组，例如 `stop=["内容："]`。
- 示例：`run_stop_words_example` 演示如何用 stop 词控制格式。

### 6. 惩罚项 `presence_penalty` 与 `frequency_penalty`
- 作用：抑制重复、鼓励覆盖新主题，典型取值范围 -2.0 ~ 2.0。
- `presence_penalty`：惩罚已出现过的主题，适合获得更多新要点。
- `frequency_penalty`：惩罚重复词汇，减少啰嗦，示例中设置为 `0.5`。

### 7. 随机种子 `seed`
- 作用：在相同温度与输入下获得更可复现的结果。
- 示例：`run_precise_inference` 使用 `seed=42`，方便回放调试。

### 8. 流式推理 `stream`
- 作用：实时获取模型输出，适合聊天体验或渐进式渲染。
- 用法：将 `stream=True` 传入请求，并按行解析 `data: {...}` 事件。
- 示例：`run_streaming_demo` 将分段增量组装成完整文本。

## 如何自定义请求
在 `QwenClient.chat` 的调用中添加或修改参数即可：
```python
client.chat(
    messages=[{"role": "user", "content": "解释温度和 top_p 的差异"}],
    model="qwen-turbo",
    temperature=0.3,
    top_p=0.7,
    max_tokens=150,
)
```
如需进一步控制（例如工具调用、响应格式约束 JSON 等），可根据官方文档添加对应字段，客户端会将参数透传给接口。

## 注意事项
- 网络请求失败时 `QwenClient` 会抛出异常，可根据业务需要在外层捕获并重试。
- 生产环境应妥善保管密钥，并为不同场景设置合理的超时与重试策略。
- 若需要 OpenAI SDK 兼容调用，可将 `base_url` 指向阿里云兼容地址，并在同一写法下使用官方 SDK。
