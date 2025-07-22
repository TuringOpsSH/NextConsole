{{define "recent10ErrorMsg"}}
{{range .problems}}{{if eq .id "win.recent10ErrorMsg"}}

|                日志名称             |            源名称            |          主机名           |             事件ID            |    事件唯一标识符                |                 时间                  | 等级                |                进程ID             |                           线程ID |
|:----------------------------------:|:-------------------------:|:----------------------:|:---------------------------:|:-------------------------:|:-----------------------------------:|:------------------|--------------------------------:|-------------------------------:|
|{{range .raw}} {{.System.Channel}}| {{.System.Provider.Name}} | {{.System.Computer}}   | {{.System.EventID.EventID}} | {{.System.EventRecordID}} | {{.System.TimeCreated.SystemTime}}  | {{.System.Level}} | {{.System.Execution.ProcessID}} | {{.System.Execution.ThreadID}} |
{{end}}
{{end}}{{end}}
{{end}}