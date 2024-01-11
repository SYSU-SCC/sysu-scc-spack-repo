# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class HplAi(AutotoolsPackage, CudaPackage, ROCmPackage):
    """An implement of HPL-AI Mixed-Precision Benchmark based on hpl-2.3"""

    homepage = "https://github.com/wu-kan/HPL-AI"
    git = homepage
    url = "https://github.com/wu-kan/HPL-AI/archive/refs/tags/v2.3d.tar.gz"
    maintainers = ["Junkang Huang", "Kan Wu"]

    # Note: HPL uses autotools starting with 2.3

    version("master", branch="master")
    version(
        "2.3d", sha256="C200A56B64BE759DC402FC1C15D7FD635862684BF196BAB0E7B543A9D093FA33".lower()
    )
    version("2.3c", sha256="4761135d5f6f9aa28071db1eb4658af773ddaae60e7b9b6b5e24c523549874b8")

    variant(
        "precision",
        default="float",
        description="The floating-point precision in LU Decomposition",
        values=("float", "double"),
        multi=False,
    )
    variant(
        "cublasGemmEx_computeType",
        default="none",
        description="Enumerant specifying the computation in cublasGemmEx",
        values=("none", "fp16", "bf16", "tf32", "fp32", "fp64"),
        multi=False,
    )

    depends_on("mpi@1.1:")
    depends_on("blas")
    depends_on("blaspp")
    depends_on("blaspp@2021.04.01: +cuda", when="+cuda")
    depends_on("blaspp@2021.04.01: +rocm", when="+rocm")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("autoconf-archive", type="build")

    conflicts("cublasGemmEx_computeType=fp16", when="@:2.3b")
    conflicts("cublasGemmEx_computeType=fp16", when="~cuda")
    conflicts("cublasGemmEx_computeType=fp16", when="precision=float ^cuda@:10.2.89")
    conflicts("cublasGemmEx_computeType=fp16", when="precision=double")

    conflicts("cublasGemmEx_computeType=bf16", when="@:2.3b")
    conflicts("cublasGemmEx_computeType=bf16", when="~cuda")
    conflicts("cublasGemmEx_computeType=bf16", when="precision=float ^cuda@:10.2.89")
    conflicts("cublasGemmEx_computeType=bf16", when="precision=double")

    conflicts("cublasGemmEx_computeType=tf32", when="@:2.3b")
    conflicts("cublasGemmEx_computeType=tf32", when="~cuda")
    conflicts("cublasGemmEx_computeType=tf32", when="precision=float ^cuda@:10.2.89")
    conflicts("cublasGemmEx_computeType=tf32", when="precision=double")

    conflicts("cublasGemmEx_computeType=fp32", when="~cuda")
    conflicts("cublasGemmEx_computeType=fp32", when="precision=double")

    conflicts("cublasGemmEx_computeType=fp64", when="~cuda")
    conflicts("cublasGemmEx_computeType=fp64", when="precision=float")

    force_autoreconf = True

    arch = "{0}-{1}".format(platform.system(), platform.processor())
    build_targets = ["arch={0}".format(arch)]

    @when("@2.3a:")
    def configure_args(self):
        filter_file(r"^libs10=.*", "libs10=%s" % self.spec["blas"].libs.ld_flags, "configure")

        cppflags = " -O3 -DOMPI_SKIP_MPICXX -DMPICH_SKIP_MPICXX "
        libs = ""
        ldflags = ""

        if "precision=float" in self.spec:
            if "cublasGemmEx_computeType=fp16" in self.spec:
                cppflags += " -DHPLAI_CUBLASGEMMEX_COMPUTETYPE=CUBLAS_COMPUTE_32F_FAST_16F "
            elif "cublasGemmEx_computeType=bf16" in self.spec:
                cppflags += " -DHPLAI_CUBLASGEMMEX_COMPUTETYPE=CUBLAS_COMPUTE_32F_FAST_16BF "
            elif "cublasGemmEx_computeType=tf32" in self.spec:
                cppflags += " -DHPLAI_CUBLASGEMMEX_COMPUTETYPE=CUBLAS_COMPUTE_32F_FAST_TF32 "
        elif "precision=double" in self.spec:
            cppflags += " -DHPLAI_T_AFLOAT=double "

        if "+cuda" in self.spec:
            cppflags += (
                " -DBLAS_HAVE_CUBLAS -DHPLAI_DEVICE_BLASPP_GEMM -DHPLAI_DEVICE_BLASPP_TRSM "
            )
            libs += " -lcudart -lcublas "
        if "+rocm" in self.spec:
            cppflags += (
                " -DBLAS_HAVE_ROCBLAS -DHPLAI_DEVICE_BLASPP_GEMM -DHPLAI_DEVICE_BLASPP_TRSM "
            )
            libs += " -lcudart -lrocblas "

        if (
            self.spec.satisfies("^intel-mkl")
            or self.spec.satisfies("^intel-oneapi-mkl")
            or self.spec.satisfies("^intel-parallel-studio+mkl")
        ):
            ldflags += "{0}".format(self.spec["blas"].libs.ld_flags)

        cfg = []
        if cppflags != "":
            cfg.append("CPPFLAGS=" + cppflags)
        if libs != "":
            cfg.append("LIBS=" + libs)
        if (ldflags) != "":
            cfg.append("LDFLAGS=" + ldflags)

        return cfg

    @run_after("install")
    def copy_dat(self):
        # The pre-2.3 makefile would include a default HPL.dat config
        # file in the bin directory
        install("./testing/ptest/HPL.dat", join_path(self.prefix.bin, "HPL.dat"))
