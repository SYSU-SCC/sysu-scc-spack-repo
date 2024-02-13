spack install --fail-fast --use-buildcache only -y gcc target=x86_64_v3 && spack gc -y && spack clean -ab
spack compiler add --scope=site $(spack location -i gcc)
spack config --scope=site add "packages:all:compiler:[gcc]"
