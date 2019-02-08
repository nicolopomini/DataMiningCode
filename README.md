# Data Mining project

Frequent itemset mining in tree-like sequences of complex objects

Usage:
`pip install -r requirements.txt`, to install the needed requirements.

`python src/main.py arguments`, making sure to use a python version at least `3.6`.
Arguments:
- `-out filename` to specify the filename on which the output is written. Default is _output.txt_;
- `-in filename` to specify the filename from which data is read. Default is input.csv;
- `-thr 3` minimum number of times a pattern has to appear to be considered frequent. Default is _4_;
