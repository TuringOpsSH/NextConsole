{{define "basicconfigs"}}

## 日志配置

| Server      	    | Type     | File Name               | Limits  | Count    |  Size    | 
| :---------------- | :------- | :---------------------- | :------ | -------: | -------: |
{{range .WlsConfs}}{{range .domain.servers}}|{{printf " %-18s" .name}}|{{if .logging.rotationType}}{{printf " %-8s " .}}{{else}}{{printf " %-8s " "default"}}{{end}}|{{if .logging.fileName}}{{printf " %-23s " .}}{{else}}{{printf " %-23s " "default"}}{{end}}|{{if  .logging.numberOfFilesLimited}}{{printf " %-7s " .}}{{else}}{{printf " %-7s " "default"}}{{end}}|{{if  .logging.fileCount}}{{printf " %8s " .}}{{else}}{{printf " %8s " "default"}}{{end}}|{{if  .logging.fileMinSize}}{{printf " %8s " .}}{{else}}{{printf " %8s " "default"}}{{end}} |
{{end}}{{end}}


## Access日志配置

| Server      	    | Enabled  | Type     | File Name               | Limits  | Count    |  Size    | 
| :---------------- | :------- | :------- | :---------------------- | :------ | -------: | -------: |
{{range .WlsConfs}}{{range .domain.servers}}{{printf "| %-18s|" .name}}{{if .webServerLog}}{{printf " %-8s |" .webServerLog.loggingEnabled}}{{else}}{{printf " %-8s |" "default"}}{{end}}{{if .webServerLog}}{{printf " %-8s |" .webServerLog.rotationType}}{{else}}{{printf " %-8s |" "default"}}{{end}}{{if .webServerLog}}{{printf " %-23s |" .webServerLog.fileName}}{{else}}{{printf " %-23s |" "default"}}{{end}}{{if .webServerLog}}{{printf " %-7s |" .webServerLog.numberOfFilesLimited}}{{else}}{{printf " %-7s |" "default"}}{{end}}{{if .webServerLog}}{{printf " %8s |" .webServerLog.fileCount}}{{else}}{{printf " %8s |" "default"}}{{end}}{{if .webServerLog}}{{printf " %8s |" .webServerLog.fileMinSize}}{{else}}{{printf " %8s |" "default"}}{{end}}
{{end}}{{end}}


## 数据源配置

| Name      	               | Min | Max | Target        | Driver                    | 
| :--------------------------- | --: | --: | ------------: |:------------------------- |
{{range .WlsConfs}}{{range .domain.dataSources}}{{if .name}} | {{printf " %-29s " .name}}{{else}}{{printf " %-10s " "-"}}{{end}} | {{if .connectionPool.min}}{{printf " %3s " .connectionPool.min}}{{else}}{{printf " %3s " "-"}}{{end}} | {{if .connectionPool.max}}{{printf " %3s " .connectionPool.max}}{{else}}{{printf " %3s " "-"}}{{end}} | {{if .target}}{{printf " %-13s " .target}}{{else}}{{printf " %3s " "-"}}{{end}} | {{if .driver}}{{printf " %-12s " .driver}}{{else}}{{printf " %3s " "-"}}{{end}} |
{{end}}{{end}}



{{end}}