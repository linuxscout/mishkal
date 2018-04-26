#/usr/bin/sh
DATE=`date +%Y-%m-%d-%H:%M`
echo "thalab-console.py -c -f samples/10.txt >output/10${DATE}.txt"
python -m cProfile ../bin/thalab-console.py -c -f samples/10.txt >output/10-${DATE}.txt


