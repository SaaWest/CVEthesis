FROM ubuntu:26.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip python3-venv libxml2-dev libxslt1-dev zlib1g-dev curl wget build-essential
COPY requirements.txt .
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY poclxml.py .

CMD ["python3", "poclxml.py"]
