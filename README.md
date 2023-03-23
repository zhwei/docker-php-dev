# Local PHP development environment.

## Features

- All in docker
- HTTPS support
- Single config file

## Setup (macOS)

1. Install mkcert:

    ```sh
    brew install mkcert
    ```

2. Config your sites in `site.json`

- `domain` is the domain name of your site, eg: `comiru.test`
    - Remind: need to add to `/etc/hosts` file, eg: `comiru.test 127.0.0.1`
- `root` is the project public directory
    - Remind: need to mount into container in docker-compose.yml, eg: `$HOME/poper`
- `fpm` is the PHP-FPM service name in docker-compose.yml
- `aliases` is the domain aliases of your site, eg: `["www.comiru.test", "sso.comiru.test"]`
- `secure` is the HTTPS support, default is `true`

1. Generate SSL certificates

    ```sh
    python3 generator.py --certs
    ```

2. Start docker containers

    ```sh
    docker compose up -d
    ```

3. Visit your site in browser

    - Site list: <http://127.0.0.1>
    - <http://php73.test>
    - <https://php82.test>
