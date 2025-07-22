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


function OrderByNum(objArr) {
    var arr = []
    for (var i = 0; i < objArr.length; i++) {
        arr.push(objArr[i]["num"])
    }
    arr.sort(function (a, b) {
        return a - b//正序
    })
    var res = []
    for (var i = 0; i < arr.length; i++) {
        flag = arr[i]
        for (var i2 = 0; i2 < objArr.length; i2++) {
            if (objArr[i2]["num"]==flag){
                res.push(objArr[i2])
                break
            }
        }
    }
    return res;
};