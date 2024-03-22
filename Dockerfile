# syntax=docker/dockerfile:1.4
ARG SCC_IMAGE=debian:bookworm-slim
FROM ${SCC_IMAGE} as builder
ARG SCC_TARGET=x86_64
ARG SCC_OPT=/root/opt
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
COPY . ${SCC_OPT}/sysu-scc-spack-repo-latest
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
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0+binutils target="+${SCC_TARGET} "gcc@12.3.0"
spack install --fail-fast -y "python target="+${SCC_TARGET}+" gmake target="+${SCC_TARGET}+" ca-certificates-mozilla target="+${SCC_TARGET} && spack gc -y && spack clean -ab
cp -r $(spack location -i --first python) $(dirname $SCC_SETUP_ENV)/../../../
mv $(dirname $SCC_SETUP_ENV)/../../../python-* $(dirname $SCC_SETUP_ENV)/../../../python
EOF
FROM ${SCC_IMAGE}
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  patch tar gzip bzip2 xz-utils file
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
EOF
ARG SCC_OPT=/root/opt
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-latest/share/sysu-scc-spack-repo/setup-env.sh
ENV SPACK_PYTHON=${SCC_OPT}/python/bin/python3
COPY --from=builder ${SCC_OPT} ${SCC_OPT}
