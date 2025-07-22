; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "包含潜在的风险提示信息",
        solution: "结合报错内容进行具体分析",
        level: "正常",
        id: "linux.msglog",
        name: "/var/log/messages 日志关键字检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "/var/log/messages 无错误关键字出现",
        category: "系统日志检查",
        family: "log"
    }

    keyArr = ["emerg", "alert", "fail", "Machine Check Exception", "Out of memory", "soft lockup", "EXT4-fs error", "qla2xxx", "Failing path", "Kernel panic", "NIC Link is Down", "crit", "I/O error", "err"]
    errArr = []

    try {
        raw = input['content']
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            for (j = 0; j < keyArr.length; j++) {
                if (!$.isInArray(errArr, keyArr[j]) && raw[i].match(keyArr[j])) {
                    errArr.push(keyArr[j])
                }
            }
        }

        if (errArr.length != 0) {
            result.actual = "存在以下关键字: "
            for (i = 0; i < errArr.length; i++) {
                result.actual += errArr[i] + "; "
            }
            result.level = "高风险"
        } else {
            result.level = "正常"
            result.actual = "不存在错误关键字"
        }

    } catch (err) {
        $.print(err.message)
        result.level = "正常"
        result.actual = "不存在错误关键字或未收集到数据"
    }

    // $.print(result)
    results.push(result)
    return { results: results }

})(input)