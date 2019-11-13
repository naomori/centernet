#!/bin/bash

#$ -l rt_F=1
#$ -l h_rt=72:00:00
#$ -j y
#$ -cwd

source /etc/profile.d/modules.sh
module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
/bin/bash ./train_and_test_dla34_bs4.sh
