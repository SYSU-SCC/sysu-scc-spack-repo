# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SysuLang(CMakePackage):
    """A mini, simple and modular Compiler for SYsU (a tiny C language)."""

    homepage = "https://github.com/arcsysu/SYsU-lang"
    url = "https://github.com/arcsysu/SYsU-lang/archive/refs/tags/v2404.0.0.20240115.tar.gz"
    git = homepage + ".git"

    maintainers = ["wu-kan"]

    version("latest", branch="latest")
    version(
        "2404.0.0.20240115",
        sha256="fe2a498c6dea20cb7ab248fe48642aa3e5ec560f4c63d64f6a8d7126da00a7ee")
    version(
        "12.0.0.20230529",
        sha256="14af349cc694b682e0b899aee589609c208280c10331af939dce54b83d7c44e7",
    )
    version(
        "11.0.7.20221118",
        sha256="9c7e92056f11f451a314b2f7f4684cb446235d389ded455ce1df294330fd15fd",
    )

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("antlr4-complete", type=["build"], when="@2404.0.0.20240115:")
    depends_on("antlr4-cpp-runtime", type=["build", "run"], when="@2404.0.0.20240115:")
    depends_on("libuuid", type=["build", "link"], when="^antlr4-cpp-runtime@:4.10.1")
    depends_on("llvm@11.0.0:+clang", type=["link", "run"])
    depends_on("python@3.8.0:", type="run")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("^antlr4-complete"):
            print(join_path(self.spec["antlr4-complete"].prefix.bin, "antlr-complete.jar"))
            args.append(self.define("ANTLR4_JAR_LOCATION", join_path(self.spec["antlr4-complete"].prefix.bin, "antlr-complete.jar")))
        if self.spec.satisfies("^llvm@17.0.0:"):
            args.append(self.define("CMAKE_CXX_STANDARD", "17"))
        return args