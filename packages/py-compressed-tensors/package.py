# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCompressedTensors(PythonPackage):
    """Library for utilization of compressed safetensors of neural network models"""

    pypi = "compressed-tensors/compressed_tensors-0.10.2.tar.gz"

    license("Apache 2.0")

    version("0.10.2", sha256="6de13ac535d7ffdd8890fad3d229444c33076170acaa8fab6bab8ecfa96c1d8f")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@8:", type="build")
