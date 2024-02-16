# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=debian:bookworm-slim
FROM ${BASE_IMAGE}
COPY . /root/sysu-scc-spack-repo-latest
ENV SCC_SETUP_ENV=/root/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    python3 patch tar gzip bzip2 xz-utils \
    file ca-certificates make bash binutils libstdc++-12-dev
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
bash $(dirname $SCC_SETUP_ENV)/init-env.sh v0.21.1
. ${SCC_SETUP_ENV}
bash $(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "gcc@11.2.0 target=x86_64_v3 os=amzn2" "gcc@11.2.0 target=$(arch)" "gcc@11.2.0"
EOF
