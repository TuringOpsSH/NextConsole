; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "主从复制涉及到的重要参数",
        effect: "可能存在丢失数据的情况",
        solution: "请检查binlog_format、expire_logs_days、log_bin、slave_skip_errors和sync_binlog参数是否正确设置",
        level: "正常",
        id: "mysql.important_parameters_involved_in_master-slave_replication",
        name: "主从复制参数",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果; binlog_format = ROW; expire_logs_days != 0; log_bin = ON; slave_skip_errors = OFF; sync_binlog = 1",
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
            if (input[i][j]["Variable_name"] == "binlog_format") {
                if (input[i][j]["Value"] != "ROW") {
                    input[i][j]["inspectionLevel"] = "中风险"
                    result.level != "中风险"
                    result.expected = result.expected + "; binlog_format = ROW"
                    result.actual = result.actual + "; binlog_format = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 从库可能存在丢失数据的情况"
                }
            }

            if (input[i][j]["Variable_name"] == "expire_logs_days") {
                if (input[i][j]["Value"] == 0) {
                    input[i][j]["inspectionLevel"] = "中风险"
                    result.level != "中风险"
                    result.expected = result.expected + "; expire_logs_days != 0"
                    result.actual = result.actual + "; expire_logs_days = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 注意观察磁盘空间大小"
                }
            }

            if (input[i][j]["Variable_name"] == "log_bin") {
                if (input[i][j]["Value"] != "ON") {
                    input[i][j]["inspectionLevel"] = "中风险"
                    result.level != "中风险"
                    result.expected = result.expected + "; log_bin = ON"
                    result.actual = result.actual + "; log_bin = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 未开启二进制日志"
                }
            }

            if (input[i][j]["Variable_name"] == "slave_skip_errors") {
                if (input[i][j]["Value"] != "OFF") {
                    input[i][j]["inspectionLevel"] = "中风险"
                    result.level != "中风险"
                    result.expected = result.expected + "; slave_skip_errors = ON"
                    result.actual = result.actual + "; slave_skip_errors = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 从库可能存在丢失数据的情况"
                }
            }

            if (input[i][j]["Variable_name"] == "sync_binlog") {
                if (input[i][j]["Value"] != 1) {
                    input[i][j]["inspectionLevel"] = "中风险"
                    result.level != "中风险"
                    result.expected = result.expected + "; sync_binlog = 1"
                    result.actual = result.actual + "; sync_binlog = " + input[i][j]["Value"]
                    result.effect = result.effect + "; 可能存在丢失数据的情况"
                }
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
