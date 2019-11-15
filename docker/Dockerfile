FROM nvcr.io/nvidia/pytorch:19.10-py3
MAINTAINER morita.n morita.n@jp.panasonic.com

RUN : "create proxy.conf for apt" && { \
    echo "Acquire::http::Proxy    \"http://proxy.mei.co.jp:8080\";"; \
    echo "Acquire::https::Proxy   \"http://proxy.mei.co.jp:8080\";"; \
    echo "Acquire::ftp::Proxy     \"http://proxy.mei.co.jp:8080\";"; \
} | tee /etc/apt/apt.conf.d/proxy.conf

RUN set -x && \
    apt update && \
    apt upgrade -y && \
    apt install -y \
        libgl1-mesa-glx \
        openssh-server

RUN : "add proxy settings for conda" && { \
    echo "proxy_servers:"; \
    echo "    http: http://proxy.mei.co.jp:8080"; \
    echo "    https: http://proxy.mei.co.jp:8080"; \
} | tee /root/.condarc

RUN : "add proxy settings for git" && { \
    echo "[http]"; \
    echo "    proxy = http://proxy.mei.co.jp:8080"; \
    echo "[https]"; \
    echo "    proxy = http://proxy.mei.co.jp:8080"; \
} | tee /root/.gitconfig

SHELL ["/bin/bash", "-l", "-c"]

RUN : "create CenterNet environment with python 3.6 " && \
    conda create --name centernet python=3.6 && \
    conda init && \
    exit

RUN : "install necessary packages" && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate centernet && \
    conda update -y -n base -c defaults conda && \
    conda install -y -c pytorch pytorch=1.1 torchvision && \
    conda install -y -c conda-forge Cython && \
    conda install -y -c conda-forge opencv=4.1.1 && \
    conda install -y -c conda-forge numba easydict scipy && \
    conda install -y -c conda-forge progress matplotlib && \
    conda install -y -c conda-forge pycocotools && \
    conda install -y -c conda-forge jupyterlab

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

COPY jupyter_notebook_config.py /root/.jupyter/
COPY jupyterlab_start.sh /usr/local/bin/
COPY sshd_config /etc/ssh/

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
