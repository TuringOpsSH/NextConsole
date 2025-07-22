; (function (input) {

    var results = []
    if (input == "") {
        return { results: [results] }
    }
    //系统内核架构检查
    //if (input["kernelArch"] != "x86_64") {
    if (input["kernelArch"] != "x86_64" &&  input["kernelArch"].indexOf('aarch64') == -1) {

        results.push({
            desc: "内核架构:" + input["kernelArch"],
            solution: "建议使用64位架构",
            level: "中风险",
            id: "linux.arch",
            name: "内核架构检查",
            category: "系统配置检查",
            actual: input["kernelArch"],
            expected: "x86_64 或 aarch64",
        })

    } else {
        results.push({
            desc: "内核架构:" + input["kernelArch"],
            solution: "当前配置正常",
            level: "正常",
            id: "linux.arch",
            name: "内核架构检查",
            category: "系统配置检查",
            actual: input["kernelArch"],
            expected: "x86_64 或 aarch64",
        })

    }

    //系统版本生命周期检查
    var effect = "系统生命周期结束后将无法或难以获得补丁等支持";
    var sys = input["platform"];

    var centos_version = 7
    if (input["platformVersion"] != "") {
        centos_version = input["platformVersion"].split(".")[0];
    }

    var redhat_all_version = input["platformVersion"];
    var redhat_first_version = centos_version;

    if (sys == "centos") {
        if (centos_version == "6") {
            results.push({
                desc: "CentOS Linux 6发行版生命周期于2020年11月30日截止，您的系统已过期",
                solution: "根据实际情况升级系统版本",
                level: "高风险",
                id: "linux.eof",
                name: "系统版本生命周期检查",
                category: "系统健康检查",
                effect: effect,
                actual: "您的系统为" + input["platform"] + "," + "（CentOS Linux 6发行版生命周期于2020年11月30日截止）",
                expected: "系统版本处于产品生命周期内"
            })
            return { results: results }
        } else if (centos_version == "7") {

            var now_date = new Date();
            var end_date = new Date(2024, 6, 30);
            var now_s_date = now_date.getTime();
            var end_s_date = end_date.getTime();

            if (now_s_date < end_s_date) {

                results.push({
                    desc: "判断系统版本是否过期",
                    solution: "根据实际情况升级系统版本",
                    level: "正常",
                    id: "linux.eof",
                    name: "系统版本生命周期检查",
                    category: "系统健康检查",
                    effect: effect,
                    actual: input["platform"],
                    expected: "系统版本处于产品生命周期内",
                })
                return { results: results }
            } else {

                results.push({
                    desc: "判断系统版本是否过期",
                    effect: "系统已过期，请注意",
                    solution: "根据实际情况升级系统版本",
                    level: "高风险",
                    id: "linux.eof",
                    name: "系统版本生命周期检查",
                    category: "系统健康检查",
                    effect: effect,
                    actual: input["platform"] + "（CentOS Linux 7发行版生命周期于2024年6月30日截止）",
                    expected: "系统版本处于产品生命周期内",
                })
                return { results: results }
            }
        } else if (centos_version == "8") {

            results.push({
                desc: "CentOS Linux 8发行版生命周期于2021年12月31日截止，您的系统已过期",
                solution: "根据实际情况升级系统版本",
                level: "高风险",
                id: "linux.eof",
                name: "系统版本生命周期检查",
                category: "系统健康检查",
                effect: effect,
                actual: "您的系统为" + input["platform"] + "," + "（CentOS Linux 8发行版生命周期于2021年12月31日截止）",
                expected: "系统版本处于产品生命周期内"
            })
            return { results: results }
        }


    } else if (sys == "redhat") {

        if (redhat_all_version == "6.10" || parseInt(redhat_first_version) > 6) {

            results.push({
                desc: "判断系统版本是否过期",
                solution: "根据实际情况升级系统版本",
                level: "正常",
                id: "linux.eof",
                name: "系统版本生命周期检查",
                category: "系统健康检查",
                effect: effect,
                actual: input["platform"],
                expected: "系统版本处于产品生命周期内"
            })
            return { results: results }
        } else {

            results.push({
                desc: "RedHat Linux 6发行版生命周期于2020年11月30日截止，您的系统已过期",
                solution: "根据实际情况升级系统版本",
                level: "高风险",
                id: "linux.eof",
                name: "系统版本生命周期检查",
                category: "系统健康检查",
                effect: effect,
                actual: "您的系统为" + input["platform"] + "," + "（RedHat Linux 6发行版生命周期于2020年11月30日截止）",
                expected: "系统版本处于产品生命周期内"
            })
            return { results: results }
        }
    } else {
        results.push({
            desc: "该系统不是centos或redhat",
            solution: "根据实际情况查看系统情况",
            level: "中风险",
            id: "linux.eof",
            effect: effect,
            name: "系统版本生命周期检查",
            category: "系统健康检查",
            actual: "该系统不是centos或redhat",
            expected: "系统版本处于产品生命周期内"
        })
        return { results: results }
    }


})(input)