# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Antlr4Complete(Package):
    """
    This package provides complete ANTLR tool, Java runtime and ST, which lets you run the tool and the generated code by version 4 of ANTLR (ANother Tool for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    url = "https://www.antlr.org/download/antlr-4.13.1-complete.jar"

    version(
        "4.13.1",
        sha256="bc13a9c57a8dd7d5196888211e5ede657cb64a3ce968608697e4f668251a8487",
        expand=False,
    )

    depends_on("java", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("*.jar", prefix.bin)
