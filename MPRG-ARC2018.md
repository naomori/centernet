# MPRG ARC2018 Dataset

## The Goal
[MPRG][]が提供してくれている[MPRG-ARC2017用のデータセット][MPRG-datasets]を使って
[CenterNet][]をTrainingし、Valiadtionすることを目的とします。
Validationには[MPRG][]が提供してくれている[評価用ソフトウェア][MPRG-evaluate]を使用します。

## Datasets
[CenterNet][]では、[COCO][],[PASCOL VOC][]を使った評価結果で優位性を主張しています。
したがって、[MPRG-ARC2017用のデータセット][]をどちらかのデータセット形式に変換し、
Training&Validationに使用することにします。


- - -
[MPRG]: http://mprg.jp/research/arc_dataset_2017_j
[MPRG-datasets]: http://www.mprg.cs.chubu.ac.jp/ARC2017/ARCdataset_png.zip
[MPRG-evaluate]: https://github.com/machine-perception-robotics-group/MC2ARCdataset_evaluate
[CenterNet]: https://github.com/xingyizhou/CenterNet
[COCO]: http://cocodataset.org/#home
[PASCAL VOC]: http://host.robots.ox.ac.uk/pascal/VOC/
