# Musetic Web in docker
# Run like this:
#
# $ docker build -t musetic-web:latest .
# $ docker run -it -v /path/to/your/code/musetic-web:/var/www/musetic-web --name musetic-dev musetic-web

FROM debian:jessie
MAINTAINER micah hausler, <hausler.m@gmail.com>

RUN apt-get update && \
    apt-get -y install \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update && \
    apt-get -y install \
    curl \
    g++ \
    gcc \
    git \
    htop \
    jq \
    libblas-dev \
    libcap-dev \
    libffi-dev \
    libfreetype6-dev \
    libjansson-dev \
    libjpeg-dev \
    liblapack-dev \
    liblcms2-dev \
    libpcre3 \
    libpcre3-dev \
    libpng12-dev \
    libpq-dev \
    libpython3.4-dev \
    libtiff5-dev \
    libwebp-dev \
    libzmq-dev \
    man \
    multitail \
    pkg-config \
    postgresql-client-9.3 \
    python3 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y install \
    python-dev \
    python-pip \
    sudo \
    tcl8.5-dev \
    tk8.5-dev \
    unzip \
    vim \
    zip \
    zlib1g-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install \
    uwsgi \
    virtualenv \
    virtualenv-tools

# We explicitly install Django and IPython since the versions don't change a lot
# and they're our largest dependencies. It just makes rebuilding the image faster
RUN /bin/mkdir -p /var/www/ && \
    virtualenv -p /usr/bin/python3 /var/www/env && \
    /var/www/env/bin/pip install \
    Django==1.7.1 \
    IPython==2.3.0 && \
    mkdir -p /var/www/musetic-web/

ENV DOCKER_DEV true
ENV PATH /var/www/env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV VIRTUAL_ENV /var/www/env

ADD ./ /var/www/musetic-web/

RUN /var/www/env/bin/pip install \
    -r /var/www/musetic-web/requirements/test.txt && \
    chown -R www-data:www-data /var/www/

ENV TERM xterm
ENV CLICOLOR 1

USER www-data
WORKDIR /var/www/musetic-web/

VOLUME /var/log/
VOLUME /var/www/musetic-web/

EXPOSE 8000

CMD /var/www/env/bin/python manage.py runserver_plus 0.0.0.0:8000
