# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到镜像中
COPY . .

# 安装 Python 依赖
RUN pip install -r requirements.txt

# 复制 config.ini 文件到镜像中
COPY config.ini /app/config.ini

# 设置环境变量
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV FIREBASE_KEY_PATH=/app/chatbot_db.json
ENV GPT_TOKEN=${GPT_TOKEN}
ENV BASIC_URL=${BASIC_URL}
ENV MODEL_NAME=${MODEL_NAME}
ENV API_VERSION=${API_VERSION}

# 复制 Firebase 密钥文件到镜像中
COPY /Users/ci1/Desktop/chatbot_db.json /app/chatbot_db.json

# 命令来运行你的程序
CMD ["python", "chatbot.py"]
