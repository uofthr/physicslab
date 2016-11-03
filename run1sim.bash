#!/bin/bash
cd $HOME
cd run1sim/rebound-fast_simulation_restarter/problems/
cd 2hour0
nohup ./rebound > /dev/null 2>&1 &
cd 2hour1
nohup ./rebound > /dev/null 2>&1 &
cd 2hour2
nohup ./rebound > /dev/null 2>&1 &
cd 2hour3
nohup ./rebound > /dev/null 2>&1 &

