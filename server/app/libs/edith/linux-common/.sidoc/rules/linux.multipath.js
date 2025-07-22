; (function (input) {
    var okResult = {
        desc: "检查多路径是否正常",
        effect: "可能影响数据存储",
        solution: "须根据报错信息及时处理",
        level: "正常",
        id: "linux.multipath",
        name: "多路径状态检查",
        raw: [],
        actual: "经检查未发现err/fail报错信息" ,
        expected: "经检查未发现err/fail报错信息。",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "检查多路径是否正常",
        effect: "可能影响数据存储",
        solution: "须根据报错信息及时处理",
        level: "高风险",
        id: "linux.multipath",
        name: "多路径状态检查",
        raw: [],
        actual: "发现err/fail报错信息，详情请查看日志内容" ,
        expected: "经检查未发现err/fail报错信息。",
        category: "系统健康检查"
    }

    ok = true
    for (i = 0; i < input.length; i++) {
        if (!input[i]["metric"]) {
            if (input[i]["err"]) {
                okResult.desc += "。经检查发现" + input[i]["err"].replace(/command-not-found:/g, "不存在").replace(/\n/g, ";")                    
                okResult.desc += "。即主机未使用multipath多路径、EMC或华为存储之一。"
            }
        } else {
            if (input[i]["metric"].match("fail") || input[i]["metric"].match("err")) {
                errResult.desc += "。发现err/fail报错信息，详情请查看日志内容。"
                errResult.raw = input[i]["metric"].split("\n")
                ok = false
            }else{
                okResult.desc += "。经检查未发现err/fail报错信息。"
            }
        }
        break // 检查第1个即可
    }

    if (ok) {
        return {
            results: [okResult]
        }
    } else {
        return {
            results: [errResult]
        }
    }

})(input)
