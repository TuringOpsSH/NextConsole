; (function (input) {
    if (!input) {
        return { results: [] }
    }

    var results = []
    var ok = true
    var desc = ""
    var actual = ""
    for (i = 0; i < input.length; i++) {
        if (!input[i].match("^Inter-") && !input[i].match("^face")) {
            ens = input[i].split(":")[0]
            receiveDrop = input[i].replace(/  +/g, ' ').split(" ")[4]
            transmitDrop = input[i].replace(/  +/g, ' ').split(" ")[11]
            if (Number(receiveDrop) > 0 || Number(transmitDrop) > 0) {
                actual += ens + "的Receive drop 为 " + receiveDrop + "，Transmit drop 为 " + transmitDrop + "; "
                desc += ens + "的Receive drop 为 " + receiveDrop + "，Transmit drop 为 " + transmitDrop + "; "
                ok = false
            }
        }
    }

    if (!ok) {
        results.push({
            desc: "网卡是否存在驱动丢包检查: " + desc,
            effect: "存在驱动丢包",
            solution: "检查网络是否正常",
            level: "高风险",
            id: "linux.procnetdev",
            name: "网卡是否存在驱动丢包检查",
            category: "系统健康检查",
            actual: "网卡存在驱动丢包: " + actual,
            expected: "不存在驱动丢包",
        })
    } else {
        results.push({
            desc: "网卡是否存在驱动丢包检查。经检查无丢包情况。",
            effect: "存在驱动丢包",
            solution: "检查网络是否正常",
            level: "正常",
            id: "linux.procnetdev",
            name: "网卡是否存在驱动丢包检查",
            actual: "不存在驱动丢包。",
            expected: "不存在驱动丢包",
            category: "系统健康检查"
        })
    }
    return { results: results }

})(input)
