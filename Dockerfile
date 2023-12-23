# syntax=docker/dockerfile:1.4
FROM debian:bullseye-slim
ARG SCC_OPT=/opt
WORKDIR ${SCC_OPT}
COPY . sysu-scc-spack-repo
ENV SCC_SETUP_ENV=${SCC_OPT}/sysu-scc-spack-repo/share/sysu-scc-spack-repo/setup-env.sh
RUN <<EOF
apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    clang-11 python3 \
    patch bash make \
    tar gzip unzip bzip2 xz-utils \
    file git ca-certificates \
    gpg apt-transport-https wget

wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

apt-get update -y
apt-get upgrade -y
apt-get install --no-install-recommends -y \
    code

apt-get autoremove -y
apt-get clean -y
rm -rf /var/lib/apt/lists/*
bash $(dirname $SCC_SETUP_ENV)/init-env.sh
EOF
