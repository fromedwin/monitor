#Grab the latest alpine image
FROM python:3.9.7-slim-buster

RUN apt-get update \
  && apt-get install -y build-essential curl \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

# RUN apk update \
#     && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev  ffmpeg

ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt --ignore-installed

# Add our code
# ADD ./monitor /opt/monitor/
WORKDIR /opt/monitor

# Expose is NOT supported by Heroku
# EXPOSE 8000 		

# Run the image as a non-root user
# RUN adduser -D sbarbier
# USER sbarbier

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
# CMD gunicorn --bind 0.0.0.0:$PORT wsgi 
CMD python3 manage.py migrate

CMD SECRET_KEY=nothing python3 manage.py tailwind install --no-input;
CMD SECRET_KEY=nothing python3 manage.py tailwind build --no-input;

CMD SECRET_KEY=nothing python3 manage.py collectstatic;