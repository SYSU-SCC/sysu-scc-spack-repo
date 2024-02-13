spack buildcache install --otherarch -y gcc@12.3.0 target=x86_64_v3 && spack gc -y && spack clean -ab
spack compiler add --scope=site $(spack location -i gcc@12.3.0)
spack config --scope=site add "packages:all:compiler:[gcc@12.3.0]"
