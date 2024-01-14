python3 -c "import tarfile;from urllib.request import urlopen;tarfile.open(fileobj=urlopen(https://github.com/spack/spack/archive/refs/tags/$1.tar.gz)).extractall('$(dirname $SCC_SETUP_ENV)/../../../spack')"
. $SCC_SETUP_ENV
spack mirror add $1 https://binaries.spack.io/$1
spack buildcache keys --install --trust
spack repo add --scope=site $(dirname $SCC_SETUP_ENV)/../..
spack compiler add --scope=site
