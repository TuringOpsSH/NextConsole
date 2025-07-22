; (function (params) {
    try {
        return params[0]["problems"]
    } catch (err) {
        $.print("Summary err", err.message)
    }

})(input)