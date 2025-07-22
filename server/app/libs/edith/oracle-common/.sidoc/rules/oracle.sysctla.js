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
        id: "oracle.sysctla",
        name: "系统内核参数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统内核参数符合最佳实践",
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

    greplist = ["kernel.shmall", "kernel.shmmax", "vm.swappines", "vm.swappiness", "vm.dirty_background_ratio", "vm.dirty_ratio", "vm.dirty_expire_centisecs", "vm.dirty_writeback_centisecs", "net.ipv4.ipfrag_high_thresh", "net.ipv4.ipfrag_low_thresh", "vm.min_free_kbytes", "kernel.randomize_va_space", "kernel.exec-shield"]

    for (k in raw) {
        mixlevel = ""
        fields = {}
        fields["name"] = k
        if (!isInArray(greplist, k)) {
            continue
        }

        fields["value"] = raw[k]

        if (k == "kernel.shmall") {
            shmall = Number(fields["value"])
        }

        if (k == "kernel.shmmax") {
            shmmax = Number(fields["value"])
        }

        if (fields["name"] == "vm.swappiness") {
            if (Number(fields["value"]) > 10) {
                // mixlevel = "中风险"
                result.actual += "vm.swappiness 预期为10, 实际为" + fields["value"] + "; "
                // result.level = "中风险"
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "vm.dirty_expire_centisecs") {
            if (Number(fields["value"]) == 0 || Number(fields["value"]) > 500) {
                // mixlevel = "中风险"
                result.actual += "vm.dirty_expire_centisecs 预期为500, 实际为" + fields["value"] + "; "
                // result.level = "中风险"
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "vm.dirty_writeback_centisecs") {
            if (Number(fields["value"]) == 0 || Number(fields["value"]) > 100) {
                // mixlevel = "中风险"
                result.actual += "vm.dirty_writeback_centisecs 预期为100, 实际为" + fields["value"] + "; "
                // result.level = "中风险"
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "net.ipv4.ipfrag_high_thresh") {
            if (Number(fields["value"]) != 16777216) {
                // mixlevel = "中风险"
                result.actual += "net.ipv4.ipfrag_high_thresh 预期为 16777216, 实际为" + fields["value"] + "; "
                // result.level = "中风险"
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "net.ipv4.ipfrag_low_thresh") {
            if (Number(fields["value"]) != 15728640) {
                // mixlevel = "中风险"
                result.actual += "net.ipv4.ipfrag_low_thresh 预期为 15728640, 实际为" + fields["value"] + "; "
                // result.level = "中风险"
            } else {
                // mixlevel = "正常"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    if (shmmax / 4096 > shmall) {
        result.mixraw.push({
            name: "shmmax /4096 > shmall",
            value: "YES",
            mixlevel: ""
            // mixlevel: "中风险"
        })
        result.actual += "shmmax 配置大于shmall" + "; "
        result.solution += "调整shmall,shmmax 设置" + "; "
        // result.level = "中风险"
    } else {
        result.mixraw.push({
            name: "shmmax /4096 > shmall",
            value: "NO",
            mixlevel: ""
            // mixlevel: "正常"
        })
    }

    results.push(result)
    return { results: results }

})(input)
