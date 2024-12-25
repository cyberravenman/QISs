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
echo '                           launcher v.0.2'
echo 'Che_Guevara_22 -_-     CyberRavenMan  *_*'

if [[ $1 == "del_venv" ]]; then
	rm -rf $PWD/QISs_v.0.2-venv
	printf '\n[+]: Virtual environment has been deleted.\n\n'
	exit
else
	printf '\n[!]: If You need to delete the old virtual environment, then run "./run del_venv"\n\n'
fi

if [ -d "$PWD/QISs_v.0.2-venv" ]; then
	echo '[*]: Activate Python virtual env..'
	source $PWD/QISs_v.0.2-venv/bin/activate &>-
	echo '[+]: Done'
else
	echo '[*]: Install Python virtual env..'
	pip3 install virtualenv --break-system-packages &>-
	echo '[+]: Done'
	
	echo '[*]: Init Python virtual env..'
	virtualenv QISs_v.0.2-venv &>-
	source $PWD/QISs_v.0.2-venv/bin/activate &>-
	echo '[+]: Done'
	
	echo '[*]: Install module "IPython"..'
	pip3 install IPython &>-
	echo '[+]: Done'
	
	echo '[*]: Install module "PyQt5"..'
	pip3 install PyQt5 &>-
	echo '[+]: Done'
	
	echo '[*]: Install module "qiskit"..'
	pip3 install qiskit &>-
	echo '[+]: Done'
	
	echo '[*]: Install module "qiskit-ibm-runtime"..'
	pip3 install qiskit-ibm-runtime &>-
	echo '[+]: Done'
	
	echo '[*]: Install module "tabulate"..'
	pip3 install tabulate &>-
	echo '[+]: Done'

	echo '[*]: Install module "debugpy"..'
	pip3 install debugpy &>-
	echo '[+]: Done'

fi
rm -rf -
printf '\n[+]: Start Software! Good luck!\n\n'
python3 QIS_Benchmark_v.0.2.py
