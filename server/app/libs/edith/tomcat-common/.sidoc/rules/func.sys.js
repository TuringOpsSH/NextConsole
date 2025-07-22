; (function (params) {
    input = params[0];
    WlsStatus = input.WlsStatus;
    WlsConfs = input.WlsConfs;
    WlsLogs = input.WlsLogs;
    SysStatus = input.SysStatus;
    SysConfs = input.SysConfs;
    //定义一个wls接收数据的对象
    wlsdata = {};
    //定义wls对象中的中间件个数sum,每个wls都有一个wlsConfs
    wlsdata.sum = input.WlsConfs.length;
    wlsdata.ip = [];
    wlsdata.os = [];
    wlsdata.cpucount = [];
    wlsdata.mem = [];
    wlsdata.cpuused = [];
    wlsdata.memused = [];
    wlsdata.diskused = [];
    wlsdata.wlsversion = [];
    wlsdata.patch = [];
    wlsdata.jdk = [];
    wlsdata.installdir = [];
    wlsdata.domaindir = [];
    wlsdata.server = [];
    wlsdata.jdbc = [];
    wlsdata.jvm = [];
    wlsdata.cpunum = {};
    wlsdata.memnum = {};
    wlsdata.disknum = {};

    serversname = [];
    //循环多个中间件的数据，加入wlsdata对象中
    for (i = 0; i < wlsdata.sum; i++) {
        wlsdata.ip.push(SysConfs[i].ip[0])
        wlsdata.os.push(SysConfs[i].base.Distro)
        wlsdata.cpucount.push(SysConfs[i].base.CPUs)
        wlsdata.mem.push((parseInt((SysConfs[i].mem.total) / 1024 / 1024)).toString() + "MB")
        wlsdata.cpuused.push((parseInt(SysStatus[i].cpupct[0].metric).toString() + "%"))
        wlsdata.memused.push((parseInt(SysConfs[i].mem.usedPercent).toString() + "%"))
        for (j = 0; j < SysConfs[i].disk.length; j++) {
            if ((SysConfs[i].disk[j].path) == "/") {
                wlsdata.diskused.push((parseInt(SysConfs[i].disk[j].usedPercent).toString() + "%"))
            }
        }
        
        wlsdata.wlsversion.push(WlsConfs[i].domain.version)

        if ((WlsConfs[i].domain.version) == "10.3.6.0") {
            wlsdata.patch.push(WlsConfs[i].wlsConfRest.bsuRecord.PatchID)

        } else {
            wlsdata.patch.push(WlsConfs[i].wlsConfRest.patchRecord.LocalMachineInformation.Patch[0].PatchId)
        }

        wlsdata.jdk.push(WlsConfs[i].wlsConfRest.jdkVersion)


        //需要取到命令行的json中，dengjson更新

        // wlsdata.installdir.push(((WlsConfs[i].edith.command).split("-d")[1]).split("-")[0])
        // wlsdata.domaindir.push(((WlsConfs[i].edith.command).split("-d")[1]).split("-")[0])


        //server名统计
        var domainname = [];
        for (q = 0; q < (WlsStatus[i].servers.length); q++) {

            domainname.push(WlsStatus[i].servers[q].Name)


        }
        wlsdata.server.push(domainname)
        domainname.splice(0);

        //添加JDBC连接数
        if (!WlsConfs[i].jdbcFiles.err) {
            wlsdata.jdbc.push(WlsConfs[i].jdbcFiles[0].connectionPool.max)
        } else {
            wlsdata.jdbc.push("空")
        }


        //系统信息检查

      

        if (parseInt(SysStatus[i].cpupct[0].metric) > 80){
            wlsdata.cpunum[(SysConfs[i].ip[0])] = (parseInt(SysStatus[i].cpupct[0].metric).toString() + "%")
        }

        if (parseInt(SysConfs[i].mem.usedPercent) > 80){
            wlsdata.memnum[(SysConfs[i].ip[0])] = (parseInt(SysConfs[i].mem.usedPercent).toString() + "%")
        }


        for (j = 0; j < SysConfs[i].disk.length; j++) {
            if ((SysConfs[i].disk[j].path) == "/") {

                if (parseInt(SysConfs[i].disk[j].usedPercent) > 80){
                    wlsdata.disknum[(SysConfs[i].ip[0])] = (parseInt(SysConfs[i].disk[j].usedPercent).toString() + "%")
                }
            }
        }


    }






    // wlsdata.ip = WlsStatus.servers[0].Name



    return wlsdata
})(input)