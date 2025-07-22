{{define "meta"}}

---
title: {{.meta.customer}} {{.meta.title}}
subtitle: {{if .meta.sys}}{{.meta.sys}}{{else}}{{range .SysConfs}}{{JsCall "func.appname" .host.hostname}}{{end}}{{end}}
author:
- {{ .meta.author.name}} ({{ .meta.author.email}})
- {{ .meta.org}}

date: {{if .meta.date}}{{.meta.date}}{{else}}{{JsCall "func.date" }}{{end}}
---

{{end}}