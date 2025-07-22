; (function (params) {
    input = params[0];
    //接收每个模块数据
    SysConfs = input.SysConfs;
    WlsConfs = input.WlsConfs;
    WasConfs = input.WasConfs;
    TomcatConfs = input.TomcatConfs;


    syssum = SysConfs.length;
    wlssum = WlsConfs.length;
    wassum = WasConfs.length;
    tomcatsum = TomcatConfs.length;

    syslist = {};
    syslist.wls = {};
    syslist.was = {};
    syslist.tomcat = {};

    if (wlssum > 0) {

        for (i = 0; i < syssum; i++) {

           
            for (q = 0; q < wlssum; q++) {
                if ((SysConfs[i].host.hostname) == (WlsConfs[q].port.hostname)) {
                    syslist.wls[SysConfs[i].host.hostname] = {};
                    syslist.wls[SysConfs[i].host.hostname].hostname = SysConfs[i].host.hostname
                    syslist.wls[SysConfs[i].host.hostname].ip = SysConfs[i].ip[0]
                    syslist.wls[SysConfs[i].host.hostname].os = SysConfs[i].host.os
                    syslist.wls[SysConfs[i].host.hostname].midware = "weblogic"
                    syslist.wls[SysConfs[i].host.hostname].status = "空"
                }
            }
        }
    }


    if (tomcatsum > 0) {

        for (i = 0; i < syssum; i++) {

            
            for (q = 0; q < tomcatsum; q++) {
                if ((SysConfs[i].host.hostname) == (TomcatConfs[q].port.hostname)) {
                    syslist.tomcat[SysConfs[i].host.hostname] = {};

                    syslist.tomcat[SysConfs[i].host.hostname].hostname = SysConfs[i].host.hostname
                    syslist.tomcat[SysConfs[i].host.hostname].ip = SysConfs[i].ip[0]
                    syslist.tomcat[SysConfs[i].host.hostname].os = SysConfs[i].host.os
                    syslist.tomcat[SysConfs[i].host.hostname].midware = "tomcat"
                    syslist.tomcat[SysConfs[i].host.hostname].status = "空"
                }
            }
        }
    }


    if (wassum > 0) {

        for (i = 0; i < syssum; i++) {

           
            for (q = 0; q < wassum; q++) {
                if ((SysConfs[i].host.hostname) == (WasConfs[q].port.hostname)) {
                    syslist.was[SysConfs[i].host.hostname] = {};
                    syslist.was[SysConfs[i].host.hostname].hostname = SysConfs[i].host.hostname
                    syslist.was[SysConfs[i].host.hostname].ip = SysConfs[i].ip[0]
                    syslist.was[SysConfs[i].host.hostname].os = SysConfs[i].host.os
                    syslist.was[SysConfs[i].host.hostname].midware = "was"
                    syslist.was[SysConfs[i].host.hostname].status = "空"
                }
            }
        }
    }

    return syslist


})(input)



// {
//     hst1:{
//         hostname:""
//         ip:""
//         midware:""
//         os:""
//     },
//     hst2:{
//         hostname:""
//         ip:""
//     }
// }