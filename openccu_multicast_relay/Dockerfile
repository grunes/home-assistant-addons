ARG BUILD_FROM=ghcr.io/home-assistant/base:3.23-2026.03.1
FROM ${BUILD_FROM}

SHELL ["/bin/ash", "-o", "pipefail", "-c"]

RUN apk add --no-cache \
        iproute2 \
        iptables \
        python3 \
        tcpdump

COPY rootfs /

RUN chmod +x /etc/services.d/relay/run \
    && chmod +x /usr/local/bin/hmip-relay.py

