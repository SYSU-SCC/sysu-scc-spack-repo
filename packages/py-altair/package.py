# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAltair(PythonPackage):
    """Declarative statistical visualization library for Python"""

    pypi = "altair/altair-5.2.0.tar.gz"

    license("BSD-3-Clause")

    version("5.2.0", sha256="2ad7f0c8010ebbc46319cc30febfb8e59ccf84969a201541c207bc3a4fa6cf81")
    version("5.1.2", sha256="e5f52a71853a607c61ce93ad4a414b3d486cd0d46ac597a24ae8bd1ac99dd460")
    version("5.1.1", sha256="ad6cd6983c8db69a34dd68e42653f6172b7fc3775b7190005107f1b4fc60d64d")
    version("5.1.0", sha256="46d2b1a9fa29eeed24513262cb1de13a40d55c04580fc21799d5de3991fea8ff")
    version("5.0.1", sha256="087d7033cb2d6c228493a053e12613058a5d47faf6a36aea3ff60305fd8b4cb0")
    version("5.0.0rc3", sha256="93ff660e45ad5b783057d331ddc489f9331cdf121e8450ddba2b71b35242d708")
    version("5.0.0rc2", sha256="aab5f1fdb02f9b52cb6a648ceb5604d8bd8fd8d4dfb6c8ecf29660ad9ad75602")
    version("5.0.0rc1", sha256="b9f565040df773dc915a708ea30f37a0d04a307de4957c1a719eaf9492c627a0")
    version("5.0.0", sha256="394c3d8be96f9cc90e15a0eee3634cc5b6f19e470fd2045759892623bd9a3fb2")
    version("4.2.2", sha256="39399a267c49b30d102c10411e67ab26374156a84b1aeb9fcd15140429ba49c5")
    version("4.2.1", sha256="4939fd9119c57476bf305af9ca0bd1aa7779b2450b874d3623660e879d0fcad1")
    version("4.2.0rc1", sha256="1b79863889c347fd38de419201b7b43504a460cb915ce57ce57796630d9f3fe9")
    version("4.2.0", sha256="d87d9372e63b48cd96b2a6415f0cf9457f50162ab79dc7a31cd7e024dd840026")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")
    depends_on("py-entrypoints", type=("build", "run"), when="@2.0.0:4")

    depends_on("py-hatchling", type=("build"), when="@5.0.0:")
    depends_on("py-packaging", type=("build", "run"), when="@5.1.0:")

    depends_on("py-importlib-metadata", type=("build", "run"), when="@5.0.0:5.0")
    depends_on("py-typing-extensions@4.0.1:", type=("build", "run"), when="@5.0.0:")
    depends_on("py-jsonschema@3.0.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@0.18:", type=("build", "run"))
    depends_on("py-pandas@0.25:", type=("build", "run"), when="@5.1.0:")
    depends_on("py-toolz", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
