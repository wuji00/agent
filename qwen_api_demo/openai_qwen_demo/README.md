# 通义千问：OpenAI SDK 调用教程（含多模态与思考模型）

本示例展示如何使用 **OpenAI Python SDK** 调用通义千问的 OpenAI 兼容接口，覆盖：
- 纯文本对话（非流式与流式）；
- 图文多模态模型；
- 思考/推理型模型；
- 关键推理参数（温度、Top-P、停止词、种子等）。

## 环境准备（推荐使用 uv）
> 如未安装 [uv](https://github.com/astral-sh/uv)，可先运行 `pip install --upgrade uv`。若已有虚拟环境，可直接在环境内使用 `uv pip install openai`。

1. 创建虚拟环境并激活：
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
   ```
2. 安装依赖：
   ```bash
   uv pip install openai
   ```
3. 配置环境变量（至少需要 API Key）：
   ```bash
   export QWEN_OPENAI_API_KEY="你的DashScope或千问API Key"
   export QWEN_OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 可选，默认已设置
   ```

## 快速运行
```bash
python openai_qwen_examples.py
```
脚本会依次打印四段示例：非流式、流式、多模态、思考模型。

## 文件说明
- `openai_qwen_examples.py`：核心示例代码，包含四个方法：
  - `basic_chat`：非流式文本对话，展示温度、Top-P、停止词、种子等推理参数的组合。
  - `streaming_chat`：流式输出，演示如何增量拼接模型回复。
  - `multimodal_chat`：图文输入，默认携带一个内置 1x1 PNG 基础图片（可替换为自定义路径）。
  - `reasoning_chat`：面向思考/推理型模型的调用，使用低温度与系统提示引导逐步推理。

## 关键参数与实践要点
1. **模型选择 `model`**
   - 文本：`qwen-plus`、`qwen-max` 等。
   - 多模态：`qwen-vl-plus` 等。
   - 思考/推理：若控制台开通了对应型号（如 `qwen-max` 或最新的思考版本），在 `reasoning_chat` 中替换即可。

2. **温度 `temperature` 与 Top-P `top_p`**
   - 低温度（0.2~0.5）强调确定性和复现性，适合推理；高温度（0.7~0.95）提升创意。
   - Top-P 控制概率质量累积，通常与温度联动，避免同时取极端值。

3. **`max_tokens` 与长度控制**
   - 避免输出过长导致费用或时延增加；示例限定在 200~300 之间。

4. **停止词 `stop`**
   - 当回复命中任意字符串时立即终止，可用于生成结构化片段。

5. **随机种子 `seed`**
   - 在相同输入与温度下提升复现性，便于调试 A/B 对比。

6. **流式输出 `stream=True`**
   - 使用生成器持续消费增量片段，适合前端渐进式渲染或命令行体验。

7. **多模态输入**
   - 使用 `messages[0]["content"]` 列表携带文本与 `image_url`，支持远程 URL 或 base64 Data URL。

8. **思考/推理模型提示**
   - 在 `system` 中要求“逐步推理/自检”，并结合低温度、充足 `max_tokens` 以保留中间推导。

## 替换自定义图片
将图片路径传给 `multimodal_chat(image_path="/path/to/img.png")`，脚本会读取并自动转成 base64 发送到接口。

## 故障排查
- 确认 `QWEN_OPENAI_API_KEY` 设置正确；
- 若网络需代理，可调整 `QWEN_OPENAI_BASE_URL` 指向对应网关；
- SDK 报错时可打印 `completion` 或捕获异常以查看详细信息。
