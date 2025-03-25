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
echo '                        launcher v.0.3.10'
echo 'Che_Guevara_22 -_-     CyberRavenMan  *_*'

if [[ $1 == "del_venv" ]]; then
	rm -rf $PWD/QISs_v.0.3.10-venv
	printf '\n[+]: Virtual environment has been deleted.\n\n'
	exit
else
	printf '\n[!]: If You need to delete the old virtual environment, then run "./run del_venv"\n\n'
fi

if [ -d "$PWD/QISs_v.0.3.10-venv" ]; then
	echo '[*]: Activate Python virtual env..'
	source $PWD/QISs_v.0.3.10-venv/bin/activate &>-
	echo '[+]: Done'
else
	echo '[*]: Updating..'
	sudo apt update
	echo '[+]: Done'
	
	echo '[*]: Install python3'
	sudo apt-get install python3
	echo '[+]: Done'
	
	echo '[*]: Install pip..'
	sudo apt install python3-pip
	echo '[+]: Done'
	
	echo '[*]: Install Python virtual env..'
	python3 -m pip install --user virtualenv --break-system-packages
	sudo apt install python3-venv
	echo '[+]: Done'
	
	echo '[*]: Creating venv <quant>..'
	python3 -m venv QISs_v.0.3.10-venv
	echo '[+]: Done'
	
	echo '[*]: Activating venv <quant>..'
	source $PWD/QISs_v.0.3.10-venv/bin/activate
	echo '[+]: Done'
	
	echo '[*]: Upgrade pip..'
	pip install --upgrade pip
	echo '[+]: Done'
	
	echo '[*]: Install PyQt5..'
	sudo apt install python3-pyqt5
	echo '[+]: Done'
	
	echo '[*]: Install PyQt5..'
	pip install PyQt5
	echo '[+]: Done'
	
	echo '[*]: Install module "IPython"..'
	pip3 install IPython
	echo '[+]: Done'
	
	echo '[*]: Install module "qiskit"..'
	pip3 install qiskit
	echo '[+]: Done'
	
	echo '[*]: Install module "qiskit-ibm-runtime"..'
	pip3 install qiskit-ibm-runtime
	echo '[+]: Done'
	
	echo '[*]: Install "qiskit[visualization]..'
	pip3 install qiskit[visualization]
	echo '[+]: Done'
	
	echo '[*]: Install module "tabulate"..'
	pip3 install tabulate
	echo '[+]: Done'
	
	echo '[*]: Install module "matplotlib"..'
	pip3 install matplotlib
	echo '[+]: Done'

	echo '[*]: Install module "pandas"..'
	pip3 install pandas
	echo '[+]: Done'
	
	echo '[*]: Install StatsModels..'
	pip install statsmodels
	echo '[+]: Done'
	
	echo '[*]: Install pytest..'
	pip install pytest
	echo '[+]: Done'
	
	echo '[*]: Install scikit-learn..'
	pip install scikit-learn
	echo '[+]: Done'
	
	echo '[*]: Install xlrd xlwt openpyxl..'
	pip install xlrd xlwt openpyxl
	echo '[+]: Done'
fi
rm -rf -
printf '\n[+]: Start Software! Good luck!\n\n'
python3 QIS_Benchmark_v.0.3.10.py
