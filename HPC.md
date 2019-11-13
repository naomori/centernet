# CenterNet動作環境の確認
現状の Docker Container で動作させている CenterNet を
Singularity 上で動作させようと思ったけど、コンテナイメージの変換は難しいみたい。

そこで、ABCI 環境に直接 CenterNet 動作環境を構築することにします。

まずは、現状の動作環境を洗い出します。
## NGC Container(pytorch:19.10-py3)のGPU関連

### CUDA
```bash
(CenterNet) root@centernet:~# nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Sun_Jul_28_19:07:16_PDT_2019
Cuda compilation tools, release 10.1, V10.1.243
```
### CuDNN
```bash
(CenterNet) root@centernet:~# apt list | grep cudnn
libcudnn7/now 7.6.4.38-1+cuda10.1 amd64 [installed,local]
libcudnn7-dev/now 7.6.4.38-1+cuda10.1 amd64 [installed,local]
```
### NCCL
```bash
(CenterNet) root@centernet:~# apt list | grep nccl
libnccl-dev/now 2.4.8-1+cuda10.1 amd64 [installed,local]
libnccl2/now 2.4.8-1+cuda10.1 amd64 [installed,local]
```

## Miniconda 環境
Miniconda のバージョンは以下を使っているみたい。
```bash
(CenterNet) root@centernet:~# conda --version
conda 4.7.12
```

conda のパッケージで注意すべきなものは、以下です。
```
pytorch		1.1.0	py3.6_cuda10.0.130_cudnn7.5.1_0	pytorch
torchvision	0.3.0	py36_cu10.0.130_1    		pytorch
opencv		4.1.1	py36h0cc45ee_2    		conda-forge
```
その他は、インストールの過程で入るものだったり、jupyter は不要だったり。

