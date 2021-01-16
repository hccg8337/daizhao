#!/bin/sh

set -e

for name in $(docker ps -a -q -f name=daizhao)
do
  docker rm -f "$name"
done
docker run -d -v /home/ec2-user/daizhao:/code --net host --env DJANGO_SETTINGS_MODULE=daizhao.settings --name daizhao_service --restart always --privileged=true daizhao service