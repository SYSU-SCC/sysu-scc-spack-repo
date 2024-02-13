spack install --fail-fast --use-buildcache only -y gcc target=$(arch) && spack gc -y && spack clean -ab
spack compiler add --scope=site $(spack location -i gcc)
spack config --scope=site add "packages:all:compiler:[gcc]"
