; function isInArray(arr, value) {
    for (var i = 0; i < arr.length; i++) {
        if (value === arr[i]) {
            return true;
        }
    }
    return false;
}

; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "仅作为调优或问题排查时的参考",
        level: "正常",
        id: "oracle.mem",
        name: "系统内存参数及使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统内存参数符合最佳实践, 使用率正常",
        category: "基本配置检查",
        family: "conf"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    //greplist = ["kernel.shmall", "kernel.shmmax", "vm.swappines", "vm.swappiness", "vm.dirty_background_ratio", "vm.dirty_ratio", "vm.dirty_expire_centisecs", "vm.dirty_writeback_centisecs", "net.ipv4.ipfrag_high_thresh", "net.ipv4.ipfrag_low_thresh", "vm.min_free_kbytes", "kernel.randomize_va_space", "kernel.exec-shield"]

    // AnonHugePages = 0
    for (k in raw) {
        mixlevel = ""
        fields = {}
        fields["name"] = k
        fields["value"] = raw[k]

        if (fields["name"] == "swapTotal") {
            swapTotal = Number(fields["value"])
            if (Number(fields["value"]) == 0) {
                mixlevel = "中风险"
                result.actual += "swapTotal 预期为 !=0, 实际为" + fields["value"] + "; "
                result.level = "中风险"
                result.solution += "为系统配置交换分区; "
            } else {
                mixlevel = "正常"
            }
        }

        if (fields["name"] == "usedPercent") {
            if (Number(fields["value"]) > 90.0) {
                mixlevel = "中风险"
                result.actual += "内存使用率大于90% (" + fields["value"].toFixed(2) + "%); "
                result.level = "中风险"
                result.solution += "进行内存调优; "
            } else {
                mixlevel = "正常"
            }
        }

        if (fields["name"] == "total") {
            total = Number(fields["value"])
        }

        if (fields["name"] == "swapFree") {
            swapFree = Number(fields["value"])
        }

        // if (fields["name"] == "AnonHugePages") { // mem 似乎无此项
        //     AnonHugePages = Number(fields["value"])
        // }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    if (swapFree / swapTotal < 0.9) {
        result.mixraw.push({
            name: "预期 swapFree / swapTotal >= 0.9",
            value: "与预期不符",
            mixlevel: "中风险"
        })
        result.actual += "系统换页较高, Swap剩余小于90%(" + ((swapFree / swapTotal ) * 100).toFixed(2) + "%); "
        result.solution += "检查内存参数设置和系统性能; "
        result.level = "中风险"
    } else {
        result.mixraw.push({
            name: "预期 swapFree / swapTotal >= 0.9",
            value: "",
            mixlevel: "正常"
        })
    }


    // if (total >= 64424509440 && AnonHugePages != 0) {
    //     result.mixraw.push({
    //         name: "内存大于等于 64G 时关闭透明巨页",
    //         value: "未关闭",
    //         mixlevel: "中风险"
    //     })
    //     result.actual += "内存大于等于 64G 但未关闭透明巨页; "
    //     result.solution += "; 关闭透明巨页"
    //     result.level = "中风险"
    // } else {
    //     result.mixraw.push({
    //         name: "内存大于等于 64G 时关闭透明巨页",
    //         value: "",
    //         mixlevel: "正常"
    //     })
    // }

    // if (raw["hugePagesTotal"] > 0 && AnonHugePages > 0) {
    //     result.mixraw.push({
    //         name: "不同时开启透明巨页和大页",
    //         value: "同时开启透明巨页和大页",
    //         mixlevel: "中风险"
    //     })
    //     result.actual += "同时开启透明巨页和大页; "
    //     result.solution += "关闭透明巨页或大页; "
    //     result.level = "中风险"
    // } else {
    //     result.mixraw.push({
    //         name: "不同时开启透明巨页和大页",
    //         value: "",
    //         mixlevel: "正常"
    //     })
    // }

    // if (raw["hugePagesTotal"] > 0) {
    //     if (raw["hugePagesFree"] / raw["hugePagesTotal"] > 0.1) {
    //         result.mixraw.push({
    //             name: "大页内存空闲比例不超过 10%",
    //             value: "大页内存空闲比例超过 10%",
    //             mixlevel: "中风险"
    //         })
    //         result.actual += "大页内存空闲比例超过 10%; "
    //         result.solution += "调整内存参数设置或检查是否实际使用大页内存; "
    //         result.level = "中风险"
    //     } else {
    //         result.mixraw.push({
    //             name: "大页内存空闲比例不超过 10%",
    //             value: "",
    //             mixlevel: "正常"
    //         })
    //     }
    // } else {
    //     result.mixraw.push({
    //         name: "大页内存空闲比例不超过 10%",
    //         value: "",
    //         mixlevel: "正常"
    //     })
    // }


    results.push(result)
    return { results: results }

})(input)
