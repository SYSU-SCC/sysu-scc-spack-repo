# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGguf(PythonPackage):
    """A fast serialization and validation library, with builtin support for JSON, MessagePack, YAML, and TOML."""

    pypi = "gguf/gguf-0.17.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.17.1",
        sha256="36ad71aad900a3e75fc94ebe96ea6029f03a4e44be7627ef7ad3d03e8c7bcb53",
    )

    depends_on("py-poetry-core", type="build")
    depends_on("py-numpy@1.17:", type=["build", "run"])
    depends_on("py-tqdm@4.27:", type=["build", "run"])
    depends_on("py-pyyaml@5.1:", type=["build", "run"])
