# python main.py arc --exp_id arc_hg --arch hourglass --batch_size 24 --master_batch 4 --lr 2.5e-4 --load_model ../models/ExtremeNet_500000.pth --gpus 0,1,2,3,4
export CUDA_VISIBLE_DEVICES=0,1,2,3
python main.py arc --dataset arc --exp_id arc_hg_bs24_epochs_900 --arch hourglass --batch_size 24 --master_batch 4 --lr 2.5e-4 --num_epochs 900 --lr_step=90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600,630,660,690,720,750,780,810,840,870 --load_model ../models/ExtremeNet_500000.pth --gpus 0,1,2,3
# python main.py arc --dataset arc --exp_id arc_hg --arch hourglass --batch_size 4 --master_batch 4 --lr 2.5e-4 --num_epochs 140 --load_model ../models/ExtremeNet_500000.pth --gpus 1
#python main.py arc --dataset arc --exp_id arc_hg --arch hourglass --batch_size 4 --master_batch 4 --lr 2.5e-4 --num_epochs 560 --load_model ../models/ExtremeNet_500000.pth --gpus 1
