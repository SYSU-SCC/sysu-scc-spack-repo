# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=debian:bookworm-slim
ARG SCC_OPT=/root/opt
FROM ${BASE_IMAGE} as builder
COPY . ${SCC_OPT}/sysu-scc-spack-repo-latest
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
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
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0+binutils target=$(arch) python target=$(arch) gmake target=$(arch) ca-certificates-mozilla target=$(arch)" "gcc@12.3.0"
cp -r $(spack location -i --first python) ${SCC_OPT}
mv ${SCC_OPT}/python-* ${SCC_OPT}/python
EOF
FROM ${BASE_IMAGE}
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  patch tar gzip bzip2 xz-utils file
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
EOF
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
ENV SPACK_PYTHON=${SCC_OPT}/python/bin/python
COPY --from=builder ${SCC_OPT} ${SCC_OPT}
