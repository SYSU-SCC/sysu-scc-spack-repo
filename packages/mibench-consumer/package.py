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

from hashlib import sha256

from spack import *


class MibenchConsumer(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://vhosts.eecs.umich.edu/mibench/"
    url = "https://vhosts.eecs.umich.edu/mibench/consumer.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version("1.0", sha256="86d76a66fa567953c7b814a6c6e816c6af0afab59610160acb8036899d03d1f9")

    # FIXME: Add dependencies if required.
    depends_on("libmad", type="run")
    depends_on("libtiff", type="run")
    depends_on("lame", type="run")

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        makefiles = [
            "./jpeg/jpeg-6a/Makefile",
            "./lame/lame3.70/Makefile",
            "./typeset/lout-3.24/Makefile",
        ]
        for mf in makefiles:
            makefile = FileFilter(mf)
            makefile.filter("gcc", "cc -Wl,--emit-relocs")
            makefile.filter("-static", "")
            makefile.filter("-lncurses", "")
            makefile.filter("-DBRHIST", "")

        with open("Makefile", "w") as mf:
            mf.write(
                """
all:
	make -C jpeg/jpeg-6a
	make -C typeset/lout-3.24
"""
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bins = ["jpeg/jpeg-6a/cjpeg", "jpeg/jpeg-6a/djpeg", "typeset/lout-3.24/lout"]
        for b in bins:
            install(b, prefix.bin)
        mkdirp(join_path(prefix, "data"))
        install_tree(".", join_path(prefix, "data"))
