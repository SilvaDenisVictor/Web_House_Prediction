FROM python:latest

WORKDIR /app

# COPY . /app/

COPY ./requeriments.txt /app/requeriments.txt

# VOLUME /var/log/apps/product-order-api /log

RUN pip install --trusted-host pypi.python.org -r requeriments.txt
COPY ./web.py /app/web.py

ENTRYPOINT [ "python", "web.py" ]