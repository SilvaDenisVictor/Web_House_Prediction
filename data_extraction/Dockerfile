FROM python:latest

WORKDIR /app

COPY . /app/

RUN pip install --trusted-host pypi.python.org -r requeriments.txt

ENTRYPOINT [ "python", "web.py" ]