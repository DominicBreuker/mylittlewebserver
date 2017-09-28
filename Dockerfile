FROM python:3.6.2-alpine3.6

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD [ "python", "./http_server.py" ]
