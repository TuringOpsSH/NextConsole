; (function (input) {
    var okResult = {
        desc: "防火墙状态检查",
        effect: "可能影响正常的网络访问",
        solution: "在确认不需要主机防火墙后关闭防火墙",
        level: "正常",
        id: "linux.iptables",
        name: "防火墙状态检查",
        category: "系统健康检查",
        actual: "",
        expected: "禁用主机防火墙（inactive，not-installed 或 disabled）"
    }

    var errResult = {
        desc: "防火墙状态检查",
        effect: "可能影响正常的网络访问",
        solution: "在确认不需要主机防火墙后关闭防火墙",
        level: "中风险",
        id: "linux.iptables",
        name: "防火墙状态检查",
        category: "系统健康检查",
        actual: "",
        expected: "禁用主机防火墙（inactive，not-installed 或 disabled）"
    }

    if (!input) {
        return { results: [okResult] }
    }

    for (i = 0; i < input.length; i++) {
        if (!input[i]["metric"]) {
            return { results: [okResult] }
        } else {
            if (input[i]["metric"].match("inactive") || input[i]["metric"].match("disabled") || input[i]["metric"].match("not-installed")) {
                okResult.actual = input[i]["metric"]
                return { results: [okResult] }
            } else {
                errResult.desc += "。当前状态为" + input[i]["metric"]
                errResult.raw = input[i]["metric"]
                errResult.actual = input[i]["metric"]
                return { results: [errResult] }
            }
        }
        break // 检查第1个即可
    }

})(input)
