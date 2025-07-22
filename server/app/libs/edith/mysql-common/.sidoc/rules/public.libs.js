;

function byte2mb(params) {
    byte_number = Number(params);
    mb = Math.round(byte_number / 1024 / 1024);
    return mb;
};

function copy(obj) {
    var objCopy = {};
    for (var key in obj) {
        objCopy[key] = obj[key];
    }
    return objCopy;
};


function mysqlVersion(currentVersion, minVersion) {
    var currentVersionCode = currentVersion.split(".")
    var minVersionCode = minVersion.split(".")

    var currentVersionValue = 0
    var minVersionValue = 0

    var num = 10000
    for (var i = currentVersionCode.length - 1; i >= 0; i--) {
        currentVersionValue += currentVersionCode[currentVersionCode.length - i -1] * num
        num = num/100
    }

    num = 10000
    for (var j = minVersionCode.length - 1; j >= 0; j--) {
        minVersionValue += minVersionCode[minVersionCode.length - j -1] * num
        num = num/100
    }

    return currentVersionValue >= minVersionValue
};
