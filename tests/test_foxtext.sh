#/usr/bin/sh
echo "thalab-console.py -c -f samples/10.txt >output/10.txt"
python -m cProfile ../thalab-console.py -c -f samples/10.txt >output/10.txt


