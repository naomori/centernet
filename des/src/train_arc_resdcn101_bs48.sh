#python main.py ctdet --exp_id coco_resdcn101 --arch resdcn_101 --batch_size 96 --master_batch 5 --lr 3.75e-4 --gpus 0,1,2,3,4,5,6,7 --num_workers 16
export CUDA_VISIBLE_DEVICES=0,1,2,3
python main.py arc --dataset arc --exp_id arc_resdcn101_bs48 --arch resdcn_101 --batch_size 48 --master_batch 5 --lr 3.75e-4 --gpus 0,1,2,3 --num_workers 16
