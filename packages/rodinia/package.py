# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rodinia(MakefilePackage, CudaPackage):
    """Rodinia: Accelerating Compute-Intensive Applications with
    Accelerators"""

    homepage = "https://rodinia.cs.virginia.edu/doku.php"
    url = "https://www.cs.virginia.edu/~kw5na/lava/Rodinia/Packages/Current/rodinia_3.1.tar.bz2"

    version("3.1", sha256="faebac7c11ed8f8fcf6bf2d7e85c3086fc2d11f72204d6dfc28dc5b2e8f2acfd")

    depends_on("cuda")
    depends_on("freeglut")
    depends_on("glew")
    depends_on("gl")
    depends_on("glu")

    conflicts("~cuda")

    build_targets = ["CUDA"]

    variant(
        "cudart",
        default="default",
        description="build with nvcc --cudart shared to be used with gpgpu-sim",
        values=("default", "shared", "static", "none"),
        multi=False,
    )

    def edit(self, spec, prefix):
        # set cuda paths
        filter_file(
            "CUDA_DIR = /usr/local/cuda",
            "CUDA_DIR = {0}".format(self.spec["cuda"].prefix),
            "common/make.config",
            string=True,
        )

        filter_file(
            "SDK_DIR = /usr/local/cuda-5.5/samples/",
            "SDK_DIR = {0}/samples".format(self.spec["cuda"].prefix),
            "common/make.config",
            string=True,
        )

        filter_file(
            "nvcc", "nvcc -I../hybridsort", "cuda/cfd/Makefile", string=True  # fix helper_cuda.h
        )

        # fix broken makefile rule
        filter_file("%.o: %.[ch]", "%.o: %.c", "cuda/kmeans/Makefile", string=True)

        # fix missing include for lseek(), read()
        filter_file(
            "#include <stdint.h>",
            "#include <stdint.h>\n#include <unistd.h>",
            "cuda/mummergpu/src/suffix-tree.cpp",
            string=True,
        )

        makefiles = [  # find . -name *akefile
            "common/common.mk",
            "cuda/huffman/Makefile",
            "cuda/heartwall/AVI/makefile",
            "cuda/heartwall/Makefile",
            "cuda/cfd/Makefile",
            "cuda/pathfinder/Makefile",
            "cuda/nn/Makefile",
            "cuda/myocyte/Makefile",
            "cuda/hotspot/Makefile",
            "cuda/hybridsort/Makefile",
            "cuda/bfs/Makefile",
            "cuda/lavaMD/makefile",
            "cuda/gaussian/Makefile",
            "cuda/lud/tools/Makefile",
            "cuda/lud/cuda/Makefile",
            "cuda/lud/base/Makefile",
            "cuda/lud/Makefile",
            "cuda/nw/Makefile",
            "cuda/streamcluster/Makefile",
            "cuda/mummergpu/src/Makefile",
            "cuda/mummergpu/Makefile",
            "cuda/leukocyte/meschach_lib/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/Linux/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/Cray/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/OS2/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/RS6000/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/GCC/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/SGI/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/MicroSoft/makefile",
            "cuda/leukocyte/meschach_lib/MACHINES/SPARC/makefile",
            "cuda/leukocyte/CUDA/Makefile",
            "cuda/leukocyte/Makefile",
            "cuda/particlefilter/Makefile",
            "cuda/dwt2d/Makefile",
            "cuda/backprop/Makefile",
            "cuda/srad/srad_v1/makefile",
            "cuda/srad/srad_v2/Makefile",
            "cuda/srad/Makefile",
            "cuda/b+tree/Makefile",
            "cuda/hotspot3D/Makefile",
            "cuda/kmeans/Makefile",
            "others/rng/rng/latex/Makefile",
            "openmp/heartwall/makefile",
            "openmp/heartwall/AVI/makefile",
            "openmp/cfd/makefile",
            "openmp/pathfinder/Makefile",
            "openmp/nn/Makefile",
            "openmp/myocyte/Makefile",
            "openmp/hotspot/Makefile",
            "openmp/bfs/Makefile",
            "openmp/lavaMD/makefile",
            "openmp/lud/tools/Makefile",
            "openmp/lud/omp/Makefile",
            "openmp/lud/base/Makefile",
            "openmp/lud/Makefile",
            "openmp/nw/Makefile",
            "openmp/streamcluster/Makefile",
            "openmp/mummergpu/src/Makefile",
            "openmp/mummergpu/Makefile",
            "openmp/leukocyte/meschach_lib/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/Linux/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/Cray/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/OS2/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/RS6000/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/GCC/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/SGI/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/MicroSoft/makefile",
            "openmp/leukocyte/meschach_lib/MACHINES/SPARC/makefile",
            "openmp/leukocyte/OpenMP/Makefile",
            "openmp/leukocyte/Makefile",
            "openmp/particlefilter/Makefile",
            "openmp/backprop/Makefile",
            "openmp/srad/srad_v1/makefile",
            "openmp/srad/srad_v2/Makefile",
            "openmp/srad/Makefile",
            "openmp/b+tree/Makefile",
            "openmp/hotspot3D/Makefile",
            "openmp/kmeans/kmeans_serial/Makefile",
            "openmp/kmeans/Makefile",
            "openmp/kmeans/kmeans_openmp/Makefile",
            "Makefile",
            "opencl/heartwall/makefile",
            "opencl/cfd/Makefile",
            "opencl/pathfinder/makefile",
            "opencl/nn/Makefile",
            "opencl/myocyte/Makefile",
            "opencl/hotspot/Makefile",
            "opencl/hybridsort/Makefile",
            "opencl/bfs/Makefile",
            "opencl/lavaMD/makefile",
            "opencl/gaussian/Makefile",
            "opencl/lud/ocl/makefile",
            "opencl/lud/tools/Makefile",
            "opencl/lud/base/Makefile",
            "opencl/lud/Makefile",
            "opencl/nw/Makefile",
            "opencl/streamcluster/Makefile",
            "opencl/leukocyte/meschach_lib/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/Linux/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/Cray/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/OS2/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/RS6000/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/GCC/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/SGI/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/MicroSoft/makefile",
            "opencl/leukocyte/meschach_lib/MACHINES/SPARC/makefile",
            "opencl/leukocyte/OpenCL/Makefile",
            "opencl/leukocyte/Makefile",
            "opencl/particlefilter/Makefile",
            "opencl/dwt2d/Makefile",
            "opencl/backprop/Makefile",
            "opencl/srad/makefile",
            "opencl/b+tree/Makefile",
            "opencl/hotspot3D/Makefile",
            "opencl/kmeans/Makefile",
            "data/nn/inputGen/Makefile",
            "data/hotspot/inputGen/Makefile",
            "data/bfs/inputGen/Makefile",
            "data/kmeans/inpuGen/Makefile",
        ]

        for makefile in makefiles:
            filter_file("-arch sm_[0-9]+", "", makefile)
            filter_file("-arch=sm_[0-9]+", "", makefile)
            filter_file("--gpu-name sm_[0-9]+", "", makefile)
            filter_file("--gpu-architecture=compute_[0-9]+", "", makefile)
            filter_file("--gpu-code=compute_[0-9]+", "", makefile)
            filter_file(
                "nvcc",
                "nvcc -arch=sm_{0}".format(spec.variants["cuda_arch"].value[0])
                + (
                    ""
                    if "cudart=default" in self.spec
                    else " --cudart " + spec.variants["cudart"].value
                ),
                makefile,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("bin/linux/cuda", prefix.bin)
        mkdirp(join_path(prefix, "data"))
        install_tree("data", join_path(prefix, "data"))
