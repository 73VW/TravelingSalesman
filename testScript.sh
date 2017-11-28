#!/bin/sh

rm *0.log

for j in 010 020 050 100 200
do
    for i in {1..10}
    do
        { time python CostaPedretti.py --filename data/pb$j.txt --nogui 1>> time$j.log; } 2>&1 | grep real >> time$j.log
    done
done
