# in your Dockerfile
FROM sphinxdoc/sphinx

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

WORKDIR /docs

EXPOSE 5500