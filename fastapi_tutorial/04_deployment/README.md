# 第四章：部署 (Deployment)

本章介绍如何将 FastAPI 应用容器化 (Docker)。

## 1. Dockerfile 解析

文件：`Dockerfile`

这是构建 Docker 镜像的蓝图。

```dockerfile
FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## 2. 使用 uv 构建 (可选)

文件：`Dockerfile.uv`

如果你希望加快构建速度，可以使用 `uv` 来安装依赖。

```dockerfile
FROM python:3.10-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt
COPY ./app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

要使用此 Dockerfile 构建：

```bash
docker build -f Dockerfile.uv -t myfastapiimage-uv .
```

## 3. 包含的示例

本目录已经包含了一个完整的示例结构：
- `app/`：包含源代码 (`main.py`)
- `requirements.txt`：依赖列表
- `Dockerfile` / `Dockerfile.uv`：构建指令

## 4. 构建与运行

### 构建镜像
在 `04_deployment` 目录下打开终端，运行：

```bash
docker build -t myfastapiimage .
```

### 运行容器
```bash
docker run -d --name mycontainer -p 80:80 myfastapiimage
```

现在你的应用运行在 `http://localhost` (端口 80)。你会看到 `{"Hello": "From Docker!"}`。
