#!/bin/bash

./fast-downward.py $1 $2 --search 'lazy_greedy([cg(),const(infinity)])' > /dev/null
python check_graph.py causal_graph.dot
