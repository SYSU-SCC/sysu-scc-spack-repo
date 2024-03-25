#!/bin/sh
export SPACK_ROOT=$(dirname $SCC_SETUP_ENV)/../../../spack
. $(dirname $SCC_SETUP_ENV)/../../../spack/share/spack/setup-env.sh
spack env activate -p sccenv
