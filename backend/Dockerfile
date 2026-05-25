FROM python:3.10-slim

WORKDIR /app

# השורה שחייבת להיות כאן:
RUN pip install --no-cache-dir flask flask-cors

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]