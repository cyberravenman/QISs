#!/bin/bash

echo '  ______   ______   ______               '   
echo ' /      \ |      \ /      \              '   
echo ' |  $$$$$$\ \$$$$$$|  $$$$$$\  _______   '    
echo ' | $$  | $$  | $$  | $$___\$$ /       \  '    
echo ' | $$  | $$  | $$   \$$    \ |  $$$$$$$  '    
echo ' | $$ _| $$  | $$   _\$$$$$$\ \$$    \   '    
echo ' | $$/ \ $$ _| $$_ |  \__| $$ _\$$$$$$\  '    
echo '  \$$ $$ $$|   $$ \ \$$    $$|       $$  '    
echo '   \$$$$$$\ \$$$$$$  \$$$$$$  \$$$$$$$   '    
echo '       \$$$                              '
echo '                           launcher v.0.1'

if [ -d "$PWD/.QISs_v.0.1-venv" ]; then
	echo '[+]: Activate Python virtual env'
	source $PWD/.QISs_v.0.1-venv/bin/activate &>-
else
	echo '[+]: Install Python virtual env'
	pip3 install virtualenv --break-system-packages &>-
	echo '[+]: Init Python virtual env'
	virtualenv .QISs_v.0.1-venv &>-
	source $PWD/.QISs_v.0.1-venv/bin/activate &>-
	echo '[+]: Install module "IPython"'
	pip3 install IPython &>-
	echo '[+]: Install module "PyQt5"'
	pip3 install PyQt5 &>-
	echo '[+]: Install module "qiskit"'
	pip3 install qiskit &>-
	echo '[+]: Install module "qiskit-ibm-runtime"'
	pip3 install qiskit-ibm-runtime &>-
	echo '[+]: Install module "tabulate"'
	pip3 install tabulate &>-
	echo '[+]: Install module "debugpy"'
	pip3 install debugpy &>-
fi
rm -rf -
echo '[+]: Start Software! Good luck!'
python3 QIS_Benchmark_v.0.1.py
