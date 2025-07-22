;(function (params) {
    str = params[0]
    if (typeof (str) === "string") {
        var num = str.replace(/[^0-9]/g, '');
        return num
    } else {
        return str
    }
})(input)