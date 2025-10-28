FROM       php:7-apache
LABEL      maintainer="Sawood Alam <@ibnesayeed>"

COPY       . /var/www/html/

# Prevent "Could not reliably determine the server's fully qualified domain name" at container start
# Create a small conf with a ServerName and enable it
RUN printf "ServerName localhost\n" > /etc/apache2/conf-available/servername.conf \
 && a2enconf servername
