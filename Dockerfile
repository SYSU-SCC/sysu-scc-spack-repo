# syntax=docker/dockerfile:1.4
ARG SCC_IMAGE=debian:bookworm-slim
FROM ${SCC_IMAGE} as builder
ARG SCC_TARGET=x86_64_v3
ARG SCC_TAG=latest
ARG SCC_OPT=/sccenv/${SCC_TAG}
ARG SCC_SPACK_TAG=v1.0.0
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}/share/sysu-scc-spack-repo/setup-env.sh
COPY . ${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
  make binutils libc6-dev \
  python3 ca-certificates file patch
apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
$(dirname $SCC_SETUP_ENV)/init-env.sh ${SCC_SPACK_TAG}
cp -r $(dirname $SCC_SETUP_ENV)/../../lib $(dirname $SCC_SETUP_ENV)/../../../spack
. $(dirname $SCC_SETUP_ENV)/../../../spack/share/spack/setup-env.sh
# Ensure generic targets for maximum matching with buildcaches
spack config --scope site add "packages:all:require:["${SCC_TARGET}"]"
EOF
FROM ${SCC_IMAGE} as target
ARG SCC_TAG=latest
ARG SCC_OPT=/sccenv/${SCC_TAG}
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}/share/sysu-scc-spack-repo/setup-env.sh
COPY --from=builder ${SCC_OPT} ${SCC_OPT}
