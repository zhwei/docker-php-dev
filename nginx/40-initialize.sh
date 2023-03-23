set -eux

# make /etc/nginx/conf.d/default.conf listen 443 and 80

echo "
server {
    listen              443         ssl http2 default_server;
    listen              [::]:443    ssl http2 default_server;
    root                /usr/share/nginx/html;

    ssl_certificate     /php-shared/certs/multiple-domain.crt;
    ssl_certificate_key /php-shared/certs/multiple-domain.key;
}
" > /etc/nginx/conf.d/default_443.conf

python3 /php-shared/generator.py --nginx
