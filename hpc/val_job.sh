#!/bin/bash

# [NOTE]
# You can't give any arguments to a job script,
# you should use an unique job script's filename.
# Because HPC uses the job script's filename as the identifier(job name).
# Or, you can specify a job name with `-N` option of qsub command.
# Using it, you can use the same job script file.
# So, specify the job name with `-N` option, please.

#$ -N val_arc_dla34_95_bs86_epoch920
#$ -l rt_F=1
#$ -l h_rt=4:00:00
#$ -j y
#$ -cwd

# arch: hourglass, dla_34, resdcn_101, or resdcn_18
arch='dla_34'
val_id='val_arc_dla34_95_bs86_epoch920'

source /etc/profile.d/modules.sh
module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1

source ~/.bash_profile
source ~/.bashrc

pyenv global miniconda3-4.3.30
conda activate centernet
export PYTHONPATH=$PYTHONPATH:/home/acb11394zl/.pyenv/versions/miniconda3-4.3.30/envs/centernet/lib/python3.6/site-packages

cd /home/acb11394zl/centernet/CenterNet.org/src

python_bin=python
${python_bin} val_arc.py ${arch} ${val_id}
