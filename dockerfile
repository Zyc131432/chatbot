FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

COPY config.ini /app/config.ini

CMD ["python", "chatbot.py"]
