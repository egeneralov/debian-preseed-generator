FROM debian:9

RUN apt-get update -q && \
apt-get install -yq python3-pip --no-install-recommends && \
apt-get autoclean -yq && \
apt-get clean -yq

RUN apt-get update -q && \
apt-get install -yq xorriso cpio genisoimage wget aria2 --no-install-recommends && \
apt-get autoclean -yq && \
apt-get clean -yq

WORKDIR /app

ADD requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt

ADD . .

ENV PORT=8080

CMD python3 app.py
