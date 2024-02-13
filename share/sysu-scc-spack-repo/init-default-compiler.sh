spack buildcache list
echo ">>> _ <<<"
spack install --fail-fast --use-buildcache only -y gcc@12.3.0%gcc@11.4.0 arch=linux-ubuntu22.04-x86_64_v3 && spack gc -y && spack clean -ab
echo ">>> _ <<<"
spack compiler add --scope=site $(spack location -i gcc)
spack config --scope=site add "packages:all:compiler:[gcc]"
