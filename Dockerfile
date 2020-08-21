FROM ubuntu:20.04

ADD . /opt/poss

RUN set -e -x; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt update; apt -y upgrade; \
    apt -y install build-essential sudo git uwsgi uwsgi-plugin-python3 python3 python3-pip python3-dev; \
    apt clean; \
    cp /opt/poss/docker/entrypoint /usr/local/bin/; \
    cp /opt/poss/docker/config_override.py /opt/poss/; \
    cp /opt/poss/config.dist.py /opt/poss/config.py; \
    echo "from config_override import *" >>/opt/poss/config.py; \
    pip3 install -r /opt/poss/requirements.txt; \
    rm -rf /root/.cache; \
    mkdir /var/poss; \
    useradd --uid=1000 poss

ENTRYPOINT ["/usr/local/bin/entrypoint"]
WORKDIR /opt/poss
CMD ["uwsgi", "--plugins=http,python", "--http=0.0.0.0:8080", "--master", "--processes=1", "--threads=10", "--die-on-term", "--module=app", "--callable=app"]
