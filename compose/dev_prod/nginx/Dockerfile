FROM nginx:1.21.3-alpine

# apline based = ubuntu => apk istead apt
RUN apk update && apk add openssl
RUN mkdir -p /home/web/www

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

COPY ./ssl-params.conf /etc/nginx/ssl-params.conf
