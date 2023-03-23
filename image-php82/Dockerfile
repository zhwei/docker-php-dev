FROM php:8.2.1-fpm

# Install exts
RUN set -eux; \
    apt-get update; \
    apt-get install -y libfreetype6-dev \
                       libjpeg62-turbo-dev \
                       libpng-dev libpq-dev; \
    docker-php-ext-install bcmath gd pcntl posix pdo_pgsql;

RUN set -eux; \
    apt-get install -y libmagickwand-dev --no-install-recommends; \
    pecl install xdebug redis imagick; \
    docker-php-ext-enable xdebug redis imagick

RUN set -eux; \
    apt-get install -y libzip-dev; \
    docker-php-ext-install zip

RUN set -eux; \
    docker-php-ext-install sockets

COPY --from=composer:2.5.2 /usr/bin/composer /usr/bin/composer