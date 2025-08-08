# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyVllm(PythonPackage, CudaPackage):
    """A high-throughput and memory-efficient inference and serving engine for LLMs"""

    license("Apache-2.0")
    homepage = "https://docs.vllm.ai/"
    git = "https://github.com/vllm-project/vllm.git"
    url = "https://github.com/vllm-project/vllm/releases/download/v0.8.5.post1/vllm-0.8.5.post1.tar.gz"

    # Exact set of modules is version- and variant-specific, just attempt to import the
    # core libraries to ensure that the package was successfully installed.
    import_modules = ["vllm", "vllm.LLM", "vllm.SamplingParams"]

    version("main", branch="main")
    version("0.10.0", sha256="a44e9013db26082a82c3931ed8772ac884d6d60566d36ecdb0e8dc01c65b241a")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with when("@0.10.0"):
        # https://github.com/vllm-project/vllm/blob/v0.10.0/requirements/cuda.txt
        depends_on("py-numba@0.61.2", type=["run"])
        depends_on("py-torch@2.7.1", type=["build", "run"])
        depends_on("py-torchaudio@2.7.1", type=["run"])
        depends_on("py-torchvision@0.22.1", type=["run"])
        depends_on("python@:3.12", type=["build", "run"])
        depends_on("py-triton@3.3.1", type=["build", "run"])

    with default_args(type="build"):
        # https://github.com/vllm-project/vllm/blob/v0.10.0/requirements/build.txt
        depends_on("cmake@3.26.1:")
        depends_on("ninja")
        depends_on("py-packaging@24.2:")
        depends_on("py-setuptools@77.0.3:79")
        depends_on("py-setuptools-scm@8:")
        # depends_on("py-wheel") # inherited if `pip` is the build system
        depends_on("py-regex")

    with default_args(type=("build", "run")):
        depends_on("py-jinja2@3.1.6:")
        depends_on("py-torch+custom-protobuf")

    with default_args(type="run"):
        # https://github.com/vllm-project/vllm/blob/v0.10.0/requirements/common.txt
        depends_on("py-regex")
        depends_on("py-cachetools")
        depends_on("py-psutil")
        depends_on("py-sentencepiece")
        depends_on("py-numpy")
        depends_on("py-requests@2.26.0:")
        depends_on("py-tqdm")
        depends_on("py-blake3")
        depends_on("py-py-cpuinfo")
        depends_on("py-transformers") # @4.53.2:
        depends_on("py-huggingface-hub@0.33.0:")
        depends_on("py-tokenizers@0.21:") # 0.21.1
        depends_on("protobuf")
        depends_on("py-fastapi@0.115.0:+all")
        depends_on("py-aiohttp")
        depends_on("py-openai@1.87.0:1.90.0")
        depends_on("py-pydantic@2.10:")
        depends_on("py-prometheus-client@0.18.0:")
        depends_on("py-pillow")
        depends_on("py-prometheus-fastapi-instrumentator")
        depends_on("py-tiktoken@0.6.0:")

        depends_on("py-llguidance@0.7.11:0.7")

        depends_on("py-diskcache") # 5.6.3

        depends_on("py-xgrammar") # 0.1.21
        depends_on("py-typing-extensions@4.10:")
        depends_on("py-filelock") # 3.16.1
        depends_on("py-partial-json-parser")
        depends_on("py-pyzmq@25.0.0:")
        depends_on("py-msgspec")
        depends_on("py-gguf@0.13.0:")

        depends_on("py-einops")
        depends_on("py-compressed-tensors@0.10.2")

        depends_on("py-cloudpickle")

        depends_on("py-cbor2")
        depends_on("py-pybase64")

        depends_on("py-numba")
        depends_on("py-torchaudio")
        depends_on("py-torchvision")
        depends_on("py-triton")

    variant("cuda", default=True, description="Use CUDA")
    conflicts("~cuda")

    patch(
        "https://github.com/vllm-project/vllm/pull/21804.patch",
        sha256="e6d46576345622ff96d563368f9ecd0df72933590acbfde716a01fe177e528ce",
        when="@0.9:"
    )

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # If oom error, try lowering the number of jobs with `spack install -j`
        env.set("MAX_JOBS", str(make_jobs))
