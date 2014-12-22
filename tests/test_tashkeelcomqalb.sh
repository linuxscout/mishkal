python -m cProfile ../mishkal-console.py -c -l 500 -f samples/vocalized/qalbvoca.txt >output/compare/qalb.txt
DATE=`date +%Y-%m-%d-%H:%M`
echo "make archive" 
cp output/compare/qalb.txt  output/compare/Q${DATE}.txt
