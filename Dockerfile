
FROM themattrix/tox-base

MAINTAINER ExOLever <devops@exolever.com>

COPY . .

ARG SKIP_TOX=false
RUN cp tests/local.py.dist tests/local.py
RUN bash -c " \
    if [ -f 'install-prereqs.sh' ]; then \
        bash install-prereqs.sh; \
    fi && \
    if [ $SKIP_TOX == false ]; then \
        TOXBUILD=true tox; \
    fi"
