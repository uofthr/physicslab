#!/bin/bash
sudo /usr/local/bin/gmetric --name="num_users" --type=int32 --value=`who | wc -l`
