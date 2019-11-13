export CUDA_VISIBLE_DEVICES=0,1,2,3
# test
python test.py arc --dataset arc --exp_id arc_hg_bs16_epochs_900 --arch hourglass --keep_res --resume
# flip test
python test.py arc --dataset arc --exp_id arc_hg_bs16_epochs_900 --arch hourglass --keep_res --resume --flip_test 
# multi scale test
python test.py arc --dataset arc --exp_id arc_hg_bs16_epochs_900 --arch hourglass --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
