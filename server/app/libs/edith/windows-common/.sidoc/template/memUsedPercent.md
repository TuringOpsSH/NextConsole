{{define "memUsedPercent"}}
{{range .problems}}{{if eq .id "win.memUsedPercent"}}

|               总量 (MB)                |        已使用(MB)                       |         可用(MB)                        |      内存使用率                  |                                  告警                                   |
|:------------------------------------:|:------------------------------------:|:-------------------------------------:|:---------------------------:|:---------------------------------------------------------------------:|
| {{JsCall "func.byte2mb" .raw.total}} | {{JsCall "func.byte2mb" .raw.used }} | {{JsCall "func.byte2mb" .raw.free  }} |    {{.raw.usedPercent }}    | {{if gt  .level "高风险"}}{{Icon "red"}}{{else}}{{Icon "green"}} {{end}} |


{{end}}{{end}}
{{end}}