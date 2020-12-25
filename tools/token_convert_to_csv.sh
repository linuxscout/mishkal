# convert wordlist vocalized with statistics
# to csv and unvocalized, vocalized, stats
# strip vowels from the first field
#cat $1 | awk '{ x=$2; gsub(/[ًٌٍَُِّْ]/, "",x); print x "\t"$2"\t"$1}' | sort > "$1.csv"

cat $1 | awk '{ x=$2; gsub(/[ًٌٍَُِّْ]/, "",x); print "u\'"x"\':u\'"$2"',#\t"$1}' | sort > "$1.csv"
