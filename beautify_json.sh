for file in $1/*.json ; do
    cat "$file" | jq > temp.json
    mv temp.json "$file"
done
