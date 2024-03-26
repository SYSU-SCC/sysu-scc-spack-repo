# sysu-scc-spack-repo

[Spack](https://spack.readthedocs.io/en/stable/repositories.html) package [repository](./packages) maintained by Student Cluster Competition Team @ Sun Yat-sen University.

由中山大学超算队维护的 [spack](https://spack.readthedocs.io/en/stable/repositories.html) package [repository](./packages)；同时，我们也向上游提交了包括 [antlr4-complete](https://github.com/spack/spack/pull/42048)、[antlr4-cpp-runtime](https://github.com/spack/spack/pull/42048)、[cutlass](https://github.com/spack/spack/pull/31379)、[py-altair](https://github.com/spack/spack/pull/31386)、[py-vl-convert-python](https://github.com/spack/spack/pull/42073)、[py-cairosvg](https://github.com/spack/spack/pull/42067)、[py-cssselect2](https://github.com/spack/spack/pull/42067) 在内的 package，并已合并入主线。

同时提供了一个面向超算竞赛的[环境部署脚本](./sysu-scc-spack-repo/share/sysu-scc-spack-repo/init-env.sh)，旨在比赛期间快速构建一个可以使用的 spack 环境，其中包括：

1. 从 spack 官方镜像下载一个预编译的编译器，重新源码自编译一遍作为默认编译器。
2. 基于 [spack environments](https://spack.readthedocs.io/en/stable/environments.html) 快速安装必要的软件环境，例如 `mpi` 等。
   - 需要注意的是，此处的 [spack.yaml](./spack.yaml) 仅作为示例，并非中大超算队在比赛中使用的版本。可以参照 [spack 文档](https://spack.readthedocs.io/en/stable/environments.html#spack-yaml) 和 [spack-configs](https://github.com/spack/spack-configs)，打包符合实际需要的软件环境。
3. 基于 [GitHub Actions](https://github.com/SYSU-SCC/sysu-scc-spack-repo/actions) 的构建测试，保障脚本的代码质量。

同样欢迎其他学校使用，欢迎[![Stars](https://img.shields.io/github/stars/SYSU-SCC/sysu-scc-spack-repo.svg)](https://github.com/SYSU-SCC/sysu-scc-spack-repo)[![Issues](https://img.shields.io/github/issues/SYSU-SCC/sysu-scc-spack-repo.svg)](https://github.com/SYSU-SCC/sysu-scc-spack-repo/issues)[![Issues-pr](https://img.shields.io/github/issues-pr/SYSU-SCC/sysu-scc-spack-repo)](https://github.com/SYSU-SCC/sysu-scc-spack-repo/pulls)！友好的超算比赛环境，由你我共建～

## How to use

### 使用预编译的环境

```shell
docker run \
   --name sccenv \
   wukan0621/sccenv
# 请提前将 sccenv 挂载到目标位置
docker cp sccenv:/sccenv /
docker rm sccenv
```

### 从零开始

最小化配置一个可以使用的 spack，需要的软件依赖可以参考 [Dockerfile](./Dockerfile)。

```shell
python3 -c "from tarfile import open;from urllib.request import urlopen;open(mode='r|gz',fileobj=urlopen('https://github.com/SYSU-SCC/sysu-scc-spack-repo/archive/refs/tags/v0.21.2.12.3.0.12.20240326.tar.gz')).extractall()"

# 只依赖这一个环境变量，可以放进 ~/.bashrc
export SCC_SETUP_ENV=$(realpath sysu-scc-spack-repo-0.21.2.12.3.0.12.20240326/share/sysu-scc-spack-repo/setup-env.sh)

# 初始化
$(dirname $SCC_SETUP_ENV)/init-env.sh v0.21.2

# 后续每次只需要执行这一句即可使用配好的环境
. $SCC_SETUP_ENV

# 从 spack 官方镜像下载一个预编译的编译器，重新源码自编译一遍作为默认编译器
# see <https://cache.spack.io/package/v0.21.2/gcc/specs/>
$(dirname $SCC_SETUP_ENV)/init-default-compiler.sh "builtin.gcc@12.3.0 target=x86_64_v3 os=ubuntu22.04" "gcc@12.3.0%gcc@12.3.0+binutils" "gcc@12.3.0"
```

### 集成进已有的 spack 环境

```shell
python3 -c "from tarfile import open;from urllib.request import urlopen;open(mode='r|gz',fileobj=urlopen('https://github.com/SYSU-SCC/sysu-scc-spack-repo/archive/refs/heads/latest.tar.gz')).extractall()"
spack repo add --scope=site sysu-scc-spack-repo-latest

# A Simple Test
spack env create sccenv sysu-scc-spack-repo-latest/spack.yaml
spack env activate -p sccenv
spack install
spack env deactivate
```

### 测试是否能用

```shell
spack install sccenv.hpl-ai ^blaspp+openmp ^openblas threads=openmp ^mpich
spack load hpl-ai
cp $(spack location -i hpl-ai)/bin/HPL.dat HPL.dat
OMP_NUM_THREADS=2 $(which mpirun) -n 4 xhpl_ai
```

## License

This project is part of Spack. Spack is distributed under the terms of both the
MIT license and the Apache License (Version 2.0). Users may choose either
license, at their option.

All new contributions must be made under both the MIT and Apache-2.0 licenses.

See LICENSE-MIT, LICENSE-APACHE, COPYRIGHT, and NOTICE for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811652
