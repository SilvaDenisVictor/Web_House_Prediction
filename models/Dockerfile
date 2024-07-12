FROM python:3.10

WORKDIR /app

COPY requeriments.txt /app/requeriments.txt

RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requeriments.txt

COPY . /app/

ENTRYPOINT [ "python", "main.py" ]