FROM python:3.10-slim

WORKDIR /app

# השורה שחייבת להיות כאן:
RUN pip install --no-cache-dir flask flask-cors --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]