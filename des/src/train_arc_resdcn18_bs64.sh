#python main.py ctdet --exp_id coco_resdcn18 --arch resdcn_18 --batch_size 114 --master_batch 18 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16
export CUDA_VISIBLE_DEVICES=0,1,2,3
python main.py arc --dataset arc --exp_id arc_resdcn18_bs64 --arch resdcn_18 --batch_size 64 --master_batch 18 --lr 5e-4 --gpus 0,1,2,3 --num_workers 16
