#/usr/bin/sh
python -m cProfile ../thalab-console.py -c -f samples/phrases.txt >output/phrases.txt
cp output/phrases.txt output/phrases/1.txt