```bash
(CenterNet) root@centernet:~# conda list
# packages in environment at /opt/conda/envs/CenterNet:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main
attrs                     19.3.0                     py_0    conda-forge
backcall                  0.1.0                      py_0    conda-forge
blas                      1.0                         mkl
bleach                    3.1.0                      py_0    conda-forge
bzip2                     1.0.8                h516909a_1    conda-forge
ca-certificates           2019.9.11            hecc5488_0    conda-forge
cairo                     1.16.0            hfb77d84_1002    conda-forge
certifi                   2019.9.11                py36_0    conda-forge
cffi                      1.13.1           py36h2e261b9_0
cudatoolkit               10.0.130                      0
cycler                    0.10.0                     py_2    conda-forge
cython                    0.29.13          py36he6710b0_0
dbus                      1.13.6               he372182_0    conda-forge
dcnv2                     0.1                       dev_0    <develop>
decorator                 4.4.1                      py_0    conda-forge
defusedxml                0.6.0                      py_0    conda-forge
easydict                  1.9                        py_0    conda-forge
entrypoints               0.3                   py36_1000    conda-forge
expat                     2.2.5             he1b5a44_1004    conda-forge
ffmpeg                    4.1.3                h167e202_0    conda-forge
fontconfig                2.13.1            h86ecdb6_1001    conda-forge
freetype                  2.9.1                h8a8886c_1
gettext                   0.19.8.1          hc5be6a0_1002    conda-forge
giflib                    5.1.9                h516909a_0    conda-forge
glib                      2.58.3            h6f030ca_1002    conda-forge
gmp                       6.1.2             hf484d3e_1000    conda-forge
gnutls                    3.6.5             hd3a4fd2_1002    conda-forge
graphite2                 1.3.13            hf484d3e_1000    conda-forge
gst-plugins-base          1.14.5               h0935bb2_0    conda-forge
gstreamer                 1.14.5               h36ae1b5_0    conda-forge
harfbuzz                  2.4.0                h9f30f68_3    conda-forge
hdf5                      1.10.5          nompi_h3c11f04_1104    conda-forge
icu                       64.2                 he1b5a44_1    conda-forge
importlib_metadata        0.23                     py36_0    conda-forge
intel-openmp              2019.4                      243
ipykernel                 5.1.3            py36h5ca1d4c_0    conda-forge
ipython                   7.9.0            py36h5ca1d4c_0    conda-forge
ipython_genutils          0.2.0                      py_1    conda-forge
jasper                    1.900.1           h07fcdf6_1006    conda-forge
jedi                      0.15.1                   py36_0    conda-forge
jinja2                    2.10.3                     py_0    conda-forge
jpeg                      9c                h14c3975_1001    conda-forge
json5                     0.8.5                      py_0    conda-forge
jsonschema                3.1.1                    py36_0    conda-forge
jupyter_client            5.3.3                    py36_1    conda-forge
jupyter_core              4.5.0                      py_0    conda-forge
jupyterlab                1.2.0                      py_0    conda-forge
jupyterlab_server         1.0.6                      py_0    conda-forge
kiwisolver                1.1.0            py36hc9558a2_0    conda-forge
lame                      3.100             h14c3975_1001    conda-forge
libblas                   3.8.0                    14_mkl    conda-forge
libcblas                  3.8.0                    14_mkl    conda-forge
libclang                  9.0.0                hc9558a2_1    conda-forge
libedit                   3.1.20181209         hc058e9b_0
libffi                    3.2.1                hd88cf55_4
libgcc-ng                 9.1.0                hdf63c60_0
libgfortran-ng            7.3.0                hdf63c60_0
libiconv                  1.15              h516909a_1005    conda-forge
liblapack                 3.8.0                    14_mkl    conda-forge
liblapacke                3.8.0                    14_mkl    conda-forge
libllvm8                  8.0.1                hc9558a2_0    conda-forge
libllvm9                  9.0.0                hc9558a2_2    conda-forge
libpng                    1.6.37               hbc83047_0
libsodium                 1.0.17               h516909a_0    conda-forge
libstdcxx-ng              9.1.0                hdf63c60_0
libtiff                   4.0.10               h2733197_2
libuuid                   2.32.1            h14c3975_1000    conda-forge
libwebp                   1.0.2                h576950b_1    conda-forge
libxcb                    1.13              h14c3975_1002    conda-forge
libxkbcommon              0.9.1                hebb1f50_0    conda-forge
libxml2                   2.9.10               hee79883_0    conda-forge
llvmlite                  0.30.0           py36h8b12597_0    conda-forge
markupsafe                1.1.1            py36h14c3975_0    conda-forge
matplotlib                3.1.1                    py36_1    conda-forge
matplotlib-base           3.1.1            py36he7580a8_1    conda-forge
mistune                   0.8.4           py36h14c3975_1000    conda-forge
mkl                       2019.4                      243
mkl-service               2.3.0            py36he904b0f_0
mkl_fft                   1.0.14           py36ha843d7b_0
mkl_random                1.1.0            py36hd6b4f25_0
more-itertools            7.2.0                      py_0    conda-forge
nbconvert                 5.6.1                    py36_0    conda-forge
nbformat                  4.4.0                      py_1    conda-forge
ncurses                   6.1                  he6710b0_1
nettle                    3.4.1             h1bed415_1002    conda-forge
ninja                     1.9.0            py36hfd86e86_0
notebook                  6.0.1                    py36_0    conda-forge
nspr                      4.23                 he1b5a44_0    conda-forge
nss                       3.47                 he751ad9_0    conda-forge
numba                     0.46.0           py36hb3f55d8_1    conda-forge
numpy                     1.17.2           py36haad9e8e_0
numpy-base                1.17.2           py36hde5b4d6_0
olefile                   0.46                     py36_0
opencv                    4.1.1            py36h0cc45ee_2    conda-forge
openh264                  1.8.0             hdbcaa40_1000    conda-forge
openssl                   1.1.1c               h516909a_0    conda-forge
pandoc                    2.7.3                         0    conda-forge
pandocfilters             1.4.2                      py_1    conda-forge
parso                     0.5.1                      py_0    conda-forge
pcre                      8.43                 he1b5a44_0    conda-forge
pexpect                   4.7.0                    py36_0    conda-forge
pickleshare               0.7.5                 py36_1000    conda-forge
pillow                    6.2.0            py36h34e0f95_0
pip                       19.3.1                   py36_0
pixman                    0.38.0            h516909a_1003    conda-forge
progress                  1.3                      py36_0    conda-forge
prometheus_client         0.7.1                      py_0    conda-forge
prompt_toolkit            2.0.10                     py_0    conda-forge
pthread-stubs             0.4               h14c3975_1001    conda-forge
ptyprocess                0.6.0                   py_1001    conda-forge
pycocotools               2.0.0           py36h14c3975_1000    conda-forge
pycparser                 2.19                     py36_0
pygments                  2.4.2                      py_0    conda-forge
pyparsing                 2.4.2                      py_0    conda-forge
pyqt                      5.12.3           py36hcca6a23_0    conda-forge
pyqt5-sip                 4.19.18                  pypi_0    pypi
pyqtwebengine             5.12.1                   pypi_0    pypi
pyrsistent                0.15.5           py36h516909a_0    conda-forge
python                    3.6.9                h265db76_0
python-dateutil           2.8.0                      py_0    conda-forge
pytorch                   1.1.0           py3.6_cuda10.0.130_cudnn7.5.1_0    pytorch
pyzmq                     18.1.0           py36h1768529_0    conda-forge
qt                        5.12.5               hd8c4c69_1    conda-forge
readline                  7.0                  h7b6447c_5
scipy                     1.3.1            py36h921218d_2    conda-forge
send2trash                1.5.0                      py_0    conda-forge
setuptools                41.6.0                   py36_0
six                       1.12.0                   py36_0
sqlite                    3.30.1               h7b6447c_0
terminado                 0.8.2                    py36_0    conda-forge
testpath                  0.4.2                   py_1001    conda-forge
tk                        8.6.9             hed695b0_1003    conda-forge
torchvision               0.3.0           py36_cu10.0.130_1    pytorch
tornado                   6.0.3            py36h516909a_0    conda-forge
traitlets                 4.3.3                    py36_0    conda-forge
wcwidth                   0.1.7                      py_1    conda-forge
webencodings              0.5.1                      py_1    conda-forge
wheel                     0.33.6                   py36_0
x264                      1!152.20180806       h14c3975_0    conda-forge
xorg-kbproto              1.0.7             h14c3975_1002    conda-forge
xorg-libice               1.0.10               h516909a_0    conda-forge
xorg-libsm                1.2.3             h84519dc_1000    conda-forge
xorg-libx11               1.6.9                h516909a_0    conda-forge
xorg-libxau               1.0.9                h14c3975_0    conda-forge
xorg-libxdmcp             1.1.3                h516909a_0    conda-forge
xorg-libxext              1.3.4                h516909a_0    conda-forge
xorg-libxrender           0.9.10            h516909a_1002    conda-forge
xorg-renderproto          0.11.1            h14c3975_1002    conda-forge
xorg-xextproto            7.3.0             h14c3975_1002    conda-forge
xorg-xproto               7.0.31            h14c3975_1007    conda-forge
xz                        5.2.4                h14c3975_4
zeromq                    4.3.2                he1b5a44_2    conda-forge
zipp                      0.6.0                      py_0    conda-forge
zlib                      1.2.11               h7b6447c_3
zstd                      1.3.7                h0b5b093_0
```

