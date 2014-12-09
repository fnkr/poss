**1)** Install POSS. https://github.com/fnkr/POSS#install

**2)** Install `uwsgi`.
```
./env/bin/pip install uwsgi
```

**3)** Place this script in your POSS root directory (where the manage.py is). You can name it `init` or so.
```
#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

exec ./env/bin/uwsgi \
                    -s 127.0.0.1:9090 \
                    --module app --callable app \
                    --master \
                    --processes 1 \
                    --enable-threads --threads 10 \
                    --die-on-term
```
`-s` can be a tcp socket (e.g. `127.0.0.1:8080`) or a unix socket (e.g. `/tmp/poss.sock`).

**4)** Make the script executable.
```
chmod +x init
```

**5)** Configure nginx.
```
server {
    listen 80;
    server_name example.com;

    client_max_body_size 10M; # maximum file size that can be uploaded

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:9090; # tcp socket
        uwsgi_pass unix:/tmp/poss.sock; # or unix socket
    }
}
```

**6)** Run `init`, reload or restart nginx. You probably want to start init script (step 3) on system startup.
