;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.serverConf",
        name: "",
        mixraw: [],
        raw: {
            resources: [],
            serverport: "",
            services: [],
            shutdown: "",
            port:""
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
    result.raw.resources = raw.resources
    result.raw.serverport = raw.serverport
    result.raw.services = raw.services
    result.raw.shutdown = raw.shutdown
    result.raw.port=raw.services[0].connectors[0].port
    results.push(result)
    return {results: results}
})(input)
