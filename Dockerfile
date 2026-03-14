FROM python:3.11-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

CMD ["python", "main.py"]