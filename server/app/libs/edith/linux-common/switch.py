old="""{
  "checks": [
    {
      "expr": "",
      "rule": "pre.stat",
      "params": []
    },
    {
      "expr": "",
      "rule": "post.stat",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.date",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.appname",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.summary",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.byte2mb",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.orderby",
      "params": []
    },
    {
      "expr": "//SysStatus/*/psaxoZz",
      "rule": "linux.psaxoZz",
      "params": [
        {
          "key": "_scope",
          "value": "psaxoZz"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/bonding",
      "rule": "linux.bonding",
      "params": [
        {
          "key": "_scope",
          "value": "ethbonding"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sysctla",
      "rule": "linux.sysctla",
      "params": [
        {
          "key": "_scope",
          "value": "sysctla"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/psaxoDd",
      "rule": "linux.psaxoDd",
      "params": [
        {
          "key": "_scope",
          "value": "psaxoDd"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/ethtoolS",
      "rule": "linux.ethtoolS",
      "params": [
        {
          "key": "_scope",
          "value": "ethtoolS"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/lspci",
      "rule": "linux.lspci",
      "params": [
        {
          "key": "_scope",
          "value": "lspci"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/ethtooli",
      "rule": "linux.ethtooli",
      "params": [
        {
          "key": "_scope",
          "value": "ethtooli"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/iptables",
      "rule": "linux.iptables",
      "params": [
        {
          "key": "_scope",
          "value": "iptables"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/msglog",
      "rule": "linux.msglog",
      "params": [
        {
          "key": "_scope",
          "value": "msglog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/dmesglog",
      "rule": "linux.dmesglog",
      "params": [
        {
          "key": "_scope",
          "value": "dmesglog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/bootlog",
      "rule": "linux.bootlog",
      "params": [
        {
          "key": "_scope",
          "value": "bootlog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/mcelog",
      "rule": "linux.mcelog",
      "params": [
        {
          "key": "_scope",
          "value": "mcelog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/varlogsecure",
      "rule": "linux.varlogsecure",
      "params": [
        {
          "key": "_scope",
          "value": "varlogsecure"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/host",
      "rule": "linux.host",
      "params": [
        {
          "key": "_scope",
          "value": "KernelArch"
        },
        {
          "key": "_name",
          "expr": "hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/mem",
      "rule": "linux.memUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "memUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/cpupct",
      "rule": "linux.cpuUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "cpuUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/kdumpstatus",
      "rule": "linux.kdumpServiceCheck",
      "params": [
        {
          "key": "_scope",
          "value": "kdumpCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/sard110p",
      "rule": "linux.diskAvgUtil",
      "params": [
        {
          "key": "_scope",
          "value": "diskAvgUtil"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/mount",
      "rule": "linux.mountCheck",
      "params": [
        {
          "key": "_scope",
          "value": "mountCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/dfihP",
      "rule": "linux.inodeUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "inodeUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/disk",
      "rule": "linux.diskUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "diskUsage"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/load",
      "rule": "linux.cpuLoad",
      "params": [
        {
          "key": "_scope",
          "value": "cpuLoad"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/passwd",
      "rule": "linux.etcPasswordCheck",
      "params": [
        {
          "key": "_scope",
          "value": "passwordCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/partition",
      "rule": "linux.partition",
      "params": [
        {
          "key": "_scope",
          "value": "partition"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/multipath",
      "rule": "linux.multipath",
      "params": [
        {
          "key": "_scope",
          "value": "multipath"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/conns",
      "rule": "linux.conns",
      "params": [
        {
          "key": "_scope",
          "value": "conns"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/lvmconf/devices",
      "rule": "linux.lvmconf",
      "params": [
        {
          "key": "_scope",
          "value": "lvmconf"
        },
        {
          "key": "_name",
          "expr": "../../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/ntpsync",
      "rule": "linux.ntpsync",
      "params": [
        {
          "key": "_scope",
          "value": "ntpsync"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/zone",
      "rule": "linux.zone",
      "params": [
        {
          "key": "_scope",
          "value": "zone"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/journalctlcrit",
      "rule": "linux.journalctlcrit",
      "params": [
        {
          "key": "_scope",
          "value": "journalctlcrit"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/journalctlerr",
      "rule": "linux.journalctlerr",
      "params": [
        {
          "key": "_scope",
          "value": "journalctlerr"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sec",
      "rule": "linux.sec",
      "params": [
        {
          "key": "_scope",
          "value": "sec"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/dmesg",
      "rule": "linux.dmesg",
      "params": [
        {
          "key": "_scope",
          "value": "dmesg"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sysrq",
      "rule": "linux.sysrq",
      "params": [
        {
          "key": "_scope",
          "value": "sysrq"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/rpmqalast",
      "rule": "linux.rpmqalast",
      "params": [
        {
          "key": "_scope",
          "value": "rpmqalast"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/rpmVa",
      "rule": "linux.rpmVa",
      "params": [
        {
          "key": "_scope",
          "value": "rpmVa"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/netused",
      "rule": "linux.netused",
      "params": [
        {
          "key": "_scope",
          "value": "netused"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/etclogindefs",
      "rule": "linux.etclogindefs",
      "params": [
        {
          "key": "_scope",
          "value": "etclogindefs"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/base",
      "rule": "linux.base",
      "params": [
        {
          "key": "_scope",
          "value": "base"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/procnetdev",
      "rule": "linux.procnetdev",
      "params": [
        {
          "key": "_scope",
          "value": "procnetdev"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        }
      ]
    }
  ],
  "rulesDir": "./rules"
}"""


