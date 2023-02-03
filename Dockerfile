FROM alpine:latest

WORKDIR /usr/src/app

RUN apk add \
	&& apk update \
	&& apk upgrade \
	&& apk add python3 \
	&& apk add py3-pip
#	&& apk add git \
#	&& git clone https://github.com/vjanis/api_web.git --depth 1 --branch=main

COPY . ./api_faili

RUN pip install -r api_faili/requirements.txt

WORKDIR /usr/src/app/api_faili

CMD uvicorn main:app --host 0.0.0.0 --port 8000