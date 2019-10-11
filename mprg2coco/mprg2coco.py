import os
import sys
import json

from images import ArcImages,ArcImage
from annotations import Annotations,Annotation

def expand_json(images_obj, annos_obj):
    for image in images_obj['images']:
        annos.expand_for_json(image['id'], image['file_name'])

if __name__ == "__main__":
    args = sys.argv
    json_dir = args[1]
    images_dir = args[2]
    bboxes_dir = args[3]
    output_file = args[4]

    output_json = {}
    with open(json_dir + "/info.json", 'r') as f:
        info_json = json.load(f)
        output_json.update(info_json)

    with open(json_dir + "/licenses.json", 'r') as f:
        licencses_json = json.load(f)
        output_json.update(licencses_json)

    with open(json_dir + "/categories.json", 'r') as f:
        categories_json = json.load(f)
        output_json.update(categories_json)

    images = ArcImages(images_dir)
    images_obj = images.get_obj()
    images_str = json.dumps(images_obj)
    images_json = json.loads(images_str)
    output_json.update(images_json)

    annos = Annotations(bboxes_dir)
    annos_obj = annos.get_obj()
    expand_json(images_obj, annos_obj)
    annos_str = json.dumps(annos.get_json())
    annos_json = json.loads(annos_str)
    output_json.update(annos_json)

    with open(output_file, 'w') as f:
        json.dump(output_json, f)
