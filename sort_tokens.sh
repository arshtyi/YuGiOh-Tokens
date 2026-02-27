# 检查 jq 是否安装
if ! command -v jq &> /dev/null; then
    echo "错误: 未找到 jq 命令。请先安装 jq。"
    exit 1
fi

# 使用 jq 进行排序
# 1. to_entries: 将对象转换为键值对数组
# 2. sort_by: 首先按 value.name 排序，然后按 value.id 排序
# 3. from_entries: 将排序后的数组转换回对象
jq 'to_entries | sort_by(.value.name, .value.id) | from_entries' token.json > token_sorted.json

# 检查 jq 命令是否成功执行
if [ $? -eq 0 ]; then
    mv token_sorted.json token.json
    echo "排序完成。"
else
    echo "排序失败。"
    rm -f token_sorted.json
    exit 1
fi
