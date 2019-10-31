# centernet
I'm struggling with CenterNet.

- - -
# Environment
docker&nvidia-dockerを使っています。

[CenterNet(Object as Points)](https://arxiv.org/abs/1904.07850)
[(github)](https://github.com/xingyizhou/CenterNet)をDockerコンテナで
動作させるまでの手順を記録します。

## download the image for pytorch

土台となるイメージを[NGC](https://ngc.nvidia.com/)から持ってきます。
持ってくるのは `CONTAINERS` - `DEEP LEARNING`に用意された
PyTorch 用のイメージ(2019/10/09 version 19.09-py3)です。
サイズは 3.28 GB なので気長に待ちます。

```bash
$ docker pull nvcr.io/nvidia/pytorch:19.09-py3
```

## create a container
コンテナを生成します。
ボリュームなども必要に応じて指定してください。

`--net host`, `-e DISPLAY`, `-v $HOME/.Xauthority` などは、
SSH + X11 転送で接続しているリモートホスト上で走っている
Docker コンテナの中で X client を動作させたときに、
ssh client 側の X server に接続させたいときの設定なので、
必要なければオプション指定しなくても良いと思います。

```bash
docker run --detach \
        --net host \
	-e DISPLAY=$DISPLAY \
        --gpus all \
        --shm-size=1g --ulimit memlock=-1 \
        -it \
	-v $HOME/.Xauthority:/root/.Xauthority:rw \
        -v /home/arc2018:/workspace/arc2018 \
        --hostname centernet \
        --name centernet \
        nvcr.io/nvidia/pytorch:19.09-py3
```

## setup container
コンテナにログインして設定作業を進めます。

```bash
$ docker exec -it centernet bash
```

### environment variables
環境変数にプロキシ設定を追加しておきます。

```bash
(CenterNet) root@centernet:~# vim ~/.bashrc
export http_proxy=http://[プロキシアドレス]:[ポート番号]
export https_proxy=http://[プロキシアドレス]:[ポート番号]
export ftp_proxy=http://[プロキシアドレス]:[ポート番号]
export proxy=http://[プロキシアドレス]:[ポート番号]
```

### apt
まずは、Ubuntu のパッケージをインストールするために
プロキシ設定(社内だとプロキシを超える必要があったりします)をします。

```bash
root@centernet:~# vim /etc/apt/apt.conf.d/proxy.conf
```
```config
Acquire::http::Proxy    "http://<proxy-ip>:<proxy-port>";
Acquire::https::Proxy   "http://<proxy-ip>:<proxy-port>";
Acquire::ftp::Proxy     "http://<proxy-ip>:<proxy-port>";
```
```bash
root@centernet:~# apt update && apt upgrade -y
```

### conda
CenterNet の環境は conda で構築するようなので、
conda でもプロキシを超えられるように設定しておきます。

`.condarc` は python スクリプトなので、
インデント(spacex4)に注意してください。

```bash
root@centernet:~# vim ~/.condarc
```
```config
proxy_servers:
    http: http://[プロキシアドレス]:[ポート番号]
    https: https://[プロキシアドレス]:[ポート番号]
```

### git
CenterNet の source codes は github で公開されているため、
git でもプロキシを超えられるように設定しておきます。

```bash
(CenterNet) root@centernet:~# vim ~/.gitconfig
```
```config
[http]
    proxy = http://[プロキシアドレス]:[ポート番号]
[https]
    proxy = http://[プロキシアドレス]:[ポート番号]
```

## setup centernet working environment

[INSTALL.md](https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md)
にしたがってインストール作業を進めます。

### conda

```bash
root@centernet:~# conda create --name CenterNet python=3.6
```
```bash
root@centernet:~# conda init
no change     /opt/conda/condabin/conda
no change     /opt/conda/bin/conda
no change     /opt/conda/bin/conda-env
no change     /opt/conda/bin/activate
no change     /opt/conda/bin/deactivate
no change     /opt/conda/etc/profile.d/conda.sh
no change     /opt/conda/etc/fish/conf.d/conda.fish
no change     /opt/conda/shell/condabin/Conda.psm1
no change     /opt/conda/shell/condabin/conda-hook.ps1
no change     /opt/conda/lib/python3.6/site-packages/xontrib/conda.xsh
no change     /opt/conda/etc/profile.d/conda.csh
modified      /root/.bashrc

==> For changes to take effect, close and re-open your current shell. <==
```

一旦、shell を抜けて再度ログインし直します。
```bash
root@centernet:~# exit
```
```bash
$ docker exec -it centernet bash
```

CenterNet は pytorch 0.4.1 で開発をしたようですが、
pytorch 1.1.0 で実行できた人がいて、情報を共有してくれているようなので、
[こちらに](https://github.com/xingyizhou/CenterNet/issues/7)にしたがって、作業を進めます。

```bash
(base) root@centernet:/workspace# conda activate CenterNet
(CenterNet) root@centernet:/workspace#
(CenterNet) root@centernet:/workspace# conda install pytorch=1.1 torchvision -c pytorch
```

### Download CenterNet

```bash
(CenterNet) root@centernet:~# git clone https://github.com/xingyizhou/CenterNet.git
```

作業を進める上で python パッケージが必要なのでインストールしておきます。

```bash
(CenterNet) root@centernet:~/CenterNet/src/lib/external# conda install Cython
```

### 1.build nms

```bash
(CenterNet) root@centernet:~# cd CenterNet/src/lib/external/
(CenterNet) root@centernet:~/CenterNet/src/lib/external# python setup.py build_ext --inplace
```
多少 warning が出ますが、気にしなくて大丈夫みたいです。


### 2. clone and build original DCN2

```bash
(CenterNet) root@centernet:~/CenterNet/src/lib/external# cd
(CenterNet) root@centernet:~# cd CenterNet/src/lib/models/networks/
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks# rm -rf DCNv2/
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks# git clone https://github.com/CharlesShang/DCNv2
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks# cd DCNv2/
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks/DCNv2# find ./ -type f -name "dcn_v2_cuda.cu"
./src/cuda/dcn_v2_cuda.cu
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks/DCNv2# vim ./src/cuda/dcn_v2_cuda.cu
```
```diff
--- src/cuda/dcn_v2_cuda.cu.orig        2019-10-10 10:20:10.745370692 +0000
+++ src/cuda/dcn_v2_cuda.cu     2019-10-10 10:19:51.185370879 +0000
@@ -8,7 +8,8 @@
 #include <THC/THCAtomics.cuh>
 #include <THC/THCDeviceUtils.cuh>

-extern THCState *state;
+//extern THCState *state;
+THCState *state = at::globalContext().lazyInitCUDA();

 // author: Charles Shang
 // https://github.com/torch/cunn/blob/master/lib/THCUNN/generic/SpatialConvolutionMM.cu
```

```bash
(CenterNet) root@centernet:~/CenterNet/src/lib/models/networks/DCNv2# python setup.py build develop
```
これも多少 warning が出ますが、大丈夫そうです。

### 3. test

demo スクリプトで `import cv2` を要求されるので、以下でインストールしておきます。
結構いろいろパッケージがインストールされるので気長に待つこと。

また、opencv は 4.X でないと駄目みたいです。
`conda install -c conda-forge opencv` とすると、3.X がインストールされるのですが、
CenterNet では 4.X が前提みたいです。

```bash
(CenterNet) root@centernet:~# conda update -n base -c defaults conda
(CenterNet) root@centernet:~# conda install -c conda-forge opencv=4.1.1
(CenterNet) root@centernet:~# conda install -c conda-forge numba easydict scipy
(CenterNet) root@centernet:~# conda install -c conda-forge progress matplotlib
(CenterNet) root@centernet:~# apt install libgl1-mesa-glx
```

また、テストの前に model をダウンロードする必要があるので、
[Model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)から
ダウンロードして、以下のディレクトリに配置してください。

```bash
(CenterNet) root@centernet:~/CenterNet/models# pwd
/root/CenterNet/models
(CenterNet) root@centernet:~/CenterNet/models# ls
ctdet_coco_dla_1x.pth  ctdet_coco_dla_2x.pth  ctdet_coco_hg.pth  ctdet_coco_resdcn101.pth  ctdet_coco_resdcn18.pth
```

テストしてみます。

```bash
(CenterNet) root@centernet:~/CenterNet/src# python demo.py ctdet --demo ../images/17790319373_bd19b24cfc_k.jpg --load_model ../models/ctdet_coco_dla_2x.pth --debug 2
```
これも imagenet のモデル?をダウンロードしているみたいので、気長に待つこと。

以下のように言われて実行できず...

```bash
This application failed to start because it could not find or load the Qt platform plugin "xcb"
in "".

Available platform plugins are: eglfs, minimal, minimalegl, offscreen, vnc, xcb.

Reinstalling the application may fix this problem.
Aborted (core dumped)
```

[ここ](https://askubuntu.com/questions/308128/failed-to-load-platform-plugin-xcb-while-launching-qt5-app-on-linux-without/1091277)を見ると、Qt関連のライブラリを入れ直せとあるので、やってみる。

```bash
(base) root@centernet:/workspace# apt-get --reinstall install libqt5dbus5 \
libqt5widgets5 libqt5network5 libqt5gui5 libqt5core5a \
libdouble-conversion1 libxcb-xinerama0
```

やってみると、上手く行った気がする。
```bash
(CenterNet) root@centernet:~/CenterNet/src# python demo.py ctdet --demo ../images/17790319373_bd19b24cfc_k.jpg --load_
model ../models/ctdet_coco_dla_2x.pth --debug 2
Fix size testing.
training chunk_sizes: [1]
The output will be saved to  /root/CenterNet/src/lib/../../exp/ctdet/default
heads {'hm': 80, 'wh': 2, 'reg': 2}
Creating model...
loaded ../models/ctdet_coco_dla_2x.pth, epoch 230
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'
qt.qpa.screen: QXcbConnection: Could not connect to display localhost:10.0
Could not connect to any X display.
```
が、Xの転送が上手く行っていない。

こんな感じでコンテナを作ってみたりもしたけど、駄目っぽい。
docker ホスト側で X server 上がっていないと駄目なんじゃないかなと
思ってみたり。

```bash
export XAUTHORITY=$HOME/.Xauthority
docker run --detach \
        --net host \
        -e DISPLAY=$DISPLAY \
        -e XDG_RUNTIME_DIR=/tmp \
	-e XAUTHORITY=$HOME/.Xauthority \
        --gpus all \
        --shm-size=1g --ulimit memlock=-1 \
        -it \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v $HOME/.Xauthority:/root/.Xauthority:rw \
        -v /home/arc2018:/workspace/arc2018 \
        --hostname centernet \
        --name centernet \
        centernet:0.2
```

Xの転送は諦めることにします。

#### save the image
`demo.py`は画像を表示(imshow)しているからXの転送が必要なのであって、
画像をファイルに保存したら大丈夫だろうということでやってみることにします。

- - -
# Evaluation

[Bechmark Evaluation](https://github.com/xingyizhou/CenterNet/blob/master/readme/GETTING_STARTED.md#benchmark-evaluation)に評価方法が書いてあるので、これをやってみます。

その前にCOCOデータ・セットを取り扱うためのパッケージをインストールしておきます。
```bash
(CenterNet) root@centernet:~/CenterNet/src# conda install -c conda-forge pycocotools
```

そして、COCOデータ・セットを所定の場所に展開しておきます。
```bash
(CenterNet) root@centernet:~# cd CenterNet/data/
(CenterNet) root@centernet:~/CenterNet/data# ls
(CenterNet) root@centernet:~/CenterNet/data# mkdir coco
(CenterNet) root@centernet:~/CenterNet/data# cd coco/
(CenterNet) root@centernet:~/CenterNet/data/coco# unzip /workspace/coco/annotations_trainval2017.zip
(CenterNet) root@centernet:~/CenterNet/data/coco# unzip /workspace/coco/val2017.zip
```

それでは評価をしてみます。
今回はGPU１つのPCで実行していますので、`CUDA_VISIBLE_DEVICES`は不要なのですが、
複数のGPUを搭載したPCで特定のGPUでのみ実行したい場合は、`CUDA_VISIBLE_DEVICES`で
使用したいGPU-IDを指定すると良いです。
```bash
(CenterNet) root@centernet:~/CenterNet/src# export CUDA_VISIBLE_DEVICES=0
(CenterNet) root@centernet:~/CenterNet/src# python test.py ctdet --exp_id coco_dla --keep_res --load_model ../models/ctdet_coco_dla_2x.pth
```

結果は以下のようになり、[Model ZOO](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md#model-zoo)
にある結果と一致したので、動作は大丈夫そうです。
```bash
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.374
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.551
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.408
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.206
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.420
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.506
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.317
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.521
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.551
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.336
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.594
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.737
```

```bash
(CenterNet) root@centernet:~/CenterNet/src# python test.py ctdet --exp_id coco_hg --arch hourglass --fix_res --load_model ../models/ctdet_coco_hg.pth
```
```bash
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.392
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.576
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.424
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.201
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.419
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.556
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.325
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.514
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.536
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.325
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.573
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.715
```

- - -
# Training

Training 用のデータは、`data/arc/{annotations,train,val}` に置きます。

hourgralss での Training では ExtremeNet のモデル(ExtremeNet_500000)をバックボーンに使用するため、
ダウンロードが必要です。
ダウンロードは[ここ](https://github.com/xingyizhou/ExtremeNet)からです。

ダウンロードしたモデルは `*.pkl` 形式となっており、`*.pth`形式に変換したいため、
[このツール](https://github.com/xingyizhou/CenterNet/blob/master/src/tools/convert_hourglass_weight.py)
を使って変換します。このスクリプトはGPUを使用するようです。

用意されている training 用スクリプト(`experiments/ctdet_coco_hg.sh`)を利用して、GPUx1の環境に合わせます。
具体的には、`--gpus` の指定を1つだけにすることと、
`batch_size` をそのGPU数分へ変更するだけです。

```bash
(CenterNet) root@centernet:~/centernet/CenterNet.org/src# python main.py arc --dataset arc --exp_id arc_hg --arch hourglass --batch_size 2 --master_batch 4 --lr 2.5e-4 --load_model ../models/ExtremeNet_500000.pth --gpus 1
```

- - -
# Test

それでは作成出来たモデルを使って、テストします。

用意されている training 用スクリプト(`experiments/ctdet_coco_hg.sh`)を利用して、GPUx1の環境に合わせます。
また、データセットとして用意したARC2018データセットを指定します。

```bash
# test
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass --gpus 1 --keep_res --resume
# flip test
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass --gpus 1 --keep_res --resume --flip_test
# multi scale test
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass --gpus 1 --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
```

- - -
# Evaluation

MPRG用の評価スクリプトを使用するために、
検出結果をテキストファイルに出力する必要があります。

以下のスクリプトを使用すると、current directory に
`ファイル名.png`,`ファイル名.txt`を出力します。
* `ファイル名.png`は、検出したBoundingBoxを元画像に描画したものです
* `ファイル名.txt`は、検出したBoundingBox情報を以下の形式(space区切り)で出力したものです
	- ItemID Confidence x_min y_min x_max y_max 
	- ItemIDはアイテムのカテゴリIDです
	- Confidenceはその確信度
	- (x_min, y_min)は左上の座標[pixel]
	- (x_max, y_max)は右下の座標[pixel]

```bash
$ python demo.py arc \
	--arch hourglass \
	--demo ../data/arc/val/hogehoge.png \
	--load_model ../exp/arc/arc_hg/model_last.pth
```


