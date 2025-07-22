; (function (input) {
    const data = input[0]
    const result = {};
    let keyList = [];
    let maxLength = 0;

    for (let i = 0; i < data.length; i++) {
        if (Object.keys(data[i]).length > maxLength) {
            maxLength = data[i].length
        }
        keyList = Object.keys(data[i])
    }

    for (let i = 0; i < keyList.length; i++) {
        let col = []
        for (let j = 0; j < data.length; j++) {
            col.push(data[j][keyList[i]])
        }
        result[keyList[i]] = col
    }

    return result
})(input)
