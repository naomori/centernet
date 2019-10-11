import os
import sys

import glob
from natsort import natsorted

import shlex
import subprocess

class ArcImages:
    def __init__(self, dir_name):
        images = []
        for png_file in natsorted(glob.glob(dir_name + '/*.png')):
            image = ArcImage(png_file)
            images.append(image.get_obj())
        self.item = { 'images': images }

    def get_obj(self):
        return self.item

    def show(self):
        print(self.item.keys())
        for image in self.item["images"]:
            image.show()

class ArcImage:
    id = 0
    def __init__(self, filepath):
        ArcImage.id += 1
        self.filepath = filepath
        filename = os.path.basename(filepath)
        width,height,create_date = self.identify(filepath)

        keys = ['id', 'file_name', 'license',
                'width', 'height', 'date_captured']
        values = [ArcImage.id, filename, 1,
                  float(width), float(height), self.create_date(create_date)]
        self.item = dict(zip(keys,values))

    def identify(self, filepath):
        identify_cmd = []
        identify_cmd.append('identify')
        identify_cmd.append('-format')
        identify_cmd.append('"%[png:IHDR.width,height], %[date:create]\\n"')
        identify_cmd.append(filepath)
        identify_str = " ".join(identify_cmd)
        tokens = shlex.split(identify_str)
        res = subprocess.run(tokens, stdout=subprocess.PIPE)
        return str(res.stdout, 'utf-8').strip().split(',')

    def create_date(self, res):
        date_cmd = []
        date_cmd.append('date')
        date_cmd.append('-d')
        date_cmd.append(res)
        date_cmd.append('"+%Y-%m-%d %H:%M:%S"')
        date_str = " ".join(date_cmd)
        tokens = shlex.split(date_str)
        res = subprocess.run(tokens, stdout=subprocess.PIPE)
        return str(res.stdout, 'utf-8').strip()

    def get_obj(self):
        return self.item

    def show(self):
        print(self.item)

if __name__ == "__main__":
    args = sys.argv
    images_dir = args[1]
    images = ArcImages(images_dir)
    images.show()
