; appnames = {
    // evodb: "DB应用系统",
    // hst124: "A应用系统",
    // hst125: "A应用系统",
    // hst141: "A应用系统",
    // orafs10205: "AFS应用系统"
}

; (function (params) {
    hostname = params[0];
    appname = ""

    if (appnames.hasOwnProperty(hostname)) {
        appname = appnames[hostname]
    } else {
        appname = hostname.toUpperCase() + "应用"
    }

    appname = appname.replace(/\|/g, "");
    return appname
})(input)
