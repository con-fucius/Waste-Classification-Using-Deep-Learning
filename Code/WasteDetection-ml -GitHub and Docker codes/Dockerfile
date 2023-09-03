FROM ubuntu:latest

RUN apt-get update && apt-get install -y git python3-dev gcc \
    python3-pip\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN ls app/

# RUN python app/server.py

EXPOSE 80

CMD ["python3", "app/server.py", "serve"]