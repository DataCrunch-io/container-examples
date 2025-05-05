FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/* .

EXPOSE 8989

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989"]