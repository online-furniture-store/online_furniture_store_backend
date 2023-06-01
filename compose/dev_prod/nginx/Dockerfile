FROM nginx:1.21.3-alpine

# apline based = ubuntu => apk istead apt
RUN apk update && apk add openssl
RUN mkdir -p /home/web/www

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 &&\
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/self.key -out /etc/ssl/certs/self.crt \
    -subj "/C=RU/ST=Moscow/L=Kremlin/O=Azzrael Code/OU=Org/CN=azz.code"
RUN ls /etc/ssl/certs/
