#!/bin/bash

for i in {1..582}
do
    echo -en "\033[37;1;41m ${i} \033[0m \n"
    link=$(sed -n -e ${i}p links)
    name=${i}_$(sed -n -e ${i}p names)
    if ((${#name} > 150))
    then
        name=${i}
    fi
    (wget http://online.toktom.kg${link}/rus/text/export --output-document=documents/${name}.doc)
done
