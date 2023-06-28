# Dockerfile, Image, Container
FROM python:3.9

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["flask", "run", "-h","0.0.0.0", "-p", "5000"]