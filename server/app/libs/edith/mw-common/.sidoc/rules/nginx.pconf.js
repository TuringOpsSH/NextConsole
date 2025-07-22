function createRaw(key, v) {
    var r = {}
    r[key] = v
    return r
}

;(function (input) {
    var results = []
    if (!input) {
        for (var i = 0; i < 20; i++) {
            var result = {
                desc: "",
                effect: "",
                solution: "需要具体分析",
                level: "低风险",
                id: "",
                name: "",
                mixraw: [],
                raw: [],
                actual: "",
                expected: "",
                category: "",
                family: "conf"
            }
            switch (i) {
                case 0:
                    result.desc = ""
                    result.expected = "不能为root、nobody和null"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "worker_user"
                    result.category = "全局配置参数检查"
                    result.name = "Worker启动用户"
                    results.push(result)
                    break
                case 1:
                    result.desc = ""
                    result.expected = "等于CPU逻辑核数"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "worker_processes"
                    result.category = "全局配置参数检查"
                    result.name = "Worker启动进程数"
                    results.push(result)
                    break
                case 2:
                    result.desc = ""
                    result.expected = "logs/access.log"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "access_log_strategy"
                    result.category = "全局配置参数检查"
                    result.name = "Access日志策略"
                    results.push(result)
                    break
                case 3:
                    result.desc = ""
                    result.actual = "未发现相关记录"
                    result.expected = "logs/access.log"
                    result.id = "nginx.pconf." + "error_log_strategy"
                    result.category = "全局配置参数检查"
                    result.name = "Error日志策略"
                    results.push(result)
                    break
                case 4:
                    result.desc = ""
                    result.actual = "未发现相关记录"
                    result.expected = "logs/nginx.pid"
                    result.id = "nginx.pconf." + "pid_path"
                    result.category = "全局配置参数检查"
                    result.name = "pid存放目录"
                    results.push(result)
                    break
                case 5:
                    result.desc = ""
                    result.expected = "1024"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "worker_connections"
                    result.category = "全局配置参数检查"
                    result.name = "每个Worker的最大连接数"
                    results.push(result)
                    break
                case 6:
                    result.actual = "未发现相关记录"
                    result.desc = ""
                    result.expected = "off"
                    result.id = "nginx.pconf." + "multi_accept"
                    result.category = "全局配置参数检查"
                    result.name = "一次接收一个新连接"
                    results.push(result)
                    break
                case 7:
                    result.desc = ""
                    result.actual = "未发现相关记录"
                    result.expected = "application/octet-stream"
                    result.id = "nginx.pconf." + "default_type"
                    result.category = "HTTP参数配置检查"
                    result.name = "默认媒体类型"
                    results.push(result)
                    break
                case 8:
                    result.desc = ""
                    result.expected = "off"
                    result.id = "nginx.pconf." + "server_tokens"
                    result.actual = "未发现相关记录"
                    result.category = "HTTP参数配置检查"
                    result.name = "版本隐藏"
                    results.push(result)
                    break
                case 9:
                    result.desc = ""
                    result.expected = "on"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "sendfile"
                    result.category = "HTTP参数配置检查"
                    result.name = "高效传输模式"
                    results.push(result)
                    break
                case 10:
                    result.desc = ""
                    result.actual = "未发现相关记录"
                    result.expected = "off"
                    result.id = "nginx.pconf." + "tcp_nopush"
                    result.category = "HTTP参数配置检查"
                    result.name = "tcp_nopush"
                    results.push(result)
                    break
                case 11:
                    result.desc = ""
                    result.expected = "off"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "tcp_nodelay"
                    result.category = "HTTP参数配置检查"
                    result.name = "禁用Nagle算法"
                    results.push(result)
                    break
                case 12:
                    result.desc = "keepalive_timeout"
                    result.expected = "75s"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "keepalive_timeout"
                    result.category = "HTTP参数配置检查"
                    result.name = "keepalive_timeout"
                    results.push(result)
                    break
                case 13:
                    result.desc = ""
                    result.expected = "30s"
                    result.id = "nginx.pconf." + "resolver_timeout"
                    result.actual = "未发现相关记录"
                    result.category = "HTTP参数配置检查"
                    result.name = "resolver_timeout"
                    results.push(result)
                    break
                case 14:
                    result.desc = ""
                    result.expected = "off"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "autoindex"
                    result.category = "HTTP参数配置检查"
                    result.name = "目标列表策略"
                    results.push(result)
                    break
                case 15:
                    result.desc = ""
                    result.expected = "off"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "proxy_cache_path"
                    result.category = "HTTP参数配置检查"
                    result.name = "打开文件缓存"
                    results.push(result)
                    break
                case 16:
                    result.actual = "未发现相关记录"
                    result.desc = ""
                    result.expected = "0"
                    result.id = "nginx.pconf." + "through_directory"
                    result.category = "Location配置检查"
                    result.name = "目录穿透"
                    results.push(result)
                    break
                case 17:
                    result.desc = ""
                    result.expected = "none"
                    result.actual = "未发现相关记录"
                    result.id = "nginx.pconf." + "proxy_pass"
                    result.category = "Location配置检查"
                    result.name = "proxy_pass指令后禁止直接使用域名进行转发"
                    results.push(result)
                    break
                case 18:
                    result.desc = ""
                    result.actual = "未发现相关记录"
                    result.expected = "none"
                    result.id = "nginx.pconf." + "fast_cgi"
                    result.category = "Fast-cgi配置检查"
                    result.name = "fast_cgi"
                    results.push(result)
                    break
                case 19:
                    result.actual = "未发现相关记录"
                    result.desc = ""
                    result.expected = "0"
                    result.id = "nginx.pconf." + "stream"
                    result.category = "Stream配置检查"
                    result.name = "是否使用stream模块"
                    results.push(result)
                    break

            }
        }
        return {results: [result]}
    }
    var key = Object.keys(input[0])
    for (var i = 0; i < key.length; i++) {
        var result = {
            desc: "",
            effect: "",
            solution: "需要具体分析",
            level: "低风险",
            id: "nginx.pconf",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "无异常指标",
            category: "指标检查",
            family: "conf"
        }

        var errResult = {
            desc: "",
            effect: "",
            solution: "需要具体分析",
            level: "中风险",
            id: "nginx.pconf",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "无异常指标",
            category: "指标检查",
            family: "conf"
        }
        switch (key[i]) {
            case "worker_user":
                if (input[0][key[i]] != "nobody" && input[0][key[i]] != "root" && !input[0][key[i]]) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "!root and !nobody and !null"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "Worker启动用户"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "不能为root、nobody和null"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "Worker启动用户"
                    results.push(result)
                }
                break
            case "worker_processes":
                if (input[0][key[i]] != input[0]["cpus"]) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "等于CPU逻辑核数"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "Worker启动进程数"
                    results.push(errResult)
                } else {
                    result.actual = input[0][key[i]]
                    result.desc = ""
                    result.expected = "=CPU逻辑核数"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "Worker启动进程数"
                    results.push(result)
                }
                break
            case "access_log_strategy":
                if (!input[0][key[i]].toString().match("/access.log")) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "logs/access.log"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "Access日志策略"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "logs/access.log"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "Access日志策略"
                    results.push(result)
                }
                break
            case "error_log_strategy":
                if (!input[0][key[i]].toString().match("/error.log")) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "logs/error.log"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "Error日志策略"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.actual = input[0][key[i]]
                    result.expected = "logs/access.log"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "Error日志策略"
                    results.push(result)
                }
                break
            case "pid_path":
                if (!input[0][key[i]].toString().match("/nginx.pid")) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "logs/nginx.pid"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "pid存放目录"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.actual = input[0][key[i]]
                    result.expected = "logs/nginx.pid"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "pid存放目录"
                    results.push(result)
                }
                break
            case "worker_connections":
                if (input[0][key[i]] != 1024) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "1024"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "每个Worker的最大连接数"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "1024"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "每个Worker的最大连接数"
                    results.push(result)
                }
                break
            case "multi_accept":
                if (input[0][key[i]] != "off") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "全局配置参数检查"
                    errResult.name = "一次接收一个新连接"
                    results.push(errResult)
                } else {
                    result.actual = input[0][key[i]]
                    result.desc = ""
                    result.expected = "off"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "全局配置参数检查"
                    result.name = "一次接收一个新连接"
                    results.push(result)
                }
                break
            case "default_type":
                if (input[0][key[i]] != "application/octet-stream") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "application/octet-stream"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "默认媒体类型"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.actual = input[0][key[i]]
                    result.expected = "application/octet-stream"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "默认媒体类型"
                    results.push(result)
                }
                break
            case "server_tokens":
                if (input[0][key[i]] != "off") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "版本隐藏"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "off"
                    result.id = "nginx.pconf." + key[i]
                    result.actual = input[0][key[i]]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "版本隐藏"
                    results.push(result)
                }
                break
            case "sendfile":
                if (input[0][key[i]] != "on") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "on"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "高效传输模式"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "on"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "高效传输模式"
                    results.push(result)
                }
                break
            case "tcp_nopush":
                if (input[0][key[i]] != "off") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "tcp_nopush"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.actual = input[0][key[i]]
                    result.expected = "off"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "tcp_nopush"
                    results.push(result)
                }
                break
            case "tcp_nodelay":
                if (input[0][key[i]] != "off") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "禁用Nagle算法"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "off"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "禁用Nagle算法"
                    results.push(result)
                }
                break
            case "keepalive_timeout":
                if (input[0][key[i]] != "75") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "75s"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "keepalive_timeout"
                    results.push(errResult)
                } else {
                    result.desc = "keepalive_timeout"
                    result.expected = "75s"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "keepalive_timeout"
                    results.push(result)
                }
                break
            case "resolver_timeout":
                if (input[0][key[i]] != "30") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "30s"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "resolver_timeout"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "30s"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.actual = input[0][key[i]]
                    result.category = "HTTP参数配置检查"
                    result.name = "resolver_timeout"
                    results.push(result)
                }
                break
            case "autoindex":
                if (input[0][key[i]] != "off") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "目标列表策略"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "off"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "HTTP参数配置检查"
                    result.name = "目标列表策略"
                    results.push(result)
                }
                break
            case "proxy_cache_path":
                if (input[0][key[i]] != "") {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "off"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "HTTP参数配置检查"
                    errResult.name = "打开文件缓存"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "off"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], "off")
                    result.category = "HTTP参数配置检查"
                    result.name = "打开文件缓存"
                    results.push(result)
                }
                break
            case "through_directory":
                if (input[0][key[i]] != false) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "0"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "Location配置检查"
                    errResult.name = "目录穿透"
                    results.push(errResult)
                } else {
                    result.actual = input[0][key[i]]
                    result.desc = ""
                    result.expected = "0"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "Location配置检查"
                    result.name = "目录穿透"
                    results.push(result)
                }
                break
            case "proxy_pass":
                if (input[0][key[i]] != false) {
                    errResult.actual = input[0][key[i]]
                    errResult.desc = ""
                    errResult.expected = "none"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "Location配置检查"
                    errResult.name = "proxy_pass指令后禁止直接使用域名进行转发"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.expected = "none"
                    result.actual = input[0][key[i]]
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "Location配置检查"
                    result.name = "proxy_pass指令后禁止直接使用域名进行转发"
                    results.push(result)
                }
                break
            case "fast_cgi":
                if (input[0][key[i]] != "none" && input[0][key[i]] != "") {
                    errResult.actual = "true"
                    errResult.desc = ""
                    errResult.expected = "none"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "Fast-cgi配置检查"
                    errResult.name = "fast_cgi"
                    results.push(errResult)
                } else {
                    result.desc = ""
                    result.actual = "false"
                    result.expected = "none"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "Fast-cgi配置检查"
                    result.name = "fast_cgi"
                    results.push(result)
                }
                break
            case "stream":
                if (input[0][key[i]] != false) {
                    errResult.desc = ""
                    errResult.actual = input[0][key[i]]
                    errResult.expected = "0"
                    errResult.id = "nginx.pconf." + key[i]
                    errResult.raw = createRaw(key[i], input[0][key[i]])
                    errResult.category = "Stream配置检查"
                    errResult.name = "是否使用stream模块"
                    results.push(errResult)
                } else {
                    result.actual = input[0][key[i]]
                    result.desc = ""
                    result.expected = "0"
                    result.id = "nginx.pconf." + key[i]
                    result.raw = createRaw(key[i], input[0][key[i]])
                    result.category = "Stream配置检查"
                    result.name = "是否使用stream模块"
                    results.push(result)
                }
                break
        }
    }
    return {results: results}
})(input)
