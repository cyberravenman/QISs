#! /bin/bash
DATE=$(date '+%Y-%m-%d_%H:%M:%S')
STR_TMP="/Documents/QISs/NIST/ResultTest_"
RESULT_DIR="$HOME$STR_TMP$DATE"
if [ $# -ne 6 ]; then
       echo "Usage: $0 <dirname_dataset> <lenght_afterthoughts> <parametr2> <parametr3> <parametr4> <parametr5>"
       exit
fi

if [ -d $RESULT_DIR ]; then
	echo "Результат тестирования  в папке: '$RESULT_DIR'."
else
	echo "Результат тестирования в папке: '$RESULT_DIR'."
	mkdir -p $RESULT_DIR
	cp -r $1/* $RESULT_DIR/
fi

for filename in $(find $RESULT_DIR -type f)
do
	file=$(basename $filename)
	dirname=$(dirname $filename)
	file=${file%.*}
	echo -e "0\n$filename\n$3\n$4\n$5\n$6\n" | ./NIST/assess $2 >/dev/null
	if [[ $? -eq 1 ]]
       then
	      	echo "Test '$file' successfully completed!"
        else
                echo "Test '$file' stopped working in an emetgency!"
                exit
        fi
	mkdir $dirname/$file
	cp -r $PWD/experiments/AlgorithmTesting $dirname/$file
	rm -rf $filename
done
