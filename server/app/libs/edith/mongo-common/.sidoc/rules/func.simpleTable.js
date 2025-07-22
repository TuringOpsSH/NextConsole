;(function (params) {
    let tmp;
    const args1 = params[1];
    const args2 = params[2];
    const data = params[0]

    if (data.length == 0) {
        return ""
    }


    let head = [];
    let title = [];
    let headNew = [];
    const body = [];
    let result = "";
    let maxLength = 0;
    if (args1 == "*") {
        for (let i = 0; i < data.length; i++) {
            if (Object.keys(data[i]).length > maxLength) {
                maxLength = data[i].length
            }
            head = Object.keys(data[i])
            title = head
        }
    } else {
        head = args1.split(",")
        title = args1.split(",")
        for (let i = 0; i < head.length; i++) {
            head[i] = head[i].trim()
        }
        if (args2 != "*" && args2 != "") {
            headNew = args2.split(",")
            for (let i = 0; i < headNew.length; i++) {
                tmp = headNew[i].split(":");
                const index = head.indexOf(tmp[0]);
                if (index != -1) {
                    title[index] = tmp[1]
                }
            }
        }
    }

    for (let i = 0; i < data.length; i++) {
        tmp = {};
        for (let j = 0; j < head.length; j++) {
            tmp[head[j]] = data[i][head[j]]
        }
        body.push(tmp)
    }

    result += "|"

    for (let i = 0; i < title.length; i++) {
        result += " " + title[i] + " |"
    }

    result += "\n|"

    for (let i = 0; i < head.length; i++) {
        result += ":---|"
    }

    for (let i = 0; i < body.length; i++) {
        result += "\n"
        result += "|"
        for (let j = 0; j < head.length; j++) {
            result += " " + body[i][head[j]] + " |"
        }

    }

    return result

})(input)
