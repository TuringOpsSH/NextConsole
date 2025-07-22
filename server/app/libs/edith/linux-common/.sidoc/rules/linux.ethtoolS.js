; (function (input) {
    if (!input) {
        return { results: [] }
    }

    var results = []
    var ok = true
    var desc = ""
    var actual = ""
    for (i = 0; i < input.length; i++) {
        for (var key in input[i]["metric"]) {
            if (key.match("errors")) {
                ens = key.split("__")[0]
                errorType = key.split("__")[1]
                errorCount = input[i]["metric"][key]
                if (Number(errorCount) > 0) {
                    desc += ens + "的" + errorType + "为" + errorCount + "; "
                    actual =  ens + "的" + errorType + "为" + errorCount + "; "
                    ok = false
                }
            }
        }
        break;
    }

    if (!ok) {
        results.push({
            desc: "检查网络接口在ethtool -S 统计信息输出中生成的rx_crc_errors或类似内容: " + desc,
            effect: "存在网络接口报错信息",
            solution: "检查网络是否正常",
            level: "高风险",
            id: "linux.ethtoolS",
            name: "网络接口错误检查",
            category: "系统健康检查",
            actual: "" + actual,
            expected: "网络接口不存在报错信息",
        })
    } else {
        results.push({
            desc: "检查网络接口在ethtool -S 统计信息输出中生成的rx_crc_errors或类似内容。经检查无报错信息。",
            effect: "存在网络接口报错信息",
            solution: "检查网络是否正常",
            level: "正常",
            id: "linux.ethtoolS",
            name: "网络接口错误检查",
            category: "系统健康检查",
            actual: "网络接口不存在报错信息",
            expected: "网络接口不存在报错信息",
        })
    }
    return { results: results }

})(input)
