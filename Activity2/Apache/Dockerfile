FROM ubuntu

RUN apt-get update

RUN apt-get install -y apache2

EXPOSE 80

COPY ./index.html /var/www/html/index.html

CMD apachectl -D FOREGROUND
