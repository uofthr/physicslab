#!/bin/bash
gmetric --name="num_users" --type=int32 --value=`who | wc -l`
