function copy(obj){
    var objCopy = {};
    for(var key in obj){
        objCopy[key] = obj[key];
    }
    return objCopy;
};