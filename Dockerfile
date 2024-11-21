# syntax=docker/dockerfile:1.4
ARG SCC_IMAGE=debian:bookworm-slim
FROM ${SCC_IMAGE} as builder
ARG SCC_TARGET=x86_64_v3
ARG SCC_TAG=latest
ARG SCC_OPT=/sccenv/${SCC_TAG}
ARG SCC_SPACK_TAG=v0.23.0
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
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0+mold" "gcc@12.3.0"
spack env create sccenv $(dirname $SCC_SETUP_ENV)/../../spack.yaml
spack env activate -p sccenv
spack install --fail-fast -y && spack gc -y && spack clean -ab
cat >${SCC_SETUP_ENV} <<END
#!/bin/sh
export SPACK_ROOT=\$(dirname $SCC_SETUP_ENV)/../../../spack
export SPACK_PYTHON=$(spack location -i python)/bin/python3
. \$(dirname \$SCC_SETUP_ENV)/../../../spack/share/spack/setup-env.sh
spack env activate -p sccenv
END
EOF
FROM ${SCC_IMAGE} as target
ARG SCC_TAG=latest
ARG SCC_OPT=/sccenv/${SCC_TAG}
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo-${SCC_TAG}/share/sysu-scc-spack-repo/setup-env.sh
COPY --from=builder ${SCC_OPT} ${SCC_OPT}
