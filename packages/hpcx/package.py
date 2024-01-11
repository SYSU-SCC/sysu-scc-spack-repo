# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import itertools
import os
import re
import sys

import llnl.util.tty as tty

from spack.util.environment import EnvironmentModifications


class Hpcx(AutotoolsPackage):
    # Current
    homepage = "https://www.open-mpi.org"
    url = "https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.0.tar.bz2"
    list_url = "https://www.open-mpi.org/software/ompi/"
    git = "https://github.com/open-mpi/ompi.git"
    version("2.6.0")
    provides("mpi")
    executables = ["mpirun"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r"Open MPI: (\S+)", output)
        return match.group(1) if match else None

    def setup_run_environment(self, env):
        # print(self.prefix.modulefiles.hpcx)
        # load_module(self.prefix.modulefiles.hpcx)
        # env.extend(EnvironmentModifications.from_sourcing_file(self.prefix.modulefiles.hpcx))
        # Because MPI is both a runtime and a compiler, we have to setup the
        # compiler components as part of the run environment.
        env.set("MPICC", join_path(self.prefix.bin, "mpicc"))
        env.set("MPICXX", join_path(self.prefix.bin, "mpic++"))
        env.set("MPIF77", join_path(self.prefix.bin, "mpif77"))
        env.set("MPIF90", join_path(self.prefix.bin, "mpif90"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

        # Use the spack compiler wrappers under MPI
        env.set("OMPI_CC", spack_cc)
        env.set("OMPI_CXX", spack_cxx)
        env.set("OMPI_FC", spack_fc)
        env.set("OMPI_F77", spack_f77)

        # See https://www.open-mpi.org/faq/?category=building#installdirs
        for suffix in [
            "PREFIX",
            "EXEC_PREFIX",
            "BINDIR",
            "SBINDIR",
            "LIBEXECDIR",
            "DATAROOTDIR",
            "DATADIR",
            "SYSCONFDIR",
            "SHAREDSTATEDIR",
            "LOCALSTATEDIR",
            "LIBDIR",
            "INCLUDEDIR",
            "INFODIR",
            "MANDIR",
            "PKGDATADIR",
            "PKGLIBDIR",
            "PKGINCLUDEDIR",
        ]:
            env.unset("OPAL_%s" % suffix)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, "mpicc")
        self.spec.mpicxx = join_path(self.prefix.bin, "mpic++")
        self.spec.mpifc = join_path(self.prefix.bin, "mpif90")
        self.spec.mpif77 = join_path(self.prefix.bin, "mpif77")
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, "libmpi_cxx.{0}".format(dso_suffix)),
            join_path(self.prefix.lib, "libmpi.{0}".format(dso_suffix)),
        ]

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
