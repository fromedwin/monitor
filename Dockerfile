FROM python:3.12-alpine

WORKDIR /app
RUN mkdir /app/collectstatic

RUN adduser --disabled-password fromedwin
RUN chown fromedwin:fromedwin /app /app/collectstatic
VOLUME /app/collectstatic

COPY --chown=fromedwin src /app/src
RUN chmod +x /app/src/entrypoint.sh

# Copy parent folder in app as . is refered to Dockerfile path
# Disabled as used by doocker-compose volume
COPY --chown=fromedwin . .

RUN \
    apk add --no-cache postgresql-libs libstdc++ tzdata nodejs npm curl && \
    apk add --no-cache --virtual .build-deps alpine-sdk postgresql-dev && \
    apk --update add build-base jpeg-dev zlib-dev libffi-dev && \
    python -m pip install --upgrade pip --no-cache-dir && \
    python -m pip install -r /app/src/requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

USER fromedwin
EXPOSE 8000