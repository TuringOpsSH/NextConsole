{{define "disk"}}
{{range .SysConfs}}

|路径|文件系统类型|总量(MB)|已用(MB)|剩余(MB)|使用率|检查结果|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
{{range .disk}}{{if ne .fstype "tmpfs" }}{{if ne .fstype "sysfs" }}{{if ne .fstype "proc" }}{{if ne .fstype "cgroupfs" }}{{if ne .fstype "isofs" }}|{{printf "%-13s" .path}}|{{printf "%-13s" .fstype}}|{{JsCall "func.byte2mb" .total }}|{{JsCall "func.byte2mb" .used}}|{{JsCall "func.byte2mb" .free}}|{{printf "%-.2g%%" .usedPercent}}|{{ if gt .usedPercent 80.00 }}{{ if ne .fstype "isofs" }}{{ Icon "red"}} {{else}}{{ Icon "green"}}{{end}} {{else}} {{Icon "green"}} {{end}}|
{{end}}{{end}}{{end}}{{end}}{{end}}{{end}}

{{end}}
{{end}}