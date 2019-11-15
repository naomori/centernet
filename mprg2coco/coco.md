# [Common Objects in Context (COCO)][COCO]

[COCO][] は、大規模な Object Detection, Segmentation, Captioning のための Dataset です。
画像とともに、アノテーション情報を含んでいます。

以下のタスクの学習に利用できます。
* Image Classification
* Object Detection
* Semantic Segmentation
* Instance Segmentation
* Caption Generation
* Pose Estimation

## Download
COCOのデータ・セットには以下のようなものがあります。
以下は、基本的に Object Detection 用のデータ・セットですが、
他に、Segmentation 用のアノテーション情報もあります。
* [トレーニング用画像](http://images.cocodataset.org/zips/train2017.zip)
* [評価用画像](http://images.cocodataset.org/zips/val2017.zip)
  - [トレーニング・評価用アノテーション](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
* [テスト用画像](http://images.cocodataset.org/zips/test2017.zip)
  - [テスト用情報](http://images.cocodataset.org/annotations/image_info_test2017.zip)

## COCO Format
`annotations_trainval2017.zip`ファイルを展開して、
`instances_{train,val}2017.json`を見ると(trainはファイルサイズが大きすぎて見ていない)、
以下のようにアノテーション情報が並んでいます。

フォーマットについては、
[ここ](http://cocodataset.org/#format-data)にあります。

1. "info": object (本ファイルの情報が記載されている)
  * "description": "COCO 2017 Dataset",
  * "url": "http://cocodataset.org",
  * "version": "1.0"
  * "year": 2017
  * "contibutor": "COCO Consortium" 
  * "date_created": "2017/09/01"
2. "licenses": array (ライセンス情報："images"のライセンス情報。idで一意に識別できる)
  * "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
  * "id": 1,
    - ライセンスの識別子(imagesのobjectから"license"で参照される)
  * "name": "Attribution-NonCommercial-ShareAlike License"
3. "images": array (画像ファイルの情報)
  * "license": 4,
    - ライセンス情報
  * "file_name": "000000397133.jpg",
    - ファイル名(ディレクトリを含んでも良い？)
  * "coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
    - option?
  * "height": 427,
    - 高さ pixel
  * "width": 640,
    - 幅   pixel
  * "date_captured": "2013-11-14 17:02:52",
    - 画像キャプチャ時刻
  * "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
  * "id": 397133
    - 画像ファイルの識別子
4. "annotations": array (アノテーション情報)
  * "segmentation": array
    - 一次元配列?
  * "area": 702.1057499999998,
    - 面積?
  * "iscrowd": 0
    - その BoundingBox が含むオブジェクトが単一の場合は`0`, 複数の場合は`1` ? 
    - 今回はすべて単一のはずなので 0 とする
  * "image_id": 289343
    - 画像ファイルのID
  * "bbox": [ 473.07, 395.93, 38.65, 28.67 ]
    - バウンディングボックス `x, y, width, height` のpixel値として並んでいる
    - 注意点は x, y は左上の x_min, y_min であること。中心点ではない。
  * "category_id": 18
    - カテゴリーの識別子
  * "id": 1773
    - アノテーションの識別子
5. "categories": array (物体のカテゴリ種類)
  * "supercategory": "vehicle",
    - カテゴリの親分類
  * "id": 2,
    - カテゴリの識別子
  * "name": "bicycle"
    - カテゴリの名前
    - 同じ `supercategory` に複数の名前が存在することもある
    - e.g. `vehicle` に対して `car`, `motorcycle`, `airplane`, etc.

- - -
# [Team MC^2: ARC2017 RGB-D Dataset][MPRG ARCdataset]
Amazon Robotics Challenge(ARC) は、物流の自動化を目的としたコンペティションです。
ARC では、棚(Storage)や箱(Tote)に陳列されたアイテムの中から
指定されたアイテムをロボットが認識し、ピッキングする問題を扱っています。

MPRGでは、Team MC^2がAmazon Robotics Challenge 2017用に作成したデータセットを公開しています。

Object Detection だけでなく Segmentation 用データや3Dデータも含まれていますが、
Object Detection 用途で2Dの画像とそのバウンディングボックスのデータのみに着目すると以下のような
ディレクトリ・ファイル配置になっています。

* train (訓練用データ)
  + boundingbox
    - `*.txt`
  + rgb
    - `*.png`
* test_known (評価用データ)
  + boundingbox
    - `*.txt`
  + rgb
    - `*.png`

`train`, `test_known` ともに、`boundingbox` と `rgb` 以下のファイル名は
拡張子を除くと同じ名前になっています。

## Bounding Box
Bounding Box の内容は、その画像ファイル(1280x960)に含まれる
アイテムID(1-40)と対応する中心X,Y座標, 幅・高さが記されています。
中心X,Y座標, 幅・高さは`[0-1]`の値に正規化されています。

- - -
# COCO API via python

[こちら][Deep Learing - MS COCO データセットの概要]によると、
`cython`, `pycocotools` をインストールすると、
[MS-COCO API][COCO API] を使用できるとのこと。
[MS-COCO API][COCO API] は、[COCO][]データ・セットのアノテーション情報を
取得できるライブラリ。

アノテーション情報は json ファイルなので、json モジュールで読み込んで取得することもできるけど、
アノテーション情報を含む json ファイルは巨大なため、読み込みに時間がかかります。
ですが、`pycocotools`は`cython`で高速化されているため、処理が早いそうです。

以下のようにインストールできます。
`cython` は `--upgrade` を付けないとインストールできませんでした。

```bash
$ pip install --upgrade cython
$ pip install pycocotools
```

- - -
# MPRG2COCO
[MPRGのデータセット][MPRG ARCdataset]から[COCO][]形式に変換するスクリプトを作成しました。

以下は必要なパッケージなので事前にインストールが必要です。
```bash
$ pip install numpy matplotlib pandas
$ pip install natsort
```

また、スクリプト内部で`identify`を使用しているので、
`ImageMagick`のインストールが必要です。
```bash
$ sudo apt install ImageMagick
```

- - -
[COCO]: http://cocodataset.org/#home
[Deep Learing - MS COCO データセットの概要]: http://pynote.hatenablog.com/entry/mscoco
[MPRG ARCdataset]: http://mprg.jp/research/arc_dataset_2017_j
[COCO API]: https://github.com/cocodataset/cocoapi
