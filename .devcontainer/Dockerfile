FROM ghcr.io/ludeeus/devcontainer/integration:latest

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update \
    && sudo apt install -y libpcap-dev vim curl jq \
    && mkdir -p /opt

WORKDIR /opt

RUN git clone --depth=1 -b dev https://github.com/home-assistant/core.git hass \
    && python3 -m pip --disable-pip-version-check install --upgrade ./hass \
    && ln -s /workspaces/hacs-mywatertoronto/custom_components/mywatertoronto /opt/hass/homeassistant/components/mywatertoronto

ENV SHELL /bin/bash
