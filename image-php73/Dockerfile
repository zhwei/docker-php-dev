FROM php:7.3.33-fpm

# Install exts
RUN apt-get update && apt-get install -y \
		libfreetype6-dev \
		libjpeg62-turbo-dev \
		libpng-dev libpq-dev 
        libzip-dev; \
    docker-php-ext-install bcmath gd json \
                           mbstring pcntl posix \
                           pdo_pgsql zip sockets

RUN apt-get install -y libmagickwand-dev --no-install-recommends; \
    pecl install xdebug-3.1.6 redis-5.3.4 imagick; \
    docker-php-ext-enable xdebug redis imagick

COPY --from=composer:2.5.2 /usr/bin/composer /usr/bin/composer
