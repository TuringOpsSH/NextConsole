; (function (params) {
  
  input = params[0];
  //接收每个模块数据
  WlsStatus = input.WlsStatus;
  WlsConfs = input.WlsConfs;
  WlsLogs = input.WlsLogs;

  SysStatus = input.SysStatus;
  SysConfs = input.SysConfs;
  //创建weblogic接收数据对象
  wlsproblems = {};


  //默认
  //创建多个主机对象
  syssum = SysConfs.length;
  //计算有几对wls的domain
  wlssum = WlsConfs.length;
  for (i = 0; i < syssum; i++) {

    //创建weblogic数据结构
    wlsproblems[SysConfs[i].host.hostname] = {};
    wlsproblems[SysConfs[i].host.hostname].SysMsg = {};
    wlsproblems[SysConfs[i].host.hostname].DomainName = {};

    //sysconf中数据
    wlsproblems[SysConfs[i].host.hostname].SysMsg.ip = SysConfs[i].ip[0]
    wlsproblems[SysConfs[i].host.hostname].SysMsg.cpus = SysConfs[i].base.CPUs
    wlsproblems[SysConfs[i].host.hostname].SysMsg.os = SysConfs[i].base.Distro
    wlsproblems[SysConfs[i].host.hostname].SysMsg.mem = (parseInt((SysConfs[i].mem.total) / 1024 / 1024)).toString() + "MB"
    wlsproblems[SysConfs[i].host.hostname].SysMsg.memused = (parseInt(SysConfs[i].mem.usedPercent).toString() + "%")

    //a为disk列表
    for (a = 0; a < SysConfs[i].disk.length; a++) {
      if ((SysConfs[i].disk[a].path) == "/") {
        wlsproblems[SysConfs[i].host.hostname].SysMsg.diskused = ((parseInt(SysConfs[i].disk[a].usedPercent).toString() + "%"))
      }
    }


    //sysstatus中数据
    //b为sysstatus列表
    for (b = 0; b < syssum; b++) {
      if ((SysConfs[i].host.hostname) == (SysStatus[b].host.hostname)) {
        wlsproblems[SysConfs[i].host.hostname].SysMsg.cpuused = (parseInt(SysStatus[b].cpupct[0].metric).toString() + "%")
      }


      wlspsef = [];
      psefnum = SysStatus[b].psef[0].metric.length;
      //c为os-psef进程信息
      for (c = 0; c < psefnum; c++) {

        if (SysStatus[b].psef[0].metric[c].indexOf("weblogic.Server") > 0) {

          wlspsef.push("-Xms" + SysStatus[b].psef[0].metric[c].split("-Xms")[1].split(" ")[0])
          wlspsef.push("-Xmx" + SysStatus[b].psef[0].metric[c].split("-Xmx")[1].split(" ")[0])
          // if (SysStatus[i].psef[0].metric[c].indexOf("-XX:+PrintGC") > 0) {
          //     wlspsef.gc = "有GC参数"
          // }
          // if (SysStatus[i].psef[0].metric[c].indexOf("-XX:HeapDumpPath=") > 0) {
          //     wlspsef.heapdump = "有HeapDump参数"
          // }              
        }
      }
      wlsproblems[SysConfs[i].host.hostname].SysMsg.psArgs = wlspsef
    }


    //默认wlsconf个数与wlsstatus个数相同 ，d为循环wlsconf和wlsstatus次数
    for (d = 0; d < wlssum; d++) {

      //wlsconf数据
      if ((SysConfs[i].host.hostname) == (WlsConfs[d].port.hostname)) {
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name] = {};
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].domainpath = WlsConfs[d].flags.domainpath
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].oraclehome = WlsConfs[d].flags.oraclehome
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].version = WlsConfs[d].domain.version

        if ((WlsConfs[d].domain.version) == "10.3.6.0") {
          wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].patch = (WlsConfs[d].wlsConfRest.bsuRecord.PatchID)

        } else {
          wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].patch = (WlsConfs[d].wlsConfRest.patchRecord.LocalMachineInformation.Patch[0].PatchId)
        }
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].jdk = (WlsConfs[d].wlsConfRest.jdkVersion)

        if (!WlsConfs[d].jdbcFiles.err) {
          wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].jdbc = (WlsConfs[d].jdbcFiles[0].connectionPool.max)
        } else {
          wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].jdbc = "空"
        }
      }

      //wlsconf数据
      if ((SysConfs[i].host.hostname) == (WlsStatus[d].port.hostname)) {

        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].oraclehome = WlsStatus[d].flags.oraclehome

        domainname = [];
        //e为循环每个wlsstatus中多个server节点
        for (e = 0; e < (WlsStatus[d].servers.length); e++) {

          domainname.push(WlsStatus[d].servers[e].Name)

        }
        wlsproblems[SysConfs[i].host.hostname].DomainName[WlsConfs[d].domain.name].server = (domainname)
        domainname.splice(0);

      }


    }


  }



  return wlsproblems


})(input)