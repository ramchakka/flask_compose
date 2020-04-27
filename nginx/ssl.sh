#!/bin/bash

#example from
#https://levelup.gitconnected.com/deploying-ssl-enabled-react-angular-vue-applications-to-aws-using-lets-encrypt-a7aff5a417ee

#LETSENCRYPT_EMAIL="YOUR_EMAIL"
#DNSNAME="YOUR_DOMAIN_NAME"

LETSENCRYPT_EMAIL="ramulu@gmail.com"
DNSNAME="giantlittlestep.com"

#docker run -it --rm --name certbot \
sudo docker run -it --rm --name certbot \
    -v "$PWD/letsencrypt:/etc/letsencrypt" \
    -v "$PWD/lib/letsencrypt:/var/lib/letsencrypt" \
    certbot/certbot \
    certonly \
    -m $LETSENCRYPT_EMAIL \
    --manual \
    --preferred-challenges dns-01 \
    --no-eff-email \
    --manual-public-ip-logging-ok \
    --keep-until-expiring \
    --agree-tos \
    -d $DNSNAME \
    --server https://acme-v02.api.letsencrypt.org/directory
