;(function (input) {
    var results = []
    var result = {
        desc: "MongoDB日志中可能包含错误或警告的日志条目",
        effect: "",
        solution: "",
        level: "正常",
        id: "mongo.warningLog",
        name: "错误或警告日志",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        logs=[]
        for (let i = 0; i < raw["log"].length; i++) {
            let obj = JSON.parse(raw["log"][i])
            logs.push(obj)
        }
        res={}
        res["totalLinesWritten"]=raw["totalLinesWritten"]
        res["ok"]=raw["ok"]
        res["log"]=logs
        result.raw = res
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}

})(input)
