#!/bin/bash
docker pull vahev/pyroute:lts
docker run --name pyroute --net=host -e DISPLAY -v /tmp/.X11-unix -t -d vahev/pyroute:lts
touch magic-cookie
xauth list > magic-cookie
docker start pyroute
docker cp ./magic-cookie pyroute:/root/pyroute
rm magic-cookie
docker exec -ti pyroute bash

