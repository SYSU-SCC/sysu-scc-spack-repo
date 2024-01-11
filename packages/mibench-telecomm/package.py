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


class MibenchTelecomm(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://vhosts.eecs.umich.edu/mibench/"
    url = "https://vhosts.eecs.umich.edu/mibench/telecomm.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version("1.0", sha256="cdcdc9bfa8ef7c78a91b9b682ad611ce762920e06a3b39140c22ded0e2e634aa")

    # FIXME: Add dependencies if required.

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        makefiles = [
            "./FFT/Makefile",
            "./CRC32/Makefile",
            "./adpcm/src/Makefile",
            "./gsm/Makefile",
        ]
        for mf in makefiles:
            makefile = FileFilter(mf)
            makefile.filter("gcc", "cc -Wl,--emit-relocs")
            makefile.filter("-static", "")

        with open("Makefile", "w") as mf:
            mf.write(
                """
all:
	make -C FFT
	make -C CRC32
	make -C adpcm/src
	make -C gsm
"""
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bins = [
            "adpcm/src/rawcaudio",
            "adpcm/src/rawdaudio",
            "adpcm/src/timing",
            "CRC32/crc",
            "FFT/fft",
            "gsm/bin/toast",
            "gsm/bin/untoast",
        ]
        for b in bins:
            install(b, prefix.bin)
        mkdirp(join_path(prefix, "data"))
        install_tree(".", join_path(prefix, "data"))
