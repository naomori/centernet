#!/bin/bash

# [NOTE]
# You can't give any arguments to a job script,
# you should use an unique job script's filename.
# Because HPC uses the job script's filename as the identifier(job name).
# Or, you can specify a job name with `-N` option of qsub command.
# Using it, you can use the same job script file.
# So, specify the job name with `-N` option, please.

#$ -N <job_name>
#$ -l rt_F=1
#$ -l h_rt=72:00:00
#$ -j y
#$ -cwd

# arch: hourglass, dla_34, resdcn_101, or resdcn_18
arch='hourglass'
exp_id='arc_hg_bs10'
batch_size=10
num_epochs=140

source /etc/profile.d/modules.sh
module load cuda/10.1/10.1.243 cudnn/7.6/7.6.4 nccl/2.4/2.4.8-1
/bin/bash ./train_and_test.sh $arch $exp_id $batch_size $num_epochs
