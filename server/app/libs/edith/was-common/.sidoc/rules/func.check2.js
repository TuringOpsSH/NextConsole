; (function (params) {
    try {
        if (params[0].hasOwnProperty("err")) {
            return "err"
        } else {
            return "ok"
        }
    } catch (error) {
        return "ok"
    }
})(input)