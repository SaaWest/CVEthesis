FROM debian:10
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential python python-dev python-pip


COPY poc.py .

CMD ["python", "poc.py"]