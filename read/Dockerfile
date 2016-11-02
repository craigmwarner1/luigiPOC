FROM python:2
ENV DB_IP 'localhost'
COPY . /code
RUN pip install redis
RUN mkdir /share
VOLUME ['/share']
CMD python /code/read.py
