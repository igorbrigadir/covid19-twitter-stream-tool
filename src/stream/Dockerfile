FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y xz-utils && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY stream.py stream.py

ENTRYPOINT ["python", "stream.py"]
