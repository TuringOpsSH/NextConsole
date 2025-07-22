(function (input) {
    var results = [];
    var result = {
        desc: "",
        effect: "",
        solution: "仅作为调优或问题排查时的参考",
        level: "正常",
        id: "oracle.osparm",
        name: "系统参数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统参数检查符合最佳实践",
        category: "基本配置检查",
        family: "conf"
    };

    try {
        raw = input.split("\n");

        MemTotal = 0;
        MemFree = 0;
        MemAvailable = 0;
        Buffers = 0;
        Cached = 0;

        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常";
            fields = {};

            // Check fields, reset mixlevel and result.level here:
            fields["name"] = raw[i].split(",")[0].replace(/\"/g, "").trim();

            if (fields["name"] == "transparent_hugepage") {
                fields["value"] = raw[i].split(",")[1].replace(/\"/g, "").trim();
                transparent_hugepage = fields["value"];
            } else {
                fields["value"] = Number(raw[i].split(",")[1].replace(/\"/g, "").trim());
            }

            if (fields["name"] == "SwapTotal") {
                swapTotal = Number(fields["value"]);
                if (Number(fields["value"]) == 0) {
                    mixlevel = "中风险";
                    result.actual += "swapTotal 预期为 !=0, 实际为" + fields["value"] + "; ";
                    result.level = "中风险";
                    result.solution += "为系统配置交换分区; ";
                } else {
                    mixlevel = "正常";
                }
            }

            if (fields["name"] == "MemTotal") {
                MemTotal = Number(fields["value"]);
            }

            if (fields["name"] == "MemFree") {
                MemFree = Number(fields["value"]);
            }

            if (fields["name"] == "MemAvailable") {
                MemAvailable = Number(fields["value"]);
            }

            if (fields["name"] == "Buffers") {
                Buffers = Number(fields["value"]);
            }

            if (fields["name"] == "Cached") {
                Cached = Number(fields["value"]);
            }

            if (fields["name"] == "SwapTotal") {
                SwapTotal = Number(fields["value"]);
            }

            if (fields["name"] == "SwapFree") {
                SwapFree = Number(fields["value"]);
            }

            if (fields["name"] == "AnonHugePages") {
                AnonHugePages = Number(fields["value"]);
            }

            if (fields["name"] == "HugePages_Total") {
                HugePages_Total = Number(fields["value"]);
            }

            if (fields["name"] == "HugePages_Free") {
                HugePages_Free = Number(fields["value"]);
            }

            fields["mixlevel"] = mixlevel;
            result.mixraw.push(fields);
        }

        MemUsed = MemTotal - MemFree - MemAvailable - Buffers - Cached;
        MemUsage = (MemUsed / MemTotal) * 100;

        if (MemUsage > 90) {
            result.mixraw.push({
                name: "内存使用率不超过90%",
                value: "与预期不符",
                mixlevel: "中风险"
            });
            result.actual += "内存使用率大于90% (" + MemUsage.toFixed(2) + "%); ";
            result.level = "中风险";
            result.solution += "进行内存调优; ";
        } else {
            result.mixraw.push({
                name: "内存使用率不超过90%",
                value: "",
                mixlevel: "正常"
            });
        }

        if (SwapFree / SwapTotal < 0.9) {
            result.mixraw.push({
                name: "预期 swapFree / swapTotal >= 0.9",
                value: "与预期不符",
                mixlevel: "中风险"
            });
            result.actual += "系统换页较高, Swap剩余小于90%(" + ((SwapFree / SwapTotal) * 100).toFixed(2) + "%); ";
            result.solution += "检查内存参数设置和系统性能; ";
            result.level = "中风险";
        } else {
            result.mixraw.push({
                name: "预期 swapFree / swapTotal >= 0.9",
                value: "",
                mixlevel: "正常"
            });
        }

        if (transparent_hugepage != "never") {
            result.mixraw.push({
                name: "关闭透明大页",
                value: "未关闭",
                mixlevel: "中风险"
            });
            result.actual += "未关闭透明大页; ";
            result.solution += "; 关闭透明大页";
            result.level = "中风险";
        } else {
            result.mixraw.push({
                name: "关闭透明大页",
                value: "",
                mixlevel: "正常"
            });
        }

        if (MemTotal >= 64424509440 && AnonHugePages != 0) {
            result.mixraw.push({
                name: "内存大于等于 64G 时关闭透明巨页",
                value: "未关闭",
                mixlevel: "中风险"
            });
            result.actual += "内存大于等于 64G 但未关闭透明巨页; ";
            result.solution += "; 关闭透明巨页";
            result.level = "中风险";
        } else {
            result.mixraw.push({
                name: "内存大于等于 64G 时关闭透明巨页",
                value: "",
                mixlevel: "正常"
            });
        }

        if (HugePages_Total > 0 && AnonHugePages > 0) {
            result.mixraw.push({
                name: "不同时开启透明巨页和大页",
                value: "同时开启透明巨页和大页",
                mixlevel: "中风险"
            });
            result.actual += "同时开启透明巨页和大页; ";
            result.solution += "关闭透明巨页或大页; ";
            result.level = "中风险";
        } else {
            result.mixraw.push({
                name: "不同时开启透明巨页和大页",
                value: "",
                mixlevel: "正常"
            });
        }

        if (HugePages_Total > 0) {
            if (HugePages_Free / HugePages_Total > 0.1) {
                result.mixraw.push({
                    name: "大页内存空闲比例不超过 10%",
                    value: "大页内存空闲比例超过 10%",
                    mixlevel: "中风险"
                });
                result.actual += "大页内存空闲比例超过 10%; ";
                result.solution += "调整内存参数设置或检查是否实际使用大页内存; ";
                result.level = "中风险";
            } else {
                result.mixraw.push({
                    name: "大页内存空闲比例不超过 10%",
                    value: "",
                    mixlevel: "正常"
                });
            }
        } else {
            result.mixraw.push({
                name: "大页内存空闲比例不超过 10%",
                value: "",
                mixlevel: "正常"
            });
        }

    } catch (err) {
        result.actual += "部分数据未采集到: " + err.message + "; ";
    }

    results.push(result);
    return { results: results };

})(input);
