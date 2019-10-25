from pycocotools.coco import COCO
import numpy as np
import matplotlib.pyplot as plt

# COCO オブジェクトの生成
print("generate COCO object")
ann_path = "train_arc.json"
coco = COCO(ann_path)

# カテゴリIDを取得する
print("fetch category ID")
print(coco.getCatIds(catNms=["Binder", "Balloons"]))

# カテゴリの情報を取得する
print("fetch category info")
cats = coco.loadCats(coco.getCatIds())
print(cats[0])

# 画像IDを取得する
print("fetch image ID")
cat_ids = coco.getCatIds(catNms=['Irish_Spring',
                                'Toilet_Brush',
                                'Mousetraps'])
print(cat_ids)

## cat_ids に含まれるすべてのカテゴリを含む画像を取得する
print(f"fetch images that includes {cat_ids}")
img_ids = coco.getImgIds(catIds=cat_ids)
print(img_ids)

# 画像の情報を取得する
print("fetch image info")
imgs = coco.loadImgs(img_ids)
print([img['file_name'] for img in imgs])

# アノテーションIDを取得する
print("fetch annotation ID")
anno_ids = coco.getAnnIds(imgIds=img_ids)
print(anno_ids)

# アノテーションの情報を取得する
print("fetch annotation info")
annos = coco.loadAnns(anno_ids[0])
from pprint import pprint
pprint(annos)

# アノテーションを可視化する
print("visualize image_id:{}".format(img_ids[0]))
img_id = img_ids[0]

## 指定した画像IDに対応する画像の情報を取得する
print("fetch image info of specialized ID")
img_info, = coco.loadImgs(img_id)
print(img_info)
file_name = img_info['file_name']
validation_dir = '../../datasets/train/rgb'
img_path = f'{validation_dir}/{file_name}'
print(img_path)

## 指定した画像IDに対応するアノテーションIDを取得する
print("fetch annotation ID")
anno_ids = coco.getAnnIds(img_id)
print(anno_ids)

# 指定したアノテーションIDに対応するアノテーションの情報を取得する
print("fetch annotation info")
annos = coco.loadAnns(anno_ids)
print(annos)
coco.showAnns(annos)

# 画像を読み込む
img = plt.imread(img_path)
print(f"load image: {img_path}")

# 画像を描画する
plt.axis('off')
plt.imshow(img)
plt.show()

# アノテーション結果を描画する
# coco.showAnns(annos)
