{{define "conns"}}
{{range .problems}}{{if eq .id "win.conns"}}

|              LISTEN              |   TIME_WAIT    |   ESTABLISHED   |  
|:-------------------------------:|:-------------:|:------------:|
| {{range .mixraw}} {{.listen}} | {{ .time_wait}}   | {{ .established}}  | 
{{end}}
{{end}}{{end}}

{{end}}