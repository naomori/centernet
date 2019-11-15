#!/bin/bash

# $1: arch: hourglass, dla_34, resdcn_101, resdcn_18
# $2: exp_id
# $3: batch size
# #4: num_epochs

echo "source ~/.bash_profile"
source ~/.bash_profile
echo "source ~/.bashrc"
source ~/.bashrc
echo "module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1"
module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
echo "pyenv global miniconda3-4.3.30"
pyenv global miniconda3-4.3.30
echo "conda activate centernet"
conda activate centernet
echo "cd /home/acb11394zl/centernet/CenterNet.org/src"
cd /home/acb11394zl/centernet/CenterNet.org/src
echo "export PYTHONPATH"
export PYTHONPATH=$PYTHONPATH:/home/acb11394zl/.pyenv/versions/miniconda3-4.3.30/envs/centernet/lib/python3.6/site-packages
echo "train_arc_gpu4.sh"
./train_arc_gpu4.sh $1 $2 $3 $4
echo "./test_arc_gpu4.sh"
./test_arc_gpu4.sh $1 $2
