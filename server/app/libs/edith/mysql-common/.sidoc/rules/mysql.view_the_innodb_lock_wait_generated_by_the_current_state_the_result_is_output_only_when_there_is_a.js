; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查看当前状态产生的InnoDB锁等待，仅在有锁等待时有结果输出",
        effect: "响应时间过长、无法完成当前事务",
        solution: "找到锁表的事务，分析锁表原因，进行优化",
        level: "正常",
        id: "mysql.view_the_innodb_lock_wait_generated_by_the_current_state_the_result_is_output_only_when_there_is_a",
        name: "InnoDB锁等待",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在InnoDB锁等待",
        category: "",
        family: "log"
    }


    if (mysqlVersion(params[3]["Value"].match(/\d+\.(?:\d+\.)*\d+/g)[0], "8")) {
        result.actual = "本检查不适用于该版本数据库"
        result.raw = ["本检查不适用于该版本数据库"]
        return {results: [result]}
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

    if (input[0].length > 20) {
        result.level = "中风险"
        result.expected = "不存在InnoDB锁等待"
        result.actual = "请移步下章节查看详细内容"
        result.effect = "响应时间过长、无法完成当前事务"
        result.solution = "找到锁表的事务，分析锁表原因，进行优化"
    }
    result.mixraw = input
    result.raw = input

    results.push(result)
    return {results: results}

})(input, params)
