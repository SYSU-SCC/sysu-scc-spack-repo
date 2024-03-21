# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=debian:bookworm-slim
FROM ${BASE_IMAGE} as builder
COPY . /root/opt/sysu-scc-spack-repo-latest
ENV SCC_SETUP_ENV=/root/opt/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    python3 patch tar gzip bzip2 xz-utils \
    file ca-certificates make binutils libstdc++-12-dev
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
$(dirname $SCC_SETUP_ENV)/init-env.sh v0.21.2
. ${SCC_SETUP_ENV}
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0+binutils target=$(arch)" "gcc@12.3.0"
spack install --fail-fast -y python && spack gc -y && spack clean -ab
cp -r $(spack location -i python)/* /root/opt/python
EOF
FROM ${BASE_IMAGE}
ENV SCC_SETUP_ENV=/root/opt/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
ENV SPACK_PYTHON=/root/opt/python/bin/python
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  patch tar gzip bzip2 xz-utils file
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=builder /root/opt /root/opt
