# syntax=docker/dockerfile:1.4
FROM debian:bullseye-slim
ARG SCC_OPT=/opt
WORKDIR ${SCC_OPT}
COPY . sysu-scc-spack-repo
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo/share/sysu-scc-spack-repo/setup-env.sh
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    clang-11 python3 \
    patch bash make \
    tar gzip unzip bzip2 xz-utils \
    file git ca-certificates
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
bash $(dirname $SCC_SETUP_ENV)/init-env.sh v0.21.0
bash $(dirname $SCC_SETUP_ENV)/init-default-compiler.sh gcc@7.5.0 gcc@7.5.0
EOF
