FROM python:3-alpine

RUN set -e -x; \
        apk add --no-cache --virtual .build-deps \
                git \
                build-base \
                linux-headers \
            ; \
            git clone https://github.com/fnkr/POSS.git /opt/poss; \
            cp /opt/poss/config.dist.py /opt/poss/config.py; \
            echo "from config_override import *" >>/opt/poss/config.py; \
            pip install -r /opt/poss/requirements.txt; \
            pip install uwsgi; \
            apk add --no-cache sudo; \
        apk del .build-deps; \
        rm -rf /root/.cache; \
        mkdir /var/poss; \
        adduser -D -u 1000 poss

ADD docker/config_override.py /opt/poss/

ADD docker/entrypoint /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint"]

WORKDIR /opt/poss
CMD ["uwsgi", "--http=0.0.0.0:8080", "--master", "--processes=1", "--threads=10", "--die-on-term", "--module=app", "--callable=app"]
