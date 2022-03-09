FROM python:3.7.9-slim

# Copy requirements first to leverage docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt