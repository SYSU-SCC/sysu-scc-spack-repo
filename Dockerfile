# syntax=docker/dockerfile:1.4
ARG SCC_IMAGE=debian:bookworm-slim
FROM ${SCC_IMAGE} as builder
ARG SCC_TARGET=x86_64_v3
ARG SCC_TAG=latest
ARG SCC_OPT=/root/sccenv/${SCC_TAG}
ARG SCC_SPACK_TAG=v0.21.2
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}/share/sysu-scc-spack-repo/setup-env.sh
COPY . ${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  patch tar gzip bzip2 xz-utils file make binutils libc6-dev \
  python3
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
$(dirname $SCC_SETUP_ENV)/init-env.sh ${SCC_SPACK_TAG}
. ${SCC_SETUP_ENV}
spack config --scope=site add "packages:all:target:["${SCC_TARGET}"]"
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0" "gcc@12.3.0"
spack install --fail-fast -y python ca-certificates-mozilla && spack gc -y && spack clean -ab
cp $(spack location -i --first python)/bin/python3 $(dirname $SCC_SETUP_ENV)/../../../
EOF
FROM ${SCC_IMAGE} as target
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  patch tar gzip bzip2 xz-utils file make binutils libc6-dev
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
EOF
ARG SCC_TAG=latest
ARG SCC_OPT=/root/sccenv/${SCC_TAG}
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}/share/sysu-scc-spack-repo/setup-env.sh
ENV SPACK_PYTHON=${SCC_OPT}/python3
COPY --from=builder ${SCC_OPT} ${SCC_OPT}
