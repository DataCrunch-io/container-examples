FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/* .

EXPOSE 8989

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989"]