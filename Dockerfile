# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=debian:bookworm-slim # ubuntu:22.04
FROM ${BASE_IMAGE}
ARG SCC_OPT=/opt
WORKDIR ${SCC_OPT}
COPY . sysu-scc-spack-repo
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo/share/sysu-scc-spack-repo/setup-env.sh
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
bash $(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "gcc arch=linux-ubuntu22.04-x86_64_v3" "gcc@12.3.0 target=x86_64_v3" "gcc@12.3.0"
EOF
