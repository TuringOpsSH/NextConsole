{{define "mem"}}
{{range .SysConfs}}

| 总量 (MB)| 已使用(MB)| 可用(MB) |缓存(MB)| swap总量(MB)| swap可用(MB) | 内存使用率|检查结果|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| {{JsCall "func.byte2mb" .mem.total}}  |{{JsCall "func.byte2mb" .mem.used }} |{{JsCall "func.byte2mb" .mem.free  }} | {{JsCall "func.byte2mb" .mem.cached }} | {{JsCall "func.byte2mb" .mem.swapTotal }}|  {{JsCall "func.byte2mb" .mem.swapFree }} | {{printf "%.2f%%" .mem.usedPercent }} |{{if gt  .mem.usedPercent 70.00}}{{Icon "red"}}{{else}}{{Icon "green"}} {{end}}|

{{end}}

{{end}}