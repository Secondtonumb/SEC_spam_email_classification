#!/bin/bash

train_trim_files=$(cat train_trim_index.txt)
# test_trim_files=$(cat test_file_index.txt)
invalid_train_files=''

for f in $train_trim_files
do
if [ ! -f $f ];then
    echo ${f}
    invalid_train_files="${invalid_train_files} ${f}"
fi
done 

echo ${invalid_train_files} > invalid_train_files
# for f in $test_trim_files
# do
#     gsed -i "s/\r//g" ${f}
# done





