; (function (params) {

    input = params[0];

    SysStatus = input.SysStatus;
    SysConfs = input.SysConfs;

    WasConfs = input.WasConfs;
    


    wasproblems = {};
    //创建多个主机对象
    syssum = SysConfs.length;
    //计算有几对wls的domain
    wassum = WasConfs.length;

    for (i = 0; i < syssum; i++) {

        wasproblems[SysConfs[i].host.hostname] = {};
        wasproblems[SysConfs[i].host.hostname].SysMsg = {};
        wasproblems[SysConfs[i].host.hostname].TomcatMsg = {};

        //sysconf中数据
        wasproblems[SysConfs[i].host.hostname].SysMsg.ip = SysConfs[i].ip[0]
        wasproblems[SysConfs[i].host.hostname].SysMsg.cpus = SysConfs[i].base.CPUs
        wasproblems[SysConfs[i].host.hostname].SysMsg.os = SysConfs[i].base.Distro
        wasproblems[SysConfs[i].host.hostname].SysMsg.mem = (parseInt((SysConfs[i].mem.total) / 1024 / 1024)).toString() + "MB"
        wasproblems[SysConfs[i].host.hostname].SysMsg.memused = (parseInt(SysConfs[i].mem.usedPercent).toString() + "%")

        //a为disk列表
        for (a = 0; a < SysConfs[i].disk.length; a++) {
            if ((SysConfs[i].disk[a].path) == "/") {
                wasproblems[SysConfs[i].host.hostname].SysMsg.diskused = ((parseInt(SysConfs[i].disk[a].usedPercent).toString() + "%"))
            }
        }


        //sysstatus中数据
        //b为sysstatus列表
        for (b = 0; b < syssum; b++) {
            if ((SysConfs[i].host.hostname) == (SysStatus[b].host.hostname)) {
                wasproblems[SysConfs[i].host.hostname].SysMsg.cpuused = (parseInt(SysStatus[b].cpupct[0].metric).toString() + "%")
            }


            // wlspsef = [];
            // psefnum = SysStatus[b].psef[0].metric.length;
            // //c为os-psef进程信息
            // for (c = 0; c < psefnum; c++) {

            //     if (SysStatus[b].psef[0].metric[c].indexOf("weblogic.Server") > 0) {

            //         wlspsef.push("-Xms" + SysStatus[b].psef[0].metric[c].split("-Xms")[1].split(" ")[0])
            //         wlspsef.push("-Xmx" + SysStatus[b].psef[0].metric[c].split("-Xmx")[1].split(" ")[0])
            //         // if (SysStatus[i].psef[0].metric[c].indexOf("-XX:+PrintGC") > 0) {
            //         //     wlspsef.gc = "有GC参数"
            //         // }
            //         // if (SysStatus[i].psef[0].metric[c].indexOf("-XX:HeapDumpPath=") > 0) {
            //         //     wlspsef.heapdump = "有HeapDump参数"
            //         // }              
            //     }
            // }
            // wasproblems[SysConfs[i].host.hostname].SysMsg.psArgs = wlspsef
        }



        for (d = 0; d < wassum; d++) {
            if ((SysConfs[i].host.hostname) == (WasConfs[d].port.hostname)) {
                wasproblems[SysConfs[i].host.hostname].TomcatMsg[WasConfs[d].serverConf.serverport] = {};
                wasproblems[SysConfs[i].host.hostname].TomcatMsg[WasConfs[d].serverConf.serverport].version = WasConfs[d].versions.tomcatVersion
                wasproblems[SysConfs[i].host.hostname].TomcatMsg[WasConfs[d].serverConf.serverport].jdk = WasConfs[d].versions.javaVersion
                wasproblems[SysConfs[i].host.hostname].TomcatMsg[WasConfs[d].serverConf.serverport].home = WasConfs[d].flags.path

            }
        }

    }
    return wasproblems


})(input)  