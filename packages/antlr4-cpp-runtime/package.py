# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Antlr4CppRuntime(CMakePackage):
    """
    This package provides runtime libraries required to use parsers
    generated for the Cpp language by version 4 of ANTLR (ANother Tool
    for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    url = "https://www.antlr.org/download/antlr4-cpp-runtime-4.13.1-source.zip"
    version("4.13.1", sha256="d350e09917a633b738c68e1d6dc7d7710e91f4d6543e154a78bb964cfd8eb4de")

    def cmake_args(self):
        args = [
            self.define("ANTLR_BUILD_CPP_TESTS", "OFF"),
            self.define("WITH_DEMO", "Off"),
            self.define("WITH_LIBCXX", "Off"),
            self.define("WITH_STATIC_CRT", "Off"),
        ]
        return args

    def install(self, spec, prefix):
        super().install(spec, prefix)
        mkdirp(join_path(prefix.lib, "cmake", "antlr4"))
        install_tree("cmake", join_path(prefix.lib, "cmake", "antlr4"))
