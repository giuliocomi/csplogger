FROM alpine

RUN apk add --update \
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
WORKDIR /home/csplogger-agent

RUN git clone https://github.com/giuliocomi/csplogger 
RUN chown -R csplogger-agent:csplogger-agent ./
WORKDIR csplogger

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER csplogger-agent
ENV FLASK_APP app.py
EXPOSE 8443
ENTRYPOINT ["python", "app.py"]
