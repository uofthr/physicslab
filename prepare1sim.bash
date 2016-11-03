#!/bin/bash
cd $HOME
mkdir run1sim
cd run1sim
curl -Lk https://github.com/hannorein/rebound/archive/fast_simulation_restarter.zip --output rebound.zip
unzip rebound.zip
cd rebound-fast_simulation_restarter/problems/2hour
curl -Lk https://github.com/uofthr/physicslab/blob/master/restart_0051.bin?raw=true --output restart_0051.bin
make
