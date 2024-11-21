#!/bin/sh
python3 -c "from tarfile import open;from urllib.request import urlopen;open(mode='r|gz',fileobj=urlopen('https://github.com/spack/spack/archive/refs/tags/$1.tar.gz')).extractall('$(dirname $SCC_SETUP_ENV)/../../../spack-$1')"
mv $(dirname $SCC_SETUP_ENV)/../../../spack-$1/spack-* $(dirname $SCC_SETUP_ENV)/../../../spack
rm -rf $(dirname $SCC_SETUP_ENV)/../../../spack-$1
. $(dirname $SCC_SETUP_ENV)/../../../spack/share/spack/setup-env.sh
spack mirror add --scope=site  $1 https://binaries.spack.io/$1
spack buildcache keys --install --trust
spack repo add --scope=site $(dirname $SCC_SETUP_ENV)/../..
