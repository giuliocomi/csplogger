FROM alpine:3.11

RUN apk add --no-cache \
	python \
	sqlite \
	libffi-dev \
	musl-dev \
	py2-pip \
	python-dev \
	gcc \
	openssl-dev \
	git \
	&& apk del libressl-dev \
	&& rm -rf /var/cache/apk/*

RUN adduser -D csplogger-agent

COPY --chown=csplogger-agent:csplogger-agent [ "requirements.txt", "/app/" ]
RUN pip install -r /app/requirements.txt
HEALTHCHECK --interval=50s --timeout=3s --start-period=5s CMD  [ "curl -k --fail https://localhost:8443/ || exit 1"]

COPY --chown=csplogger-agent:csplogger-agent [ ".", "/app/" ]
USER csplogger-agent
ENV FLASK_APP app.py
EXPOSE 8443
ENTRYPOINT ["python", "/app/app.py"]
HEALTHCHECK --interval=50s --timeout=3s --start-period=5s CMD  [ "curl -k --fail https://localhost:8443/ || exit 1"]
