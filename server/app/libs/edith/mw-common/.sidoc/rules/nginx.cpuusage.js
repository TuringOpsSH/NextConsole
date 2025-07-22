;(function (input) {
    var results = []
    var result = {
        desc: "Nginx进程所使用的CPU",
        level: "低风险",
        id: "nginx.status.cpuusage",
        name: "Nginx进程CPU使用率",
        raw: [],
        actual: 0,
        expected: "70以下",
        family: "status",
    }
    if (!input) {
        result.actual = 0
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = 0
        return {results: [result]}
    }
    var errResult = {
        desc: "Nginx进程所使用的CPU",
        level: "中风险",
        id: "nginx.status.cpuusage",
        name: "Nginx进程CPU使用率",
        raw: [],
        actual: 0,
        expected: "70以下",
        family: "status"
    }
    var cpuUsage = input[0]["metric"]
    if (cpuUsage > 70.0) {
        errResult.actual = cpuUsage
        errResult.raw = cpuUsage
        results.push(errResult)
    } else {
        result.actual = cpuUsage
        result.raw = cpuUsage
        results.push(result)
    }
    return {results: results}
})(input)
