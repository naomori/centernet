# test
python test.py arc --dataset arc --exp_id arc_resdcn18_bs64 --arch resdcn_18 --keep_res --resume
# flip test
python test.py arc --dataset arc --exp_id arc_resdcn18_bs64 --arch resdcn_18 --keep_res --resume --flip_test
# multi scale test
python test.py arc --dataset arc --exp_id arc_resdcn18_bs64 --arch resdcn_18 --keep_res --resume --flip_test --test_scales 0.5,0.75,1,1.25,1.5
