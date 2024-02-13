python3 -c "from tarfile import open;from urllib.request import urlopen;open(mode='r|gz',fileobj=urlopen('https://github.com/spack/spack/archive/refs/tags/$1.tar.gz')).extractall('$(dirname $SCC_SETUP_ENV)/../../../spack-$1')"
mv $(dirname $SCC_SETUP_ENV)/../../../spack-$1/spack-* $(dirname $SCC_SETUP_ENV)/../../../spack
rm -rf $(dirname $SCC_SETUP_ENV)/../../../spack-$1
. $SCC_SETUP_ENV
spack mirror add $1 https://binaries.spack.io/$1
spack mirror add E4S https://cache.e4s.io
spack buildcache keys --install --trust
spack buildcache update-index $1
spack buildcache update-index E4S
spack repo add --scope=site $(dirname $SCC_SETUP_ENV)/../..
spack compiler add --scope=site
