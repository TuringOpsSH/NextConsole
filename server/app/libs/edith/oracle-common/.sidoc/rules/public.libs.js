;function byte2mb(params) {
    byte_number = Number(params);
    mb = Math.round(byte_number / 1024 / 1024);
    return mb;
};

function copy(obj){
    var objCopy = {};
    for(var key in obj){
        objCopy[key] = obj[key];
    }
    return objCopy;
};