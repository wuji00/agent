# 使用官方 Python 基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /code

# 复制依赖文件
COPY ./requirements.txt /code/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制应用代码
COPY ./app /code/app

# 启动命令
# 这里假设你的代码在 app/main.py 中，且应用实例名为 app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
