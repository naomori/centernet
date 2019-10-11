#!/bin/sh
docker run --detach \
        --gpus all \
        --shm-size=1g --ulimit memlock=-1 \
        -it \
        -v /home/arc2018:/workspace/arc2018 \
        --hostname centernet \
        --name centernet \
        centernet:0.2

