#!/bin/bash
source ~/.bash_profile
echo "source ~/.bash_profile"
source ~/.bashrc
echo "source ~/.bashrc"
module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
echo "module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1"
pyenv global miniconda3-4.3.30
echo "pyenv global miniconda3-4.3.30"
conda activate centernet
echo "conda activate centernet"
cd /home/acb11394zl/centernet/CenterNet.org/src
echo "cd /home/acb11394zl/centernet/CenterNet.org/src"
export PYTHONPATH=$PYTHONPATH:/home/acb11394zl/.pyenv/versions/miniconda3-4.3.30/envs/centernet/lib/python3.6/site-packages
echo "export PYTHONPATH"
./train_arc_dla_34_bs24.sh
echo "./train_arc_dla_34_bs24.sh"
./test_arc_dla_34_bs24.sh
echo "./test_arc_dla_34_bs24.sh"
