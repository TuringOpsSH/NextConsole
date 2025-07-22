; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.view_index_fragmentation_information_for_all_databases",
        name: "查看所有数据库的索引碎片信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "查看所有数据库的索引碎片信息检查正常",
        category: "",
        family: "any"
    }

    // 非空且元素是字符串认定为执行遇到异常
    try {
        if (Array.isArray(input) && input.length > 0) {
            var allStrings = input.every(function (item) {
                return typeof item === 'string';
            });
            if (allStrings) {
                return { results: [result] };
            }
        }
    } catch (error) {
        return { results: [result] }
    }

    try {
        raw = input
        result.raw = $.copy(input)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["DatabaseName"] //string
        // fields["SchemaName"] //string
        // fields["TableName"] //string
        // fields["IndexName"] //string
        // fields["AverageFragmentation"] //string
        // fields["FragmentationSeverity"] //string

		averageFragmentation = Number(fields["AverageFragmentation"])
		if (averageFragmentation < 30){
			fields["mixlevel"] = mixlevel
		}else if (averageFragmentation >= 30 && averageFragmentation < 80){
			fields["mixlevel"] = "中风险"
		}else{
			fields["mixlevel"] = "高风险"
		}
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)