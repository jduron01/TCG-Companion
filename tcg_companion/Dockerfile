FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /

COPY nginx.conf /etc/nginx/nginx.conf
COPY docker_run_server.sh .

RUN mkdir -p /staticfiles

EXPOSE 80

RUN chmod +x docker_run_server.sh

ENTRYPOINT ["./docker_run_server.sh"]

# FROM python:3.12.10
# COPY requirements.txt ./
# RUN pip3 install --user -r requirements.txt
# COPY . ./
# RUN chmod +x docker_run_server.sh
# EXPOSE 80
# ENTRYPOINT ["./docker_run_server.sh"]