#!/bin/sh
docker run --detach \
	-p 8888:8888 \
	-p 6066:6066 \
	-p 2222:22 \
	--privileged \
        --gpus all \
        --shm-size=1g --ulimit memlock=-1 \
        -it \
        -v /home/arc2018:/workspace/arc2018 \
        -v /home/moritan/github/pytorch_advanced:/workspace/pytorch_advanced \
	-v /home/moritan/github/centernet:/workspace/centernet \
        --hostname centernet \
        --name centernet \
        centernet:0.3
