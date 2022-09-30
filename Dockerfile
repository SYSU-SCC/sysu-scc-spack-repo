# syntax=docker/dockerfile:1.4
FROM debian:11-slim
ARG SCC_OPT=/opt
WORKDIR ${SCC_OPT}
COPY . sysu-scc-spack-repo
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo/share/sysu-scc-spack-repo/setup-env.sh
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    clang-11 python3 \
    make patch patchelf bash \
    tar gzip unzip bzip2 xz-utils \
    file gnupg2 git ca-certificates
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
sh $(dirname $SCC_SETUP_ENV)/init-env.sh
EOF
