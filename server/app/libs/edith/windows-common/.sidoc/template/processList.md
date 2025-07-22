{{define "processList"}}

{{range .problems}} {{if eq .id "win.processList"}}{{range $k, $v := .raw}}
{{JsCall "func.simpleTable" $v "*" "*"}}
{{end}}{{end}}{{end}}

{{end}}