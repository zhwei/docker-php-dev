FROM nginx

# install python3
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends python3; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*;
