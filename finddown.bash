#!/bin/bash
for i in `seq -f "%02g"  0 44`; do
    [[ $(ssh -t research@physics-lab${i}.utsc-labs.utoronto.ca "echo 'testecho'" 2>/dev/null)  != *testecho* ]]
    if [ $? -eq 0 ]; then
        echo "research@physics-lab${i}.utsc-labs.utoronto.ca"
    fi
done