- - -
# CenterNet 動作環境の構築

## python 環境のインストール
miniconda は pyenv 経由でインストールすることにします。

```bash
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
```bash
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

ここから先はABCI計算ノードで作業します。
一旦ログアウトする場合も再度ABCI計算ノードを立ち上げ直します。
```bash
$ qrsh -g gaa50053 -l rt_F=1
```

gcc-7.3.0 を利用するよう環境変数を設定します。
```bash
$ export PATH=/apps/gcc/7.3.0/bin:$PATH
$ export LD_LIBRARY_PATH=/apps/gcc/7.3.0/lib64:$LD_LIBRARY_PATH
```

miniconda のバージョンは現時点(2019/11/06)で最新のものをインストールします。
```bash
$ pyenv install miniconda3-4.3.30
$ pyenv global miniconda3-4.3.30
$ conda --version
conda 4.7.12
```
conda のバージョンは大丈夫そうです。

## CenterNet仮想環境の作成
ここからは、CenterNet の環境構築の際に行った作業と同じです。
```bash
$ conda create --name centernet python=3.6
```
centernetの仮想環境を作成したら、
```bash
$ conda init
$ exit
```
一旦ログアウトして再度ログインします。
```bash
$ qrsh -g gaa50053 -l rt_F=1
```

## Environment Module
docker の動作環境通りにモジュールをロードします。
**conda のインストール前にかならずロードしておく必要があるかも。**
```
$ module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
$ module list
Currently Loaded Modulefiles:
  1) cuda/10.1/10.1.243   2) cudnn/7.6/7.6.4      3) nccl/2.4/2.4.8-1
```

