python -m cProfile ../mishkal-console.py -c -l 500 -f samples/vocalized/rndlines.txt >output/compare/rndlines.11.txt
DATE=`date +%Y-%m-%d-%H:%M`
echo "make archive" 
cp output/compare/rndlines.11.txt  output/compare/L${DATE}.txt
