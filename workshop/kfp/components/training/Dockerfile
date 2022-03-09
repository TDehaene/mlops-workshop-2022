FROM python:3.7.9-slim

# Install OpenMP for XGBoost
RUN apt-get update && apt-get -y install libgomp1

# Copy requirements first to leverage docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all necessary file to the container
WORKDIR /src
COPY src ./
COPY helpers ./helpers

ENTRYPOINT ["python", "main.py"]