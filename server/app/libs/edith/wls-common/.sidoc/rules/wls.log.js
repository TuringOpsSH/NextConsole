; (function (input) {

    var problemPrefix = "wls.log."


    var errResults = {
        "BEA-170011": {
            desc: "LogBroadcaster无法传递日志",
            effect: "可能是Admin Server离线造成",
            solution: "请检查Admin Server状态",
            level: "high",
            id: problemPrefix + "BEA-170011",
            name: "LogBroadcaster无法传递日志",
        },
        "BEA-110503": {
            desc: "JTA备份不存在",
            effect: "可能是Admin Server离线造成",
            solution: "请检查Admin Server状态",
            level: "high",
            id: problemPrefix + "BEA-110503",
            name: "JTA备份不存在",
        },
        "BEA-001112": {
            desc: "JDBC连接测试失败",
            effect: "数据库连接池可能无法工作",
            solution: "请检查数据库状态或数据库配置",
            level: "high",
            id: problemPrefix + "BEA-001112",
            name: "JDBC连接测试失败",
        },
        "BEA-000123": {
            desc: "重复绑定JNDI失败",
            effect: "会影响系统性能",
            solution: "请开发商检查配置或代码，避免此类操作",
            level: "low",
            id: problemPrefix + "BEA-000123",
            name: "重复绑定JNDI失败",
        },
        "BEA-000000": {
            desc: "无法连接到 Admin Server",
            effect: "Admin Server可能已经关闭",
            solution: "对业务一般无影响，检查Admin Server状态",
            level: "low",
            id: problemPrefix + "BEA-000000",
            name: "无法连接到 Admin Server",
        },
        "BEA-310003": {
            desc: "剩余空间Heap已经极少",
            effect: "说明存在内存泄漏或者堆大小设置过小",
            solution: "需要深入分析Heap满的原因",
            level: "high",
            id: problemPrefix + "BEA-310003",
            name: "HEAP紧张警告",
        },
        "BEA-149617": {
            desc: "UDDI应用部署错误",
            effect: "无",
            solution: "无",
            level: "none",
            id: problemPrefix + "BEA-149617",
            name: "UDDI应用部署错误",
        },
        "BEA-101020": {
            desc: "HTTP模块遇到了应用错误",
            effect: "应用部分功能受到影响，如果数量不多可以忽略",
            solution: "需要参考详细日志做出判断",
            level: "low",
            id: problemPrefix + "BEA-101020",
            name: "HTTP模块应用错误",
        },
        "BEA-101017": {
            desc: "HTTP模块遇到了应用错误",
            effect: "应用部分功能受到影响，如果数量不多可以忽略",
            solution: "需要参考详细日志做出判断",
            level: "low",
            id: problemPrefix + "BEA-101017",
            name: "HTTP模块应用错误",
        },
        "BEA-100026": {
            desc: "HTTP Session模块遇到了未知的错误，通常是较为严重的底层错误",
            effect: "可能会影响系统正常运行",
            solution: "需要参考详细日志做出判断",
            level: "normal",
            id: problemPrefix + "BEA-100026",
            name: "HTTP Session模块未知错误",
        },
        "BEA-080004": {
            desc: "RMI模块遇到了未知的错误，通常是较为严重的底层错误",
            effect: "可能会影响系统正常运行",
            solution: "需要参考详细日志做出判断",
            level: "low",
            id: problemPrefix + "BEA-080004",
            name: "RMI模块未知错误",
        },
        "BEA-002608": {
            desc: "Server模块遇到了未知的错误，通常是较为严重的底层错误",
            effect: "可能会影响系统正常运行",
            solution: "需要参考详细日志做出判断",
            level: "normal",
            id: problemPrefix + "BEA-002608",
            name: "Server模块未知错误",
        },
        "BEA-000802": {
            desc: "HTTP模块遇到了未知的错误，通常是较为严重的底层错误",
            effect: "可能会影响系统正常运行",
            solution: "需要参考详细日志做出判断",
            level: "normal",
            id: problemPrefix + "BEA-000802",
            name: "HTTP模块未知错误",
        },
        "BEA-000421": {
            desc: "Socket模块遇到了未知的错误，通常是较为严重的底层错误",
            effect: "可能会影响系统正常运行",
            solution: "需要参考详细日志做出判断",
            level: "normal",
            id: problemPrefix + "BEA-000421",
            name: "Socket模块未知错误",
        },

        "BEA-000337": {
            desc: "请求执行超过了600秒",
            effect: "会影响系统性能，出现过多会造成线程积压",
            solution: "一般是应用问题，需要开发商检查相应的代码",
            level: "high",
            id: problemPrefix + "BEA-000337",
            name: "请求执行超过了600秒",
        },
        "BEA-090153": {
            desc: "生产模式中使用了demo证书",
            effect: "存在一定的安全隐患",
            solution: "使用自定义证书",
            level: "low",
            id: problemPrefix + "BEA-090153",
            name: "生产模式中使用了demo证书",
        },
        "BEA-090152": {
            desc: "生产模式中使用了demo的信任证书",
            effect: "存在一定的安全隐患",
            solution: "使用自定义证书",
            level: "low",
            id: problemPrefix + "BEA-090152",
            name: "生产模式中使用了demo的信任证书",
        },
        "BEA-000449": {
            desc: "因没有读到数据，关闭了Socket端口",
            effect: "如果过多，会影响一定的性能",
            solution: "如果不是很多，可以不做处理",
            level: "low",
            id: problemPrefix + "BEA-000449",
            name: "因没有读到数据，关闭了Socket端口",
        },
        "BEA-149506": {
            desc: "建立了与其他Server的JMX连接",
            effect: "轻微影像性能",
            solution: "如果不是很多，可以不做处理",
            level: "low",
            id: problemPrefix + "BEA-149506",
            name: "建立了与其他Server的JMX连接",
        },
        "BEA-141274": {
            desc: "命令行设置的生产模式替代了config.xml的设置",
            effect: "简单的提示",
            solution: "建议在配置中修改为生产模式，避免此警告的出现",
            level: "low",
            id: problemPrefix + "BEA-141274",
            name: "命令行设置的生产模式替代了config.xml的设置",
        },
        "BEA-002611": {
            desc: "主机名localhost映射到了多个IP",
            effect: "可能会影响部分功能",
            solution: "如果未影响业务，可以暂不处理",
            level: "low",
            id: problemPrefix + "BEA-002611",
            name: "主机名localhost映射到了多个IP",
        },
        "BEA-003101": {
            desc: "修改了AdminServer的非动态属性",
            effect: "非动态属性在服务器处于运行状态时被更新。",
            solution: "重新启动管理服务器，以便属性生效。",
            level: "low",
            id: problemPrefix + "BEA-003101",
            name: "修改了AdminServer的非动态属性",
        },
        "BEA-141238": {
            desc: "一个影响服务器的非动态更改",
            effect: "对配置所做的一个或多个更改影响非动态设置",
            solution: "为了使用更改，必须重新启动托管服务器",
            level: "low",
            id: problemPrefix + "BEA-141238",
            name: "一个影响服务器的非动态更改",
        },
        "BEA-141239": {
            desc: "一个影响服务器的非动态更改",
            effect: "对配置所做的一个或多个更改影响非动态设置",
            solution: "这可能需要重新部署或重新启动已配置的实体",
            level: "low",
            id: problemPrefix + "BEA-141239",
            name: "一个影响服务器的非动态更改",
        },
        "BEA-149513": {
            desc: "JMX连接器服务器停止",
            effect: "正常操作",
            solution: "无需处理",
            level: "low",
            id: problemPrefix + "BEA-149513",
            name: "JMX连接器服务器停止",
        },
        "BEA-000503": {
            desc: "读取RJVM请求数据头失败",
            effect: "监控工具相关的错误，可能会影响部分监控功能",
            solution: "一般不影响业务，可以暂不处理",
            level: "low",
            id: problemPrefix + "BEA-000503",
            name: "读取RJVM请求数据头失败",
        },
        "BEA-141277": {
            desc: "使用-Dcom.sun.management.jmxremote或JRockit的-XManagement启动参数引起",
            effect: "可能会影响监控功能",
            solution: "如果未影响业务，可以暂不处理。也可以增加-Djavax.management.builder.initial=weblogic.management.jmx.mbeanserver.WLSMBeanServerBuilder启动参数解决",
            level: "low",
            id: problemPrefix + "BEA-141277",
            name: "MBeanServer的启动缺乏安全基础架构的支持",
        }
    }
    errResult = errResults[input.code]
    if (errResult == undefined) {
        return {
            results: [
                {
                    desc: "未知",
                    effect: "未知",
                    solution: "未知",
                    level: "low",
                    id: problemPrefix + input.code,
                    name: "未定义错误",
                    log: input,
                    code: input.code,
                }
            ]
        }
    } else {
        if (errResult.level == "none") {
            return { results: [] }
        } else {
            errResult["code"] = input["code"]
            return {
                results: [
                    errResult
                ]
            }
        }

    }

})(input)