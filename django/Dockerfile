#Grab the latest alpine image
FROM alpine:latest

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip bash
ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

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
CMD python3 manage.py runserver 0.0.0.0:8000 
