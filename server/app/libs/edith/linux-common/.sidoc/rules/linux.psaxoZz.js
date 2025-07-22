; (function (input) {
    var okResult = {
        desc: "检查是否存在僵死进程",
        effect: "可能存在不合理的资源占用",
        solution: "根据进程具体信息进行处理",
        level: "正常",
        id: "linux.psaxoZz",
        name: "僵死进程检查",
        raw: [],
        actual: "",
        expected: "不存在僵死进程",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "检查是否存在僵死进程",
        effect: "可能存在不合理的资源占用",
        solution: "根据进程具体信息进行处理",
        level: "中风险",
        id: "linux.psaxoZz",
        name: "僵死进程检查",
        raw: [],
        actual: "存在僵死进程：",
        expected: "不存在僵死进程",
        category: "系统健康检查"
    }

    if (!input) {
        return { results: [okResult] }
    }

    for (i = 0; i < input.length; i++) {
        if (!input[i]["metric"]) {
            okResult.actual = "不存在僵死进程"
            return { results: [okResult] }
        } else {
            errResult.actual += input[i]["metric"]
            errResult.raw = input[i]["metric"]
            return { results: [errResult] }
        }
        break // 检查第1个即可
    }

})(input)
