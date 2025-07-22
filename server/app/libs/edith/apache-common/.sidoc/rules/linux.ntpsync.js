; (function (input) {
    var okResult = {
        desc: "检查是否设置时钟同步",
        effect: "当未设置时钟同步时可能造成应用异常",
        solution: "设置时钟同步（Chrony或NTP）",
        level: "正常",
        id: "linux.ntpsync",
        name: "时钟同步检查",
        category: "health",
        actual: "",
        expected: "已设置时钟同步（Chrony或NTP）",
    }

    var errResult = {
        desc: "检查是否设置时钟同步",
        effect: "当未设置时钟同步时可能造成应用异常",
        solution: "设置时钟同步（Chrony或NTP）",
        level: "高风险",
        id: "linux.ntpsync",
        name: "时钟同步检查",
        category: "health",
        actual: "",
        expected: "设置时钟同步（Chrony或NTP）",
    }
    
    errResult.desc += '。ntpdate crontab 设置为（' + input['ntpdate crontab'] + "）"
    errResult.desc += '。ntpstat synchronised 设置为（' + input['ntpstat synchronised'] + "）"
    errResult.desc += '。timedatectl synchronized 设置为（' + input['timedatectl synchronized'] + "）"

    ok = true
    if (input['ntpdate crontab'].split("#")[0] == "" // 去除cron中可能存在的注释后比较
        && input['ntpstat synchronised'] == "" // 基于grep，无设置时将没有输出
        && input['timedatectl synchronized'].match("no")) { // NTP synchronized: no 或 NTP synchronized: yes
        ok = false
    }

    if (ok) {
        okResult.actual = "已设置时钟同步（Chrony或NTP）"
        return {
            results: [okResult]
        }
    } else {
        errResult.actual = "未设置时钟同步（Chrony或NTP）"
        return {
            results: [errResult]
        }
    }

})(input)
