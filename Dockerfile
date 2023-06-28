# Dockerfile, Image, Container
FROM python:3.9

RUN mkdir -p /home/fastapibasics

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]