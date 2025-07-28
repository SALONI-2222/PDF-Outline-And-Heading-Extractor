# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]

# docker window cmd command : docker run --rm -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" --network none mysolution:abcd1234