FROM python:3.14-slim

WORKDIR /app

EXPOSE 8000

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "./main.py" ]
