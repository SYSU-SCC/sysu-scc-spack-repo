python3 -c "import tarfile;from urllib.request import urlopen;tarfile.open(mode='r|gz',fileobj=urlopen('https://github.com/spack/spack/archive/refs/tags/$1.tar.gz')).extractall('$(dirname $SCC_SETUP_ENV)/../../../spack-$1')"
mv -r $(dirname $SCC_SETUP_ENV)/../../../spack-$1/spack-$1 $(dirname $SCC_SETUP_ENV)/../../../spack
rm -rf $(dirname $SCC_SETUP_ENV)/../../../spack-$1
. $SCC_SETUP_ENV
spack mirror add $1 https://binaries.spack.io/$1
spack buildcache keys --install --trust
spack repo add --scope=site $(dirname $SCC_SETUP_ENV)/../..
spack compiler add --scope=site
