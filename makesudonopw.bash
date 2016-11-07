#!/bin/bash
for i in `seq -f "%02g"  1 44`; do
    ssh -t research@physics-lab${i}.utsc-labs.utoronto.ca "sudo sh -c 'echo \"%wheel ALL=(ALL) NOPASSWD: ALL\" >> /etc/sudoers'"
done
