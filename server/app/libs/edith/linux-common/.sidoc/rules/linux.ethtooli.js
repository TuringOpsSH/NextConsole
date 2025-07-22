; (function (input) {
    var okResult = {
        desc: "检查所有活动网络链路状态是否正常",
        effect: "可能会影响网络稳定",
        solution: "查看网络链路具体信息",
        level: "正常",
        id: "linux.ethtooli",
        name: "网卡链路状态检查",
        raw: [],
        category: "系统健康检查",
        actual: "",
        expected: "所有活动网络链路状态都为正常",
    }

    var errResult = {
        desc: "检查所有活动网络链路状态是否正常",
        effect: "可能会影响网络稳定",
        solution: "查看网络链路具体信息",
        level: "高风险",
        id: "linux.ethtooli",
        name: "网卡链路状态检查",
        category: "系统健康检查",
        raw: [],
        actual: "未配置",
        expected: "所有活动网络链路状态都为正常",
    }

    if (!input) {
        errResult.actual = "未检测到网络链路状态"
        return { results: [errResult] }
    }

    for (i = 0; i < input.length; i++) {
        var ens = ""
        var info = {}
        var thisinfo = {}
        for (var key in input[i]["metric"]) {
            var thisEns = key.split("__")[0]
            var thisKey = key.split("__")[1]
            var thisVal = input[i]["metric"][key]
            if (ens != thisEns) {
                ens = thisEns
            }
            if (thisKey == "Link detected") {
                thisinfo.Link_detected = thisVal
            }
            else if (thisKey == "Speed") {
                thisinfo.Speed = thisVal
            }
            else if (thisKey == "Duplex") {
                thisinfo.Duplex = thisVal
            }
            else if (thisKey == "Supported ports") {
                thisinfo.Supported_ports = thisVal
            }
            else if (thisKey == "driver") {
                thisinfo.driver = thisVal
            }
            else if (thisKey == "version") {
                thisinfo.version = thisVal
                info[ens] = thisinfo

            }
        }
        okResult.raw.push(info)
        break;
    }

    if (okResult.raw.length != 0) {
        return { results: [okResult] }
    } else {
        return { results: [errResult] }
    }


})(input)
