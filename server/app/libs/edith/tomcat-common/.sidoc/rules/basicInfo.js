;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "basicInfo",
        name: "Tomcat基本信息",
        mixraw: [],
        raw: {
            Arch:"",
            CPUs: "",
            Distro: "",
            TotalMemory: ""
        },
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }
    if (!raw) {
        return {results: [result]}
    }
    result.raw.Arch = raw.Arch
    result.raw.CPUs = raw.CPUs
    result.raw.Distro = raw.Distro
    result.raw.TotalMemory = raw["Total Memory"]
    results.push(result)
    return {results: results}
})(input)
