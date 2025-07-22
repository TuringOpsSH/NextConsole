; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "错误关键字出现次数较多时可能存在非法登录请求",
        solution: "检查主机登录历史, 同时确保主机密码符合安全合规要求并及时修改密码",
        level: "正常",
        id: "linux.varlogsecure",
        name: "/var/log/secure 日志关键字检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "/var/log/secure 无错误关键字出现",
        category: "系统日志检查",
        family: "log"
    }

    count_failed_password = 0
    count_fail = 0

    try {
        raw = input['content']
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            if (raw[i].match("Failed password")) {
                count_failed_password += 1
            } else if (raw[i].match("fail")) {
                count_fail += 1
            }
        }

        if (count_failed_password != 0 || count_fail != 0) {
            result.actual = "日志中出现 Failed password " + count_failed_password + "次, 出现 fail " + count_fail + "次."
            result.level = "中风险"
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