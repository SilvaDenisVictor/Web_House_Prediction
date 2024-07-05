FROM python:latest

WORKDIR /app

# COPY . /app/

COPY ./requeriments.txt /app/requeriments.txt
COPY ./web.py /app/web.py

# VOLUME /var/log/apps/product-order-api /log

RUN pip install --trusted-host pypi.python.org -r requeriments.txt

ENTRYPOINT [ "python", "web.py" ]