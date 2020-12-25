#/usr/bin/sh
python -m cProfile ../bin/thalab-console.py -c -f samples/phrases.txt >output/phrases.txt
cp output/phrases.txt output/phrases/1.txt
