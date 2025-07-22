; (function (input) {
    var results = []
    var result = {
        desc: "TCP连接情况检查",
        effect: "该规则用于检查TCP连接情况，包括LISTEN、TIME_WAIT和ESTABLISHED状态的连接数。如果连接情况正常，则返回正常状态。",
        solution: "检查TCP连接情况，确保LISTEN、TIME_WAIT和ESTABLISHED状态的连接数正常。如果连接数异常，则需要进一步排查问题。",
        level: "正常",
        id: "win.conns",
        name: "TCP连接情况检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "TCP连接情况正常",
        category: "系统健康检查",
        family: "status"
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

    var listen = 0
    var time_wait = 0
    var established = 0
    for (i = 0; i < raw.length; i++) {
        fields = raw[i]
        if (fields["status"] == "LISTEN") {
            listen += 1
        }
        else if (fields["status"] == "TIME_WAIT") {
            time_wait += 1
        }
        else if (fields["status"] == "ESTABLISHED") {
            established += 1
        }
    }

    result.mixraw.push({
        "listen": listen,
        "time_wait": time_wait,
        "established": established,
        "mixlevel": "正常"
    })
    results.push(result)
    return { results: results }

})(input)
