FROM fedora:30

RUN sed -i -E 's|^(metalink\=https\:\/\/mirrors\.fedoraproject\.org\/metalink\?repo\=fedora\-\$releasever&arch\=\$basearch)$|#\1\nbaseurl=https://mirror.fnkr.net/fedora/releases/$releasever/Everything/$basearch/os/\ndeltarpm=0|' /etc/yum.repos.d/fedora.repo && \
    sed -i -E 's|^(metalink\=https\:\/\/mirrors\.fedoraproject\.org\/metalink\?repo\=updates\-released\-f\$releasever&arch\=\$basearch)$|#\1\nbaseurl=https://mirror.fnkr.net/fedora/updates/$releasever/Everything/$basearch/\ndeltarpm=0|' /etc/yum.repos.d/fedora-updates.repo && \
    sed -i 's/^enabled=1$/enabled=0/g' /etc/yum.repos.d/fedora-modular.repo /etc/yum.repos.d/fedora-updates-modular.repo

ADD . /opt/poss

RUN set -e -x; \
    dnf -y upgrade; \
    dnf -y install @development-tools git uwsgi uwsgi-router-http uwsgi-plugin-python3 python3 python3-pip python3-devel; \
    dnf clean all; \
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
