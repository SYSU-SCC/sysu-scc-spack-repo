# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack import *


class GpgpuSim(MakefilePackage):
    homepage = "https://github.com/gpgpu-sim/gpgpu-sim_distribution"

    version("dev", git="https://github.com/gpgpu-sim/gpgpu-sim_distribution", branch="dev")
    version("accel-sim", git="https://github.com/accel-sim/gpgpu-sim_distribution")
    version(
        "4.0.1",
        url="https://github.com/gpgpu-sim/gpgpu-sim_distribution/archive/refs/tags/v4.0.1.tar.gz",
        sha256="9c7d6e42af507dc7d7572cfe0d5179fa41b90bf3299522e438034a1aaad06f81",
    )

    depends_on("makedepend", type=("build"))
    depends_on("sed", type=("build"))
    depends_on("bison", type=("build"))
    depends_on("flex", type=("build"))
    depends_on("zlib", type=("link"))
    depends_on("cuda", type=("build", "link", "run"))
    depends_on("gl", type=("link"))
    conflicts("%" + "gcc@8:")

    def edit(self, spec, prefix):
        # fix <https://github.com/gpgpu-sim/gpgpu-sim_distribution/issues/221>
        cuda_sim_Makefile = FileFilter("src/cuda-sim/Makefile")
        cuda_sim_Makefile.filter(
            "> \$\(OUTPUT_DIR\)/ptx_parser_decode\.def",
            " | sed 's/\"end of file\"/end of file/' "
            + " | sed 's/\"invalid token\"/invalid token/' "
            + "> $(OUTPUT_DIR)/ptx_parser_decode.def",
        )
        for mf in (
            ["setup_environment"]
            + glob.glob("**/*akefile", recursive=True)
            + glob.glob("**/*.mk", recursive=True)
        ):
            print(mf, flush=True)
            m = FileFilter(mf)
            m.filter("gcc-\$\(CC_VERSION\)/cuda-\$\(CUDART_VERSION\)/", "")
            m.filter("gcc-\$CC_VERSION/cuda-\$CUDA_VERSION_NUMBER/", "")
            m.filter("gcc", "cc")
            m.filter("g\+\+", "c++")
            m.filter("CC_VERSION.*", "")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "gpgpu-sim_distribution"))
        install_tree(self.stage.source_path, join_path(prefix, "gpgpu-sim_distribution"))

    def setup_build_environment(self, env):
        env.set("CUDA_INSTALL_PATH", self.spec["cuda"].prefix)
        env.set("GPGPUSIM_ROOT", self.stage.source_path)
        if self.version == Version("4.0.1"):
            env.set("GPGPUSIM_POWER_MODEL", self.stage.source_path + "/src/gpuwattch/")
        else:
            env.set("GPGPUSIM_POWER_MODEL", self.stage.source_path + "/src/accelwattch/")
        env.set("GPGPUSIM_SETUP_ENVIRONMENT_WAS_RUN", "1")

    def setup_run_environment(self, env):
        env.set("CUDA_INSTALL_PATH", self.spec["cuda"].prefix)
