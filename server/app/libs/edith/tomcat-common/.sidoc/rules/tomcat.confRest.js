;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.webConf",
        name: "tomcat版本和Jvm参数信息",
        mixraw: [],
        raw: {
            javaVersion: "",
            tomcatVersion: "",
            jvmParam:{}
        },
        actual: "",
        expected: "",
        category: "配置检查",
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
    result.raw.javaVersion = raw.javaVersion
    result.raw.tomcatVersion = raw.tomcatVersion
    result.raw.jvmParam=copy(raw.jvmParam)

    results.push(result)
    return {results: results}
})(input)
