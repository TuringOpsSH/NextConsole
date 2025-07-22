# README

## 巡检模板

WAS 巡检对应的巡检模板为 `was-common-版本.zip`

## 数据采集

```bash
edith was get-log --profile /WebSphere/AppServer/profiles/AppSrv01/ -o /edith_data -f json
edith was get-conf --profile /WebSphere/AppServer/profiles/AppSrv01/ -o /edith_data -f json
```



