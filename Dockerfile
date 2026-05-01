FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    aria2 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy coding files to workdir
COPY . /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=1

# Install python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python3", "-m", "Bot"]
