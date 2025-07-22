function copy(obj){
    var objCopy = {};
    for(var key in obj){
        objCopy[key] = obj[key];
    }
    return objCopy;
};

;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.host",
        name: "",
        mixraw: [],
        raw: {
            hostname: "",
            uptime: 0,
            bootTime: 0,
            procs: 0,
            os: "",
            platform: "",
            platformFamily: "",
            platformVersion: "",
            kernelVersion: "",
            kernelArch: "",
            virtualizationSystem: "",
            virtualizationRole: "",
            hostId: ""
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

    result.raw = copy(raw)

    results.push(result)
    return {results: results}
})(input)