## CenterNet依存パッケージのインストール
centernet仮想環境を有効化し、作業を続行します。
```bash
$ conda activate centernet
(centernet)$ conda update -n base -c defaults conda
(centernet)$ conda install conda-build
(centernet)$ conda install pytorch=1.1 torchvision -c pytorch
(centernet)$ conda install cython
(centernet)$ conda install -c conda-forge opencv=4.1.1
(centernet)$ conda install -c conda-forge numba easydict scipy
(centernet)$ conda install -c conda-forge progress matplotlib
(centernet)$ conda install -c conda-forge pycocotools
```
ただ、このままだと 仮想環境 `centernet` のパスが通っておらず、
`import torch` が失敗してしまうので、
`~/.bash_profile` に以下の行を追加しておきます。
```
export PYTHONPATH=$PYTHONPATH:/home/acb11394zl/.pyenv/versions/miniconda3-4.3.30/envs/centernet/lib/python3.6/site-packages
```

## CenterNet のビルド

ABCIのインタラクティブノードに置いた CenterNet のソースコード中で
GPU付きの環境でビルドしなければならないものが２つあります。
したがって、インタラクティブジョブを利用することで、
それらをビルドします。
また、このビルド時に Default でインストールされている gcc-4.8.5 では
PyTorch のビルドにおいて Warning が出るため、gcc-7.3.0 を利用することにします。
（参考: https://docs.abci.ai/ja/tips/gcc-7.3.0）

ABCIのインタラクティブノードから、インタラクティブジョブを実行します。
```bash
$ qrsh -g gaa50053 -l rt_F=1
```

インタラクティブジョブ内では、
必要なモジュールとconda環境を準備します。
```bash
$ module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
$ conda activate centernet
```

gcc-7.3.0 を利用するよう環境変数を設定します。
```bash
$ export PATH=/apps/gcc/7.3.0/bin:$PATH
$ export LD_LIBRARY_PATH=/apps/gcc/7.3.0/lib64:$LD_LIBRARY_PATH
```

まずは１つ目。
```bash
$ cd /home/acb11394zl/centernet/CenterNet.org/src/lib/external
$ rm -rf build nms.cpython-36m-x86_64-linux-gnu.so
$ python setup.py build_ext --inplace
```

次に２つ目。
```bash
$ cd /home/acb11394zl/centernet/CenterNet.org/src/lib/models/networks/DCNv2
$ rm -rf build/ DCNv2.egg-info/ _ext.cpython-36m-x86_64-linux-gnu.so
$ sh ./make.sh
```

## CenterNet の実行
全然動かん。

必ずここで固まる。
```python
from trains.train_factory import train_factory
```
突破出来るかもしれない。
* すべての `*.py` に実行権限を付ける
* `trains/__init__.py` の作成し忘れ
