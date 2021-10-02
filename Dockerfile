FROM python:3.9-slim

COPY requirements.txt /app/
COPY server.py /app/

WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["python", "server.py"]
