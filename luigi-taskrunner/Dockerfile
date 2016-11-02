FROM python:latest

RUN mkdir /etc/luigi
ADD ./etc/luigi/logging.cfg /etc/luigi/
ADD ./etc/luigi/client.cfg /etc/luigi/
VOLUME /etc/luigi

RUN mkdir -p /luigi/tasks
RUN mkdir -p /luigi/work
RUN mkdir -p /luigi/outputs

ADD ./luigi/tasks/hello_world.py /luigi/tasks

VOLUME /luigi/work
VOLUME /luigi/tasks
VOLUME /luigi/outputs

RUN apt-get update && apt-get install -y \
    libpq-dev \
    freetds-dev \
    build-essential

RUN bash -c "pyvenv /luigi/.pyenv \
    && source /luigi/.pyenv/bin/activate \
    && pip install cython \
    && pip install sqlalchemy luigi pymssql psycopg2 alembic pandas \
    && pip install docker-py"

ADD ./luigi/taskrunner.sh /luigi/

ENTRYPOINT ["bash", "/luigi/taskrunner.sh"]
