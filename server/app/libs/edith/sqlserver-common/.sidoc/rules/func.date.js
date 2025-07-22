; (function (params) {
    dt = new Date(Date.now()).toLocaleString()
    dtArr = dt.split(",")[0].split("/")
    return dtArr[2]+"-" + dtArr[0] + "-" + dtArr[1]
})(input)