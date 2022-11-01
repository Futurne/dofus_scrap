#! /bin/sh
for file in "$1"/*.json ; do
    jq < "$file"> temp.json
    mv temp.json "$file"
done
