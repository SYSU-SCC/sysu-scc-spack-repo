# sysu-scc-spack-repo

[Spack](https://spack.readthedocs.io/en/stable/repositories.html) package [repository](./packages) maintained by Student Cluster Competition Team @ Sun Yat-sen University.

由中山大学超算队维护的 [spack](https://spack.readthedocs.io/en/stable/repositories.html) package [repository](./packages)；同时，我们也向上游提交了包括 cutlass（[spack#31379](https://github.com/spack/spack/pull/31379)）、py-altair（[spack#31386](https://github.com/spack/spack/pull/31386)）在内的 package，并已合并入主线。

同时提供了一个面向超算竞赛的[环境部署脚本](./sysu-scc-spack-repo/share/sysu-scc-spack-repo/init-env.sh)，旨在比赛期间快速构建一个可以使用的 spack 环境，其中包括：

1. 从源码重新编译的旧版本 `gcc`（此处选择了 `gcc@7.5.0`，也可以在[这个文件](./share/sysu-scc-spack-repo/setup-env.sh)中修改对应的环境变量）。
2. 基于 [spack environments](https://spack.readthedocs.io/en/stable/environments.html) 快速安装必要的软件环境，例如 `mpi` 等。
   - 需要注意的是，此处的 [spack.yaml](./spack.yaml) 仅作为示例，并非中大超算队在比赛中使用的版本。可以参照 [spack 文档](https://spack.readthedocs.io/en/stable/environments.html#spack-yaml) 和 [spack-configs](https://github.com/spack/spack-configs)，打包符合实际需要的软件环境。
3. 基于 [GitHub Actions](https://github.com/SYSU-SCC/sysu-scc-spack-repo/actions) 的构建测试，保障脚本的代码质量。

同样欢迎其他学校使用，欢迎[![Stars](https://img.shields.io/github/stars/SYSU-SCC/sysu-scc-spack-repo.svg)](https://github.com/SYSU-SCC/sysu-scc-spack-repo)[![Issues](https://img.shields.io/github/issues/SYSU-SCC/sysu-scc-spack-repo.svg)](https://github.com/SYSU-SCC/sysu-scc-spack-repo/issues)[![Issues-pr](https://img.shields.io/github/issues-pr/SYSU-SCC/sysu-scc-spack-repo)](https://github.com/SYSU-SCC/sysu-scc-spack-repo/pulls)！友好的超算比赛环境，由你我共建～

## How to use

### 从零开始

最小化配置一个可以使用的 spack，需要的软件依赖可以参考 [Dockerfile](./Dockerfile)。

```bash
git clone https://github.com/SYSU-SCC/sysu-scc-spack-repo

# 只依赖这一个环境变量，可以放进 ~/.bashrc
export SCC_SETUP_ENV=$(realpath sysu-scc-spack-repo/share/sysu-scc-spack-repo/setup-env.sh)

# 初始化
bash $(dirname $SCC_SETUP_ENV)/init-env.sh

# 后续每次只需要执行这一句即可使用配好的环境
. $SCC_SETUP_ENV
```

### 集成进已有的 spack 环境

```bash
git clone https://github.com/SYSU-SCC/sysu-scc-spack-repo
spack repo add --scope=site sysu-scc-spack-repo

# A Simple Test
spack env create sysu-scc sysu-scc-spack-repo/spack.yaml
spack env activate -p sysu-scc
spack install
spack env deactivate
```

### 测试是否能用

```bash
spack install sysu-scc.hpl-ai ^blaspp+openmp ^openblas threads=openmp ^mpich
spack load hpl-ai
cp $(spack location -i hpl-ai)/bin/HPL.dat HPL.dat
OMP_NUM_THREADS=2 $(which mpirun) -n 4 xhpl_ai
```

### 在 docker 中测试

```bash
docker pull wukan0621/sccenv
docker run \
  --name sccenv \
  -it wukan0621/sccenv \
  bash

# 然后在 docker 中检查
. $SCC_SETUP_ENV
spack find
```

## License

This project is part of Spack. Spack is distributed under the terms of both the
MIT license and the Apache License (Version 2.0). Users may choose either
license, at their option.

All new contributions must be made under both the MIT and Apache-2.0 licenses.

See LICENSE-MIT, LICENSE-APACHE, COPYRIGHT, and NOTICE for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811652
