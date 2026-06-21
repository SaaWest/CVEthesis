FROM python:3.8

WORKDIR /

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY code_svg.py .

COPY test.svg .

CMD ["python3", "code_svg.py"]
