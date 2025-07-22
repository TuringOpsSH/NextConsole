{{define "mission"}}


## 基本信息

根据本项目的服务合同和用户的要求，我方于{{ .meta.date}}对{{.meta.customer}}中间件进行了当月例行巡检。

巡检过程中，{{.meta.org}}工程师得到了相关负责人的大力支持，按计划顺利完成了本次巡检工作。


## 任务信息

项目名称：{{.meta.project.name}}

客户单位：{{.meta.customer}}

巡检周期：{{.meta.project.cycle}}

客户联系人：{{.meta.project.contact.name}}    电话：{{.meta.project.contact.phone}}

巡检工程师：{{.meta.author.name}}    电话：{{.meta.author.phone}}

项目经理：{{.meta.project.manager.name}}    电话：{{.meta.project.manager.phone}}


{{end}}