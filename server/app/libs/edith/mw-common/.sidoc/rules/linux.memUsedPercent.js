; (function (input) {

    var results = []
    //检查内容使用情况
    
    if (input["usedPercent"] > 90) {
        results.push({
            desc: "内存使用率过高",
            effect: "可能影响业务",
            usedPercent: "",
            solution: "排查各应用占用内存情况，合理进行扩容",
            level: "高风险",
            id: "linux.memUsedPercent",
            name: "内存使用率检查",
            usedPercent: input["usedPercent"].toFixed(2) + "%",
            category: "基本配置检查",
            actual: input["usedPercent"].toFixed(2) + "%",
            expected: "内存使用率小于 90%",
        })
    } else {
        results.push({
            desc: "内存使用率正常",
            level: "正常",
            id: "linux.memUsedPercent",
            usedPercent: "",
            name: "内存使用率检查",
            category: "基本配置检查",
            usedPercent: input["usedPercent"].toFixed(2) + "%",
            category: "基本配置检查",
            actual: input["usedPercent"].toFixed(2) + "%",
            expected: "内存使用率小于 90%",
        })
    }

    //检查swap空间设置
    var total = (input["total"] / 1024 / 1024)
    var swapTotal = (input["swapTotal"] / 1024 / 1024)
    if (total < 2048) {
        if (swapTotal != total * 2) {
            results.push({
                desc: "Swap空间大小和物理内存不匹配",
                effect: "可能影响业务",
                actual: "",
                expected: "",
                level: "低风险",
                id: "linux.swapCheck",
                name: "Swap空间设置检查",
                category: "capacity",
                actual: swapTotal.toFixed(2) + "MB",
                expected: "Swap空间应该设置为内存的两倍"
            })
        }

    } else if (total >= 2048 && total <= 8192) {
        if (swapTotal != total) {
            results.push({
                desc: "Swap空间大小和物理内存不匹配",
                effect: "可能影响业务",
                actual: "",
                expected: "",
                level: "低风险",
                id: "linux.swapCheck",
                name: "Swap空间设置检查",
                category: "capacity",
                actual: swapTotal.toFixed(2) + "MB",
                expected: "Swap空间应该设置为和内存一样大小"
            })
        }
    } else if (total > 8192) {
        if (swapTotal != total / 2) {
            results.push({
                desc: "Swap空间大小和物理内存不匹配",
                effect: "可能影响业务",
                actual: "",
                expected: "",
                level: "低风险",
                id: "linux.swapCheck",
                name: "Swap空间设置检查",
                category: "capacity",
                actual: swapTotal.toFixed(2) + "MB",
                expected: "Swap空间应该设置为内存的一半"
            })
        }
    } else {
        results.push({
            desc: "Swap空间设置正常",
            level: "正常",
            id: "linux.swapCheck",
            name: "Swap空间设置检查",
            category: "capacity",
            actual: swapTotal.toFixed(2) + "MB",
            expected: "Swap空间应该设置正常"
        })
    }

    //检查swap使用率
    var swapTotal = input["swapTotal"]
    var swapCached = input["swapCached"]
    var swapFree = input["swapFree"]
    var swapUsedPercent = (swapTotal - swapCached) / swapFree
    if (swapUsedPercent > 20) {
        results.push({
            desc: "Swap空间使用率过高" + swapUsedPercent + "%",
            effect: "可能影响业务",
            solution: "重启Swap相关进程，或对Swap空间进行扩容",
            level: "高风险",
            actual: swapUsedPercent + "%",
            expected: "Swap空间可用率小于 80%",
            id: "linux.swapUsedPercent",
            name: "Swap空间使用率检查",
            category: "capacity"

        })
    } else {
        results.push({
            desc: "Swap空间使用率正常",
            level: "正常",
            id: "linux.swapUsedPercent",
            name: "Swap空间使用率检查",
            actual: swapUsedPercent + "%",
            expected: "Swap空间可用率小于 80%",
            category: "capacity"
        })
    }


    return { results: [results] }
})(input)