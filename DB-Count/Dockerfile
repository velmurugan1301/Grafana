FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests
COPY db_api_exporter.py .
CMD ["python", "db_api_exporter.py"]
