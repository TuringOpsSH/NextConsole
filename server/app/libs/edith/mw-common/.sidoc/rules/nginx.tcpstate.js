;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "需要具体分析",
        level: "低风险",
        id: "",
        name: "",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "暂无",
        category: "",
        family: "status"
    }
    if (!input) {
        result.actual = "未发现相关记录"
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }
    if (!raw) {
        result.actual = "未发现相关记录"
        return {results: [result]}
    }
    var key = Object.keys(input[0]["metric"])
    for (var i = 0; i < key.length; i++) {
        var result = {
            desc: "-",
            effect: "",
            solution: "",
            level: "低风险",
            id: "",
            name: "",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "",
            category: "动态参数检查",
            family: "status"
        }
        switch (key[i]) {
            case "time_wait":
                result.name = "TIME_WAIT数量"
                result.id = "nginx.tcpstate." + key[i]
                result.raw = input[0]["metric"][key[i]]
                results.push(result)
                break
            case "established":
                result.name = "ESTABLISHED数量"
                result.id = "nginx.tcpstate." + key[i]
                result.raw = input[0]["metric"][key[i]]
                results.push(result)
                break
        }
    }
    return {results: results}
})(input)
