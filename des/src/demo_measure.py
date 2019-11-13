from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import cv2

from opts import opts
from detectors.detector_factory import detector_factory

image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']

def demo(opt):
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
  opt.debug = max(opt.debug, 0)
  Detector = detector_factory[opt.task]
  detector = Detector(opt)

  if opt.demo == 'webcam' or \
    opt.demo[opt.demo.rfind('.') + 1:].lower() in video_ext:
    cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
    detector.pause = False
    while True:
        _, img = cam.read()
        cv2.imshow('input', img)
        ret = detector.run(img)
        time_str = ''
        for stat in time_stats:
          time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
        print(time_str)
        if cv2.waitKey(1) == 27:
            return  # esc to quit
  else:
    if os.path.isdir(opt.demo):
      image_names = []
      ls = os.listdir(opt.demo)
      for file_name in sorted(ls):
          ext = file_name[file_name.rfind('.') + 1:].lower()
          if ext in image_ext:
              image_names.append(os.path.join(opt.demo, file_name))
    else:
      image_names = [opt.demo]

    time_sum = dict.fromkeys(time_stats, 0)

    for (image_name) in image_names:
      ret = detector.run(image_name)
      time_str = ''
      for stat in time_stats:
        time_sum[stat] += ret[stat]
        time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
      print(time_str)

    tot = time_sum['tot']
    proc = time_sum['pre'] + time_sum['net'] + time_sum['dec'] + time_sum['post']
    net = time_sum['net']
    tot_fps = len(image_names) / tot
    proc_fps = len(image_names) / proc
    net_fps = len(image_names) / net
    time_sum_str = f'tot: {tot_fps}[fps], '
    time_sum_str += f'proc: {proc_fps}[fps], '
    time_sum_str += f'net: {net_fps}[fps]'
    print(time_sum_str)

if __name__ == '__main__':
  opt = opts().init()
  demo(opt)
