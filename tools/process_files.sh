function get_diacritics {
    # change the path to mishkal-console.py according to your system 
    mishkal_py="../bin/mishkal-console.py"
    input_file=${1}
    output_dir=${2}
    out_name=$(basename ${input_file})
    printf "processing %s\n" ${input_file}
    py -2.7 ${mishkal_py} -f ${input_file} | grep '^ ' > ${output_dir}/${out_name} || pause
}

# change pathes according to your system 
oov_files="../input/lines_*.txt"
out_dir="../output"

for oov_file in ${oov_files}
do
    get_diacritics ${oov_file} ${out_dir}
done

printf "done\n"
