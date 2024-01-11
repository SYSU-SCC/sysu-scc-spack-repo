# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SysuLang(CMakePackage):
    """A mini, simple and modular Compiler for SYsU (a tiny C language)."""

    homepage = "https://github.com/arcsysu/SYsU-lang"
    url = "https://github.com/arcsysu/SYsU-lang/archive/v11.0.7.20221118.tar.gz"
    git = homepage + ".git"

    maintainers = ["wu-kan"]

    version(
        "12.0.0.20230529",
        sha256="14af349cc694b682e0b899aee589609c208280c10331af939dce54b83d7c44e7",
    )
    version(
        "11.0.7.20221118",
        sha256="9c7e92056f11f451a314b2f7f4684cb446235d389ded455ce1df294330fd15fd",
    )
    version("latest", branch="latest")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("llvm@11.0.0:+clang", type="link")
    depends_on("python@3.8.0:", type="run")
