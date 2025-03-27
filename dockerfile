# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到镜像中
COPY . /app

# 安装 Python 依赖
RUN pip install -r requirements.txt


# 复制 config.ini 文件到镜像中
COPY config.ini /app/config.ini

# 命令来运行你的程序
CMD ["python", "chatbot.py"]
