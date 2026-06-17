From python:3.12-slim
workdir /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "hello:app", "--host", "0.0.0", "--port", "8000"]
