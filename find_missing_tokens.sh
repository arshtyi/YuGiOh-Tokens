if [ -d "new" ]; then
    rm -rf new/*
else
    mkdir -p new
fi
> new.txt
for file in ref/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        id="${filename%.*}"
        if ! grep -q "\"$id\":" token.json; then
            echo "$id"
            echo "$id" >> new.txt
            cp "$file" "new/$filename"
        fi
    fi
done

count_le8=0
count_gt8=0

if [ -f new.txt ]; then
    while IFS= read -r id || [ -n "$id" ]; do
        id=${id%$'\r'}
        if [ ${#id} -le 8 ]; then
            ((count_le8++))
        else
            ((count_gt8++))
        fi
    done < new.txt
fi
echo ""
echo "统计结果："
echo "正式发售但还未收录 (ID长度<=8): $count_le8"
echo "暂未发售 (ID长度>8): $count_gt8"
