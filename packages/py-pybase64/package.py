# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPybase64(PythonPackage):
    """Fast Base64 implementation"""

    pypi = "pybase64/pybase64-1.4.2.tar.gz"

    license("BSD-2-Clause")

    version("1.4.2", sha256="46cdefd283ed9643315d952fe44de80dc9b9a811ce6e3ec97fd1827af97692d0")

    depends_on("py-setuptools", type="build")
