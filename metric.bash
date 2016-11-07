#!/bin/bash
sudo /usr/local/bin/gmetric --name="num_users" --type=int32 --value=`/usr/bin/who | /usr/bin/wc -l | xargs`
