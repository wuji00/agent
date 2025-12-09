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

## 2. 包含的示例

本目录已经包含了一个完整的示例结构：
- `app/`：包含源代码 (`main.py`)
- `requirements.txt`：依赖列表
- `Dockerfile`：构建指令

## 3. 构建与运行

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
