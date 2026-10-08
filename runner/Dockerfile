# GitHub Actions self-hosted 러너 + Manim 렌더링 환경
FROM ubuntu:24.04

ARG RUNNER_VERSION=2.338.0
ARG TARGETARCH=amd64

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git jq sudo \
        python3 python3-venv python3-dev build-essential \
        libpango1.0-dev pkg-config fonts-noto-cjk ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m runner
WORKDIR /home/runner/actions-runner
RUN case "$TARGETARCH" in amd64) arch=x64 ;; arm64) arch=arm64 ;; *) echo "지원하지 않는 아키텍처: $TARGETARCH" && exit 1 ;; esac \
    && curl -fsSL "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${arch}-${RUNNER_VERSION}.tar.gz" | tar xz \
    && ./bin/installdependencies.sh \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /home/runner/_work \
    && chown -R runner:runner /home/runner

COPY --chmod=755 entrypoint.sh /entrypoint.sh
USER runner
ENTRYPOINT ["/entrypoint.sh"]
