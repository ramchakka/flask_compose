# Use the Nginx image
FROM nginx

RUN mkdir /etc/letsencrypt
COPY letsencrypt/live/giantlittlestep.com/fullchain.pem /etc/letsencrypt
COPY letsencrypt/live/giantlittlestep.com/privkey.pem /etc/letsencrypt

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d
