#!/bin/bash
for i in `seq -f "%02g"  45 45`; do
    ssh -t research@physics-lab${i}.utsc-labs.utoronto.ca "su PLAdmin -c 'sudo dseditgroup -o edit -a research -t user admin &&  sudo dseditgroup -o edit -a research -t user wheel && sudo whoami'"
done
