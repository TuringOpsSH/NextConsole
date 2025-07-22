; (function (input) {
    var results = []
    var result = {
        desc: "检查ORA-, WARNING, TNS-, corrupted, Deadlock, timeout, abnormal, terminated, offline等关键字",
        effect: "根据日志信息具体分析",
        solution: "根据日志信息具体分析",
        level: "正常",
        id: "oracle.awkalert",
        name: "Alert 日志检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "近15天无异常Alert 日志",
        category: "系统运行状态",
        family: "log"
    }

    try {
        var reg = new RegExp('\\$', "g")

        if (!input) {
            return { results: [result] }
        }

        try {
            raw = input.replace(reg, "\\\$").split("\n")
        } catch (err) {
            raw = input["content"] // windows AlertLog3000
        }

        if (!raw) {
            return { results: [result] }
        }

        newraw = []
        /*var reg1 = new RegExp('-', "g")
        var reg2 = /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d./;
        var regExp = new RegExp(reg2);
        lastline = raw[raw.length - 1]
        if (regExp.test(lastline)) {
            start = Number(lastline.split("T")[0].replace(reg1, "")) - 15 //取最近15天
            for (i = 0; i < raw.length; i++) {
                now = Number(raw[i].split("T")[0].replace(reg1, ""))
                if (now >= start) {
                    newraw.push(raw[i])
                }
            }
        } else {
            newraw = raw
        }*/
		
		// 定义两个用于匹配可能日期格式的正则表达式
		const isoRegEx = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/;
		const verboseRegEx = /\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}/;

		if (raw.length > 0) {
			// 尝试匹配最后一个元素中的日期,改成当前日期
			let lastLineDate = new Date();
			
			// 计算15天前的日期
			let date15DaysAgo = new Date(lastLineDate.getTime());
			date15DaysAgo.setDate(lastLineDate.getDate() - 15);

			newraw = raw.filter((line, i) => {
				let lineDateStr = line.match(isoRegEx) || line.match(verboseRegEx);
				if (lineDateStr) {
					let lineDate = new Date(lineDateStr[0]);
					
					// 对于verbose格式的额外处理
					if (!lineDate.getTime()) {
						const pieces = lineDateStr[0].split(' ');
						lineDate = new Date(`${pieces[1]} ${pieces[2]}, ${pieces[4]} ${pieces[3]}`);
					}
					
					return lineDate >= date15DaysAgo;
				}
				return false;
			});
		}
		

        for (i = 0; i < newraw.length; i++) {
            fields = {
                event: "",
                mixlevel: ""
            }
            fields["event"] = newraw[i]

            // Check fields, reset mixlevel and result.level here:

            // fields["event"] //string
            if (fields["event"].match("ORA-") || fields["event"].match("WARNING") ||
                fields["event"].match("TNS-") || fields["event"].match("corrupted") ||
                fields["event"].match("Deadlock") || fields["event"].match("timeout") ||
                fields["event"].match("abnormal") || fields["event"].match("terminated") ||
                fields["event"].match("offline")) {
                fields["mixlevel"] = "中风险"
                result.level = "中风险"
            }
            result.mixraw.push(fields)
        }


    } catch (err) {
        $.print("[Error] oracle.awkalert", err.message)
        result.actual = "近15天无异常Alert 日志或未采集到相关数据"
    }

    if (result.level == "中风险") {
        result.actual = "存在ORA-, WARNING, TNS-, corrupted, Deadlock, timeout, abnormal, terminated, offline相关告警日志"
    } else {
        if (result.actual == "") {
            result.actual = "近15天无异常Alert 日志"
        }
    }

    results.push(result)
    return { results: results }
})(input)
