spack buildcache install --otherarch "$1" && spack gc -y && spack clean -ab
spack compiler add --scope=site $(spack location -i $1)
spack config --scope=site add "packages:all:compiler:[$2]"
