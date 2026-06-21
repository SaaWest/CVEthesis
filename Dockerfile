FROM debian:11
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python python-dev python-pip build-essential

COPY poc.py .
RUN python -m pip install lxml<=3.3.4

CMD ["python", "poc.py"]