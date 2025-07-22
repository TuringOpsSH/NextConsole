{{define "base"}}
{{range .problems}}{{if eq .id "win.base"}}

| 配置项                        | 值                                            |
|:---------------------------|:---------------------------------------------|
| CPU Cores                  | {{index .raw "CPU Cores"}}                   |
| CPU Model                  | {{index .raw "CPU Model"}}                   |
| Disk capacity              | {{index .raw "Disk capacity"}}               |
| IP Count                   | {{index .raw "IP Count"}}                    |
| IP list                    | {{index .raw "IP list"}}                     |
| Machine category           | {{index .raw "Machine category"}}            |
| Mem                        | {{index .raw "Mem"}}                         |
| Memorys                    | {{index .raw "Memorys"}}                     |
| Network card list          | {{index .raw "Network card list"}}           |
| Number of CPU cores        | {{index .raw "Number of CPU cores"}}         |
| Number of network cards    | {{index .raw "Number of network cards"}}     |
| Number of physical CPUs    | {{index .raw "Number of physical CPUs"}}     |
| OS Version                 | {{index .raw "OS Version"}}                  |
| ServerManu                 | {{index .raw "ServerManu"}}                  |
| ServerSerial               | {{index .raw "ServerSerial"}}                |
| Status                     | {{index .raw "Status"}}                      |
| hddModel                   | {{index .raw "hddModel"}}                    |
| hddModel                   | {{index .raw "hddModel"}}                    |

{{end}}{{end}}
{{end}}