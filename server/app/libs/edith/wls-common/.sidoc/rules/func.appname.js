; (function (params) {
    hostname = params[0];
    appnames = {}
    if (params.length >= 2) {
        appnames = params[1];
    }

    appname = ""

    if (hostname.match("|")) {
        hostname = hostname.split("|")[0]
    }

    if (!appnames) {
        appname = hostname.toUpperCase() + "应用"
    } else {
        if (appnames.hasOwnProperty(hostname)) {
            appname = appnames[hostname]
        } else {
            appname = hostname.toUpperCase() + "应用"
        }
    }

    return appname
})(input)