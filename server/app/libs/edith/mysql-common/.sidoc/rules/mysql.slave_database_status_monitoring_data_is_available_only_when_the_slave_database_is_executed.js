; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "从库状态监测（需要在从库执行才有数据）",
        effect: "监测从库状态，确保从库正常运行",
        solution: "如果从库状态异常，需要及时排查问题并修复",
        level: "正常",
        id: "mysql.slave_database_status_monitoring_data_is_available_only_when_the_slave_database_is_executed",
        name: "从库状态",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果; Slave_IO_Running = YES; Slave_SQL_Running = YES; Seconds_Behind_Master < 10",
        category: "",
        family: "log"
    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return {results: results}
    }
    result.raw = input
    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            if (input[i][j]["Slave_IO_Running"].toLowerCase() == "no") {
                input[i][j]["inspectionLevel"] = "高风险"
                result.level = "高风险"
                result.expected = result.expected + "; Slave_IO_Running = YES"
                result.actual = result.actual + "; Slave_IO_Running = " + input[i][j]["Slave_IO_Running"]
                result.solution = result.solution + "- 从库状态异常"
            }

            if (input[i][j]["Slave_SQL_Running"].toLowerCase() == "no") {
                input[i][j]["inspectionLevel"] = "高风险"
                result.level = "高风险"
                result.expected = result.expected + "; Slave_SQL_Running = YES"
                result.actual = result.actual + "; Slave_SQL_Running = " + input[i][j]["Slave_SQL_Running"]
                result.solution = result.solution + "- 从库状态异常"
            }

            if (input[i][j]["Seconds_Behind_Master"] > 10) {
                input[i][j]["inspectionLevel"] = "高风险"
                result.level = "高风险"
                result.expected = result.expected + "; Seconds_Behind_Master < 10"
                result.actual = result.actual + "; Seconds_Behind_Master = " + input[i][j]["Seconds_Behind_Master"]
                result.solution = result.solution + "- 主从延迟过高"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
