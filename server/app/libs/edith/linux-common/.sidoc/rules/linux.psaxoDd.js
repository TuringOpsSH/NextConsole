; (function (input) {
    var okResult = {
        desc: "检查是否存在不可中断进程",
        effect: "进程不接收信号，可能存在不合理的资源占用",
        solution: "根据进程具体信息进行处理",
        level: "正常",
        id: "linux.psaxoDd",
        name: "不可中断进程检查",
        raw: [],
        actual: "不存在不可中断进程",
        expected: "不存在不可中断进程",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "检查是否存在不可中断进程",
        effect: "进程不接收信号，可能存在不合理的资源占用",
        solution: "根据进程具体信息进行处理",
        level: "中风险",
        id: "linux.psaxoDd",
        name: "不可中断进程检查",
        actual: "存在不可中断进程" ,
        expected: "不存在不可中断进程",
        raw: [],
        category: "系统健康检查"
    }

    if (!input) {
        return { results: [okResult] }
    }

    for (i = 0; i < input.length; i++) {
        if (!input[i]["metric"]) {
            okResult.actual = input[i]["metric"]
            return { results: [okResult] }
        } else {
            errResult.actual += errResult.raw
            errResult.raw = input[i]["metric"]
            return { results: [errResult] }
        }
        break // 检查第1个即可
    }

})(input)
