;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "一些重要的参数",
        effect: "; 可能丢失数据; 无法级联复制; 无法区分大小写; 可能出现锁; 可能运行慢",
        solution: "请逐个查看各指标，根据情况进行修复",
        level: "正常",
        id: "mysql.some_important_parameters",
        name: "重要参数",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果; innodb_flush_log_at_trx_commit = 1; log_slave_updates = ON; lower_case_table_names = 1; tx_isolation == READ-COMMITTED; long_query_time == 5",
        category: "",
        family: "log"
    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果; innodb_flush_log_at_trx_commit = 1; log_slave_updates = ON; lower_case_table_names = 1; tx_isolation == READ-COMMITTED; long_query_time == 5"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return {results: results}
    }
    result.raw = input

    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            input[i][j]["inspectionLevel"] = "正常"

            if (input[i][j]["Variable_name"] == "innodb_flush_log_at_trx_commit") {
                if (input[i][j]["Value"] != 1) {
                    if (result.level != "高风险") {
                        result.level = "高风险"
                    }
                    input[i][j]["inspectionLevel"] = "高风险"
                    //预期值不要让他动态变化，就四种直接罗列
                    //result.expected = result.expected + "; innodb_flush_log_at_trx_commit != 1"
                    result.actual = result.actual + "; innodb_flush_log_at_trx_commit = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 可能丢失数据"
                }
            }
            if (input[i][j]["Variable_name"] == "log_slave_updates") {
                if (input[i][j]["Value"] == "OFF") {
                    if (result.level != "高风险") {
                        result.level = "中风险"
                    }
                    input[i][j]["inspectionLevel"] = "中风险"
                    //result.expected = result.expected + "; log_slave_updates = ON"
                    result.actual = result.actual + "; log_slave_updates = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 无法级联复制"
                }
            }
            if (input[i][j]["Variable_name"] == "lower_case_table_names") {
                if (input[i][j]["Value"] != 1) {
                    if (result.level != "高风险") {
                        result.level = "中风险"
                    }
                    input[i][j]["inspectionLevel"] = "中风险"
                    //result.expected = result.expected + "; lower_case_table_names = 1"
                    result.actual = result.actual + "; lower_case_table_names = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 无法区分大小写"
                }
            }
            if (input[i][j]["Variable_name"] == "tx_isolation") {
                if (input[i][j]["Value"] != "READ-COMMITTED") {
                    if (result.level != "高风险") {
                        result.level = "中风险"
                    }
                    input[i][j]["inspectionLevel"] = "中风险"
                    //result.expected = result.expected + "; tx_isolation == READ-COMMITTED"
                    result.actual = result.actual + "; tx_isolation = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 可能出现锁"
                }
            }
            if (input[i][j]["Variable_name"] == "long_query_time") {
                if (input[i][j]["Value"] > 5) {
                    if (result.level != "高风险") {
                        result.level = "低风险"
                    }
                    input[i][j]["long_query_time"] = "低风险"
                    //result.expected = result.expected + "; tx_isolation == READ-COMMITTED"
                    result.actual = result.actual + "; long_query_time = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 可能运行慢"
                }
            }
        }
    }
    result.solution = "涵盖多个指标，请逐个查看"
    result.mixraw = input

    results.push(result)
    return {results: results}

})(input, params)
