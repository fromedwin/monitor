FROM python:3.12-alpine

RUN adduser --disabled-password fromedwin

WORKDIR /app

# Generate collectstatic folder to store static files
RUN mkdir /app/collectstatic
RUN chown fromedwin:fromedwin /app /app/collectstatic
VOLUME /app/collectstatic

# Copy requirements first for better layer caching
COPY --chown=fromedwin src/requirements.txt /app/src/requirements.txt

# Install system dependencies and Python packages
RUN \
    apk add --no-cache postgresql-libs libstdc++ tzdata nodejs npm curl && \
    apk add --no-cache --virtual .build-deps alpine-sdk postgresql-dev && \
    apk --update add build-base jpeg-dev zlib-dev libffi-dev && \
    python -m pip install --upgrade pip --no-cache-dir && \
    python -m pip install -r /app/src/requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# Add in docker image full code base
COPY --chown=fromedwin . .

USER fromedwin
EXPOSE 8000