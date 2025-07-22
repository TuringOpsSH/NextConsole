; (function (params) {
    byte_number = Number(params);
    mb = Math.round(byte_number / 1024 / 1024);
    return mb;
})(input)