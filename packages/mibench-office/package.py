# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install automotive
#
# You can edit this file again by typing:
#
#     spack edit automotive
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import glob
from hashlib import sha256

from spack import *


class MibenchOffice(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://vhosts.eecs.umich.edu/mibench/"
    url = "https://vhosts.eecs.umich.edu/mibench/office.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version("1.0", sha256="e8bd0229346b8926dd61cfa8a377e9ce8751381dc669e062acc1b89df58eff4b")

    # FIXME: Add dependencies if required.
    depends_on("ghostscript", type="run")

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        makefiles = ["./ghostscript/src/Makefile", "./ghostscript/src/gcc-head.mak"]
        for mf in makefiles:
            makefile = FileFilter(mf)
            makefile.filter("gcc", "cc -Wl,--emit-relocs")
            makefile.filter("-static", "")

        makefiles = ["./ispell/Makefile", "./stringsearch/Makefile"]
        for mf in makefiles:
            makefile = FileFilter(mf)
            makefile.filter("gcc", "cc -Wl,--emit-relocs")
            makefile.filter("-static", "")

        for mf in glob.glob("./ghostscript/src/**/*.h", recursive=True) + glob.glob(
            "./ghostscript/src/**/*.c", recursive=True
        ):
            makefile = FileFilter(mf)
            makefile.filter("dprintf", "dbgprintf")

        for mf in ["./ispell/correct.c", "./ispell/ispell.h"]:
            makefile = FileFilter(mf)
            makefile.filter("getline", "mygetline")

        for mf in ["./ghostscript/src/time_.h"]:
            makefile = FileFilter(mf)
            makefile.filter(
                "#ifdef HAVE_SYS_TIME_H",
                "#include <stdlib.h>\n#include <time.h>\n#ifdef HAVE_SYS_TIME_H",
            )

        with open("Makefile", "w") as mf:
            mf.write(
                """
all:
	make -C ispell
	make -C stringsearch
"""
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bins = ["ispell/ispell", "stringsearch/search_small", "stringsearch/search_large"]
        for b in bins:
            install(b, prefix.bin)
        mkdirp(join_path(prefix, "data"))
        install_tree(".", join_path(prefix, "data"))
