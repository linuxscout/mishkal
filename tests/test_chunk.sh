#/usr/bin/sh
#DATA_FILE=vocalized/text.txt
DATA_FILE=samples/vocalized/rndlines.txt
#DATA_FILE=txt
echo "extractchunks.py -f samples/${DATA_FILE} >output/chunks/${DATA_FILE}"
python extractchunks.py -f samples/${DATA_FILE} >output/chunks/${DATA_FILE}

sort output/chunks/${DATA_FILE} |uniq -c | sort -n -r > output/chunks/${DATA_FILE}.srt