new="""{
  "checks": [
    {
      "expr": "",
      "rule": "pre.stat",
      "params": []
    },
    {
      "expr": "",
      "rule": "post.stat",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.date",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.appname",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.summary",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.byte2mb",
      "params": []
    },
    {
      "expr": "",
      "rule": "func.orderby",
      "params": []
    },
    {
      "expr": "//SysStatus/*/psaxoZz",
      "rule": "linux.psaxoZz",
      "params": [
        {
          "key": "_scope",
          "value": "psaxoZz"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/bonding",
      "rule": "linux.bonding",
      "params": [
        {
          "key": "_scope",
          "value": "ethbonding"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sysctla",
      "rule": "linux.sysctla",
      "params": [
        {
          "key": "_scope",
          "value": "sysctla"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/psaxoDd",
      "rule": "linux.psaxoDd",
      "params": [
        {
          "key": "_scope",
          "value": "psaxoDd"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/ethtoolS",
      "rule": "linux.ethtoolS",
      "params": [
        {
          "key": "_scope",
          "value": "ethtoolS"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/lspci",
      "rule": "linux.lspci",
      "params": [
        {
          "key": "_scope",
          "value": "lspci"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/ethtooli",
      "rule": "linux.ethtooli",
      "params": [
        {
          "key": "_scope",
          "value": "ethtooli"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/iptables",
      "rule": "linux.iptables",
      "params": [
        {
          "key": "_scope",
          "value": "iptables"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/msglog",
      "rule": "linux.msglog",
      "params": [
        {
          "key": "_scope",
          "value": "msglog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/dmesglog",
      "rule": "linux.dmesglog",
      "params": [
        {
          "key": "_scope",
          "value": "dmesglog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/bootlog",
      "rule": "linux.bootlog",
      "params": [
        {
          "key": "_scope",
          "value": "bootlog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/mcelog",
      "rule": "linux.mcelog",
      "params": [
        {
          "key": "_scope",
          "value": "mcelog"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/varlogsecure",
      "rule": "linux.varlogsecure",
      "params": [
        {
          "key": "_scope",
          "value": "varlogsecure"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/host",
      "rule": "linux.host",
      "params": [
        {
          "key": "_scope",
          "value": "KernelArch"
        },
        {
          "key": "_name",
          "expr": "hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/mem",
      "rule": "linux.memUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "memUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/cpupct",
      "rule": "linux.cpuUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "cpuUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/kdumpstatus",
      "rule": "linux.kdumpServiceCheck",
      "params": [
        {
          "key": "_scope",
          "value": "kdumpCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/sard110p",
      "rule": "linux.diskAvgUtil",
      "params": [
        {
          "key": "_scope",
          "value": "diskAvgUtil"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/mount",
      "rule": "linux.mountCheck",
      "params": [
        {
          "key": "_scope",
          "value": "mountCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/dfihP",
      "rule": "linux.inodeUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "inodeUsedPercent"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/disk",
      "rule": "linux.diskUsedPercent",
      "params": [
        {
          "key": "_scope",
          "value": "diskUsage"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/load",
      "rule": "linux.cpuLoad",
      "params": [
        {
          "key": "_scope",
          "value": "cpuLoad"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/passwd",
      "rule": "linux.etcPasswordCheck",
      "params": [
        {
          "key": "_scope",
          "value": "passwordCheck"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/partition",
      "rule": "linux.partition",
      "params": [
        {
          "key": "_scope",
          "value": "partition"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/multipath",
      "rule": "linux.multipath",
      "params": [
        {
          "key": "_scope",
          "value": "multipath"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/conns",
      "rule": "linux.conns",
      "params": [
        {
          "key": "_scope",
          "value": "conns"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/lvmconf/devices",
      "rule": "linux.lvmconf",
      "params": [
        {
          "key": "_scope",
          "value": "lvmconf"
        },
        {
          "key": "_name",
          "expr": "../../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/ntpsync",
      "rule": "linux.ntpsync",
      "params": [
        {
          "key": "_scope",
          "value": "ntpsync"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/zone",
      "rule": "linux.zone",
      "params": [
        {
          "key": "_scope",
          "value": "zone"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/journalctlcrit",
      "rule": "linux.journalctlcrit",
      "params": [
        {
          "key": "_scope",
          "value": "journalctlcrit"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/journalctlerr",
      "rule": "linux.journalctlerr",
      "params": [
        {
          "key": "_scope",
          "value": "journalctlerr"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sec",
      "rule": "linux.sec",
      "params": [
        {
          "key": "_scope",
          "value": "sec"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysLogs/*/dmesg",
      "rule": "linux.dmesg",
      "params": [
        {
          "key": "_scope",
          "value": "dmesg"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/sysrq",
      "rule": "linux.sysrq",
      "params": [
        {
          "key": "_scope",
          "value": "sysrq"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/rpmqalast",
      "rule": "linux.rpmqalast",
      "params": [
        {
          "key": "_scope",
          "value": "rpmqalast"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/rpmVa",
      "rule": "linux.rpmVa",
      "params": [
        {
          "key": "_scope",
          "value": "rpmVa"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysStatus/*/netused",
      "rule": "linux.netused",
      "params": [
        {
          "key": "_scope",
          "value": "netused"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/etclogindefs",
      "rule": "linux.etclogindefs",
      "params": [
        {
          "key": "_scope",
          "value": "etclogindefs"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/base",
      "rule": "linux.base",
      "params": [
        {
          "key": "_scope",
          "value": "base"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    },
    {
      "expr": "//SysConfs/*/procnetdev",
      "rule": "linux.procnetdev",
      "params": [
        {
          "key": "_scope",
          "value": "procnetdev"
        },
        {
          "key": "_name",
          "expr": "../host/hostname"
        },
        {
          "key":"_ip",
          "expr":"../edith/ips"
        }
      ]
    }
  ],
  "rulesDir": "./rules"
}
"""

content = new
with open(".sidoc/check-config.json", "r", encoding="UTF-8") as f:
    if '../edith/ips' in f.read():
        content = old

with open(".sidoc/check-config.json", "w", encoding="UTF-8") as f:
    f.write(content)