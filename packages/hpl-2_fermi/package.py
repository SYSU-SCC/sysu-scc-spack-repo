# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


class Hpl2Fermi(AutotoolsPackage, CudaPackage):
    """HPL is a software package that solves a (random) dense linear system
    in double precision (64 bits) arithmetic on distributed-memory computers.
    It can thus be regarded as a portable as well as freely available
    implementation of the High Performance Computing Linpack Benchmark."""

    homepage = "https://developer.nvidia.com/rdp/assets/cuda-accelerated-linpack-linux64"

    # Note: HPL uses autotools starting with 2.3

    version(
        "15",
        sha256="16DD21AF22FCED613923A6CB09805D63952FC9C9F278CB7582061A43FE39A408".lower(),
        url="https://cdn.jsdelivr.net/gh/SYSU-SCC/HybridHPL/src/hpl-2.0_FERMI_v15.tgz",
    )

    depends_on("mpi@1.1:")
    depends_on("mkl")

    # hpl-2.3 adds support for openmpi 4
    conflicts("^openmpi@4.0.0:")
    conflicts("~cuda")

    parallel = False

    arch = "{0}-{1}".format(platform.system(), platform.processor())
    build_targets = ["arch={0}".format(arch)]

    @when("@:15")
    def autoreconf(self, spec, prefix):
        # Prevent sanity check from killing the build
        touch("configure")

    @when("@:15")
    def configure(self, spec, prefix):
        # List of configuration options
        # Order is important
        config = []

        config.extend(
            [
                # Shell
                "SHELL        = /bin/sh",
                "CD           = cd",
                "CP           = cp",
                "LN_S         = ln -fs",
                "MKDIR        = mkdir -p",
                "RM           = /bin/rm -f",
                "TOUCH        = touch",
                # Platform identifier
                "ARCH         = {0}".format(self.arch),
                # HPL Directory Structure / HPL library
                "TOPdir       = {0}".format(os.getcwd()),
                "INCdir       = $(TOPdir)/include",
                "BINdir       = $(TOPdir)/bin/$(ARCH)",
                "LIBdir       = $(TOPdir)/lib/$(ARCH)",
                "HPLlib       = $(LIBdir)/libhpl.a",
                # Message Passing library (MPI)
                "MPinc        = {0}".format(spec["mpi"].prefix.include),
                "MPlib        = -L{0}".format(spec["mpi"].prefix.lib),
                # Linear Algebra library (BLAS or VSIPL)
                "LAinc        = {0} -I{1} ".format(
                    spec["mkl"].prefix.include, spec["cuda"].prefix.include
                ),
                "LAdir        = -L$(TOPdir)/src/cuda -L{0} -L{1}".format(
                    spec["mkl"].prefix.lib + "/intel64", spec["cuda"].prefix.lib
                ),
                "LAlib        = $(LAdir) -ldgemm -lcuda -lcudart -lcublas -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -liomp5",
                # F77 / C interface
                "F2CDEFS      = -DAdd__ -DF77_INTEGER=int -DStringSunStyle",
                # HPL includes / libraries / specifics
                "HPL_INCLUDES = -I$(INCdir) -I$(INCdir)/$(ARCH) " + "-I$(LAinc) -I$(MPinc)",
                "HPL_LIBS     = $(HPLlib) $(LAlib) $(MPlib)",
                "HPL_OPTS     = -DCUDA ",
                "HPL_DEFS     = $(F2CDEFS) $(HPL_OPTS) $(HPL_INCLUDES)",
                # Compilers / linkers - Optimization flags
                "CC           = {0}".format(spec["mpi"].mpicc),
                "CCNOOPT      = $(HPL_DEFS) -O0 -w",
                "CCFLAGS = $(HPL_DEFS) -fomit-frame-pointer -O3 -funroll-loops -W -Wall -fopenmp",
                "LINKER       = $(CC)",
                "LINKFLAGS    = $(CCFLAGS) $(OMP_DEFS)",
                "ARCHIVER     = ar",
                "ARFLAGS      = r",
                "RANLIB       = echo",
            ]
        )

        # Write configuration options to include file
        with open("Make.{0}".format(self.arch), "w") as makefile:
            for var in config:
                makefile.write("{0}\n".format(var))

    @when("@:15")
    def install(self, spec, prefix):
        # Manual installation
        install_tree(join_path("bin", self.arch), prefix.bin)
        install_tree(join_path("lib", self.arch), prefix.lib)
        install("./src/cuda/libdgemm.so.1.0.1", join_path(self.prefix.lib, "libdgemm.so.1"))
        install_tree(join_path("include", self.arch), prefix.include)
        install_tree("man", prefix.man)
