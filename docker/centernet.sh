#!/bin/sh
docker run --detach \
  -p 8888:8888 \
  -p 6006:6006 \
  -p 2222:22 \
  --privileged \
  --gpus all \
  --shm-size=1g --ulimit memlock=-1 \
  -it \
  -v /home/arc2018:/workspace/arc2018 \
  --hostname centernet \
  --name centernet \
  centernet:3.0
