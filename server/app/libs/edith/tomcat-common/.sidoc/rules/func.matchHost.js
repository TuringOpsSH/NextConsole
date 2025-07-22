; (function (params) {
    input = params[0];


    allsyslist = {};

    SysStatus = input.SysStatus;
    SysConfs = input.SysConfs;

    TomcatConfs = input.TomcatConfs;
    TomcatStatus = input.TomcatStatus;
    WlsStatus = input.WlsStatus;
    WlsConfs = input.WlsConfs;
    WlsLogs = input.WlsLogs;
    WasConfs = input.WasConfs;
    WasStatus = input.SysStatus;

    syssum = SysConfs.length;
    wlssum = WlsConfs.length;
    wassum = WasConfs.length;
    tomcatsum = TomcatConfs.length;


    for (i = 0; i < syssum; i++) {

        allsyslist[SysConfs[i].host.hostname] = {}
        allsyslist[SysConfs[i].host.hostname].SysConfs = SysConfs;
        allsyslist[SysConfs[i].host.hostname].SysStatus = SysStatus;

        if (wlssum > 0) {
            allsyslist[SysConfs[i].host.hostname].WlsStatus = WlsStatus;
            allsyslist[SysConfs[i].host.hostname].WlsConfs = WlsConfs;
            allsyslist[SysConfs[i].host.hostname].WlsLogs = WlsLogs;
        }
        if (wassum > 0) {
            allsyslist[SysConfs[i].host.hostname].WasConfs = WasConfs;
            allsyslist[SysConfs[i].host.hostname].WasStatus = WasStatus;

        }
        if (input.WlsConfs.length > 0) {
            allsyslist[SysConfs[i].host.hostname].TomcatConfs = TomcatConfs;
            allsyslist[SysConfs[i].host.hostname].TomcatStatus = TomcatStatus;
        }
    }


return allsyslist


})(input)

