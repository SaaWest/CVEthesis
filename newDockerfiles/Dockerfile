FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y python3 python3-dev python3-pip curl wget build-essential
COPY requirements.txt .

COPY . /poc.py

WORKDIR /app

CMD ["python3", "poc.py"]
