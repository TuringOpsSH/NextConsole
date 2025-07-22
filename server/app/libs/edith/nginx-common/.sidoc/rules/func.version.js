; (function (params) {
    input = params[0];
    var version = {
        ver: 0,
        v12: "",
        v11: "ok"
    }

    if (input) {
        version.ver = Number(input[0]["instance"]["dbversion"])
        if (version.ver >= 12) {
            version.v12 = "ok"
            version.v11 = ""
        } else {
            version.v12 = ""
            version.v11 = "ok"
        }
    }

    return version
})(input)