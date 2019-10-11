import os
import sys

import glob
from natsort import natsorted

from bboxes import BoundingBoxes

class Annotations:
    def __init__(self, bboxes_dir):
        annos = []
        for bboxes_filename in natsorted(glob.glob(bboxes_dir + '/*.txt')):
            anno = Annotation(bboxes_filename)
            annos.append(anno)
        self.item = { 'annotations' : annos }

    def get_obj(self):
        return self.item

    def get_json(self):
        annos_list = []
        for anno in self.item['annotations']:
            annos_list.extend(anno.get_json())
        return { 'annotations' : annos_list }

    def expand_for_json(self, image_id, png_filename):
        for anno in self.item['annotations']:
            if not anno.cmp_filename(png_filename):
                continue
            anno.expand_for_json(image_id)
            return

    def show(self):
        print(self.item.keys())
        for anno in self.item["annotations"]:
            anno.show()

    def show_json(self):
        for anno in self.item["annotations"]:
            anno.show_json()

class Annotation:
    id = 0
    def __init__(self, bboxes_filename):
        Annotation.id += 1
        bboxes = BoundingBoxes(bboxes_filename)
        df_bboxes = bboxes.fetch_df()
        iscrowd = 1 if len(df_bboxes) > 1 else 0
        keys = ['start_id', 'file_name', 'iscrowd', 'bboxes']
        values = [Annotation.id, os.path.basename(bboxes_filename),
                  iscrowd, df_bboxes]
        self.item = dict(zip(keys,values))
        self.json = []
        Annotation.id += (len(df_bboxes) - 1)

    def expand_for_json(self, image_id):
        start_id = self.item['start_id']
        df_bboxes = self.item['bboxes']
        for df_bbox in df_bboxes.itertuples():
            entry = {}
            entry['id'] = start_id
            entry['image_id'] = image_id
            entry['iscrowd'] = self.item['iscrowd']
            entry['category_id'] = df_bbox.Index
            entry['bbox'] = [ df_bbox.center_x_pixel, df_bbox.center_y_pixel,
                              df_bbox.width_pixel, df_bbox.height_pixel ]
            self.json.append(entry)
            start_id += 1
        return self.json

    def cmp_filename(self, filename):
        if os.path.splitext(filename)[0] == \
           os.path.splitext(self.item['file_name'])[0]:
            return True
        else:
            return False

    def get_obj(self):
        return self.item

    def get_json(self):
        return self.json

    def show(self):
        print(self.item)

    def show_json(self):
        print(self.json)

if __name__ == "__main__":
    args = sys.argv
    bboxes_dir = args[1]

    annos = Annotations(bboxes_dir)
    annos.show()
