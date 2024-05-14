#!/bin/sh
spack buildcache install --otherarch "$1"
spack compiler add --scope=site $(spack location -i "$1")
spack install --fresh --fail-fast -y "$2" && spack gc -y && spack clean -ab
rm $(dirname $SCC_SETUP_ENV)/../../../spack/etc/spack/compilers.yaml
spack compiler add --scope=site $(spack location -i "$2")
spack config --scope=site add "packages:all:compiler:[$3]"
