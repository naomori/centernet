import os
import sys
import glob

import shlex
import subprocess
import shutil

from multiprocessing import Pool
import multiprocessing as multi

py_exe = 'python ./detect_evaluation.py'

args = sys.argv
result_dir=args[1]

def detect_script(result_path):
    python_script = f"{py_exe} " \
                    f"-i ../CenterNet.org/data/arc/val/ " \
                    f"-t ../CenterNet.org/data/arc/boundingbox/ " \
                    f"-r {result_path}/"
    subprocess.run(shlex.split(python_script))

p = Pool(4)
p.map(detect_script, glob.glob(f'../CenterNet.org/results/{result_dir}'))
p.close()
