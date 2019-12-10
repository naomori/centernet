# MPRG ARC2018 Dataset

## The Goal
[MPRG][]が提供してくれている[MPRG-ARC2017用のデータセット][MPRG-datasets]を使って
[CenterNet][]をTrainingし、Valiadtionすることを目的とします。
Validationには[MPRG][]が提供してくれている[評価用ソフトウェア][MPRG-evaluate]を使用します。

- - -

## Datasets
[CenterNet][]では、[COCO][],[PASCAL VOC][]を使った評価結果で優位性を主張しています。
したがって、[MPRG-ARC2017用のデータセット][]をどちらかのデータセット形式に変換し、
Training&Validationに使用することにします。

## COCO
今回は[COCO][]を利用することにします。
[COCO][]データセットの説明については、[こちら](https://www.pynote.info/entry/mscoco)が分かりやすいです。
作成した `mprg2coco` を使用して、[MPRG-ARC2017用のデータセット][MPRG-datasets]を表現する
訓練用COCO形式ファイル`train_arc.json`, 評価用COCO形式ファイル`val_arc`を作成しておきます。

- - -

## ARCデータセットの実装
COCO,PascalVOCのデータセットを取り扱う実装は`src/lib/datasets`にあります。
`arc.py`ファイルをCOCO,PascalVOCと同様に実装し、以下のディレクトリに置き、
`dataset_factory.py`に実装したクラスを登録します。
```git
A       src/lib/datasets/dataset/arc.py
A       src/lib/datasets/sample/arc.py
M       src/lib/datasets/dataset_factory.py
```

## ARC用訓練実装
COCO,PascalVOCのデータセットの推論実装は`src/lib/trains`にあります。
`arc.py`ファイルをCOCO,PascalVOCと同様に実装し、以下のディレクトリに置き、
`train_factory.py`に実装したクラスを登録します。
```git
A       src/lib/trains/arc.py
M       src/lib/trains/train_factory.py
```
あと decode 処理も必要そうなので追加しておきます。
ただし、中身は `ctdet` と全く同じです。
データセットと対象とする問題はリンクしているため、
coco だと ctdet(物体検知?) みたいになっているのですが、
今回 ARC 用のデータセットを用意したので、別途実装を追加しないといけなくなってしまいました。

```git
M       src/lib/models/decode.py
```

## ARC用推論実装
COCO,PascalVOCのデータセットの推論実装は`src/lib/detectors`にあります。
`arc.py`ファイルをCOCO,PascalVOCと同様に実装し、以下のディレクトリに置き、
`detector_factory.py`に実装したクラスを登録します。
`base_detector.py`の変更は、`arc.py`の出力に必要な情報を設定するためです。
```git
A       src/lib/detectors/arc.py
M       src/lib/detectors/base_detector.py
M       src/lib/detectors/detector_factory.py
```

また、推論した結果を表示するための実装は`src/lib/utils`にあります。
ここで、ARCデータセット用のクラス名の登録や、推論した画像の保存などの処理を登録します。
今回は、リモートのPCのDocker Containerで Training/Validation/Evaluation をするため、
手元のPCで画像を表示させながら処理するのは難しい状況にあります。
したがって、画像を表示させるのではなくファイルに保存して後から見れるようにしておきます。
```git
M       src/lib/utils/debugger.py
M       src/lib/utils/post_process.py
```

## ARC用オプション追加
どのデータセットを使うのかを指定するための実装は`src/lib/opts.py`です。
```git
M       src/lib/opts.py
```
このファイルにARC用のオプションを追加しておきます。
また、データセットの mean, std を内部に含んでいますので、
事前にそれらを計算しておきます。
それらは`mprg2coco/mean_std.ipynb`で計算できます。
train,valid の両方の画像を合わせて計算しておきます。

## DCNv2
[CenterNet][]を PyTorch 1.1 で動作させるための対応内容が
[ここ](https://github.com/xingyizhou/CenterNet/issues/7)で紹介されています。
DCNv2 については、original のものを持ってきた上で修正が必要みたいです。

- - -
# ARCデータセットによる訓練の実行
データセットを以下のように置きます。
```bash
data/arc
|-- annotations: COCO形式ファイル
|   |-- train_arc.json  : 訓練用
|   `-- val_arc.json    : 評価用
|-- train: 訓練用画像
|   `-- *.png           : PNG image data, 1280 x 960, 8-bit/color RGB, non-interlaced
`-- val: 評価用画像
    `-- *.png           : PNG image data, 1280 x 960, 8-bit/color RGB, non-interlaced
```

その上で以下を実行します。
```bash
python main.py arc --dataset arc \
  --exp_id arc_hg --arch hourglass \
  --batch_size 4 --master_batch 4 \
  --lr 2.5e-4 --num_epochs 560 \
  --load_model ../models/ExtremeNet_500000.pth --gpus 1
```

CenterNetの著者は、以下のように GPUx5 の環境で訓練を実施したようですが、
GPUx1 の環境しかないため、batch_size を減らした上で実施しています。
```bash
python main.py arc \
  --exp_id arc_hg --arch hourglass \
  --batch_size 24 --master_batch 4 \
  --lr 2.5e-4 \
  --load_model ../models/ExtremeNet_500000.pth --gpus 0,1,2,3,4
```

# ARCデータセットによるテストの実行
以下を実行します。

テストのモデルとして`model_last.pth`を使用います。
model_best や他の epoch のモデルもあったのですが、
model_last が一番精度が出るみたいです(epochs=140程度だと)。
epochs を増加させて Training したモデルであれば、適切なものは異なるのかもしれません。

```bash
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass \
  --gpus 1 --num_workers 4 --keep_res --resume \
  --load_model ../exp/arc/arc_hg/model_last.pth 
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass \
  --gpus 1 --num_workers 4 --keep_res --resume --flip_test \
  --load_model ../exp/arc/arc_hg/model_last.pth 
python test.py arc --dataset arc --exp_id arc_hg --arch hourglass \
  --gpus 1 --num_workers 4 --keep_res --resume --flip_test \
  --test_scales 0.5,0.75,1,1.25,1.5 \
  --load_model ../exp/arc/arc_hg/model_last.pth 
```

著者実装では以下のようにテストを実施しています。
```bash
# test
python test.py ctdet --exp_id coco_hg --arch hourglass --keep_res --resume
# flip test
python test.py ctdet --exp_id coco_hg --arch hourglass --keep_res --resume --flip_test 
# multi scale test
python test.py ctdet --exp_id coco_hg --arch hourglass --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
```

# ARCデータセットに対する推論結果の取得
以下のような python スクリプトを全ての評価画像に対して実行して、
推論した BoundingBox を描画した画像ファイルと、
その BoundingBox を記録したテキストファイルを出力します。

```python
model = f'{exp_dir}/model_last.pth'
py_exe = 'python ./demo.py'
arch = 'hourglass'

def demo(png_path):
    python_script = f"{py_exe} arc --arch {arch} " \
                    f"--demo {png_path} --load_model {model}"
    subprocess.run(shlex.split(python_script))
```

全体のスクリプトは、`demo_arc_{hg,dla_34}.py`として用意しています。

- - -
# ARCデータセット評価用スクリプトの実行
[MPRG][]が評価用スクリプトを用意してくれているので、以下のように実行します。
* `-i`: 評価用画像の置き場所。このディレクトリ直下に画像ファイル`*.png` が置いてある
* `-t`: Ground-Truth の置き場所。このディレクトリ直下に真値データ`*.txt`が置いてある
* `-r`: 推論結果(BoundingBoxのテキスト)の置き場所。このディレクトリ直下に推論BoundingBox`*.txt`が置いてある

```bash
python detect_evaluation.py \
  -i /home/arc2018/datasets/ARCdataset_png/test_known/rgb/ \
  -t /home/arc2018/datasets/ARCdataset_png/test_known/boundingbox/ \
  -r ~/github/centernet/CenterNet.org/exp/arc/arc_hg/demo/
```

評価用スクリプトの実行が完了すると、
`-r`で指定したディレクトリ配下に`eval`ディレクトリが作成されており、
confusion matrixの画像(confusion_matrix.{pdf,png})と、
Matching-Rate, Miss-Rate, Mean IoU が書かれたテキストファイル(totalresult.txt)が置かれています。

推論結果は、x座標は`[0,1280]`, y座標は`[0,960]`に clip されています。

- - -
[MPRG]: http://mprg.jp/research/arc_dataset_2017_j
[MPRG-datasets]: http://www.mprg.cs.chubu.ac.jp/ARC2017/ARCdataset_png.zip
[MPRG-evaluate]: https://github.com/machine-perception-robotics-group/MC2ARCdataset_evaluate
[CenterNet]: https://github.com/xingyizhou/CenterNet
[COCO]: http://cocodataset.org/#home
[PASCAL VOC]: http://host.robots.ox.ac.uk/pascal/VOC/
