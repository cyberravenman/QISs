#!/bin/bash

pip3 install virtualenv --break-system-packages &>-
virtualenv QISs-venv &>-
source $PWD/QISs-venv/bin/activate &>-
pip3 install IPython PyQt5 qiskit qiskit-ibm-runtime tabulate &>-
rm -rf -
python3 ./QIS_Benchmark_v.0.3.py
