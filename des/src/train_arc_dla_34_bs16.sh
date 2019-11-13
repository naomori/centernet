# python main.py arc --dataset arc --exp_id arc_dla_34 --batch_size 128 --master_batch 9 --lr 5e-4 --gpus 0,1,2,3,4,5,6,7 --num_workers 16 --num_epochs 230 lr_step 180,210
# python main.py arc --dataset arc --exp_id arc_dla_34 --batch_size 16 --master_batch 9 --lr 5e-4 --gpus 0 --num_workers 6 --num_epochs 230 --lr_step 180,210
export CUDA_VISIBLE_DEVICES=0,1,2,3
#python main.py arc --dataset arc --exp_id arc_dla_34 --batch_size 16 --master_batch 9 --lr 5e-4 --gpus 0,1,2,3 --num_workers 6 --num_epochs 920 --lr_step 180,210
python main.py arc --dataset arc --exp_id arc_dla_34_bs16 --batch_size 16 --master_batch 9 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16 --num_epochs 230 --lr_step 180,210
