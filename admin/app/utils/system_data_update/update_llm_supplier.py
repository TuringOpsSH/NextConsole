from gevent import monkey
import platform
if platform.system().lower().startswith('darwin'):
    monkey.patch_socket()
else:
    monkey.patch_all()
import requests
import json
from app.app import app, db
from sqlalchemy.orm.attributes import flag_modified

suppliers = [
    "阿里云百炼"
]


def update_dashscope_models():
    """
    爬取并生成最新的阿里云百炼模型列表
    :return:
    """
    with app.app_context():
        url = "https://bailian-cs.console.aliyun.com/data/api.json?action=BroadScopeAspnGateway&product=sfm_bailian&api=zeldaEasy.broadscope-platform.modelCenter.listFoundationModels&_v=undefined"
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'bailian-cs.console.aliyun.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        raw_payload = {
            "params": {"Api": "zeldaEasy.broadscope-platform.modelCenter.listFoundationModels", "V": "1.0", "Data": {
                "input": {"name": "", "provider": "", "capabilities": [], "contextWindowLessEqual": None,
                          "contextWindowGreaterEqual": None, "queryApplyStatus": True, "queryPrice": True, "queryQuota": True,
                          "queryQpmInfo": True, "queryPermissions": True, "queryWorkspaceLimit": True, "pageSize": 12,
                          "group": True, "pageNo": 1, "profileRegion": "cn_hangzhou"},
                "cornerstoneParam": {"feTraceId": "8a6705cb-321d-416a-a529-487e191ada7f",
                                     "feURL": "https://bailian.console.aliyun.com/?tab=model#/model-market", "protocol": "V2",
                                     "console": "ONE_CONSOLE", "productCode": "p_efm", "switchAgent": 10096242,
                                     "switchUserType": 3, "domain": "bailian.console.aliyun.com", "userNickName": "",
                                     "userPrincipalName": "", "xsp_lang": "zh-CN"}}},
            "sec_token": "3vw72qfc0x4Fk1MUZR8Y1C"
        }
        result = []
        for i in range(1, 12):
            raw_payload['params']['Data']['input']['pageNo'] = i
            new_params = json.dumps(raw_payload['params'], ensure_ascii=False)
            new_payload = f"params={requests.utils.quote(new_params)}&sec_token=3vw72qfc0x4Fk1MUZR8Y1C"
            response = requests.post(url, headers=headers, data=new_payload)
            data = response.json()
            model_type_mapping = {
                'TG': '文本生成',
                'IG': '图片生成',
                'QwQ': '推理模型',
                'IU': '图片理解',
                'VU': '视频理解',
                'ASR': '语音识别',
                'TTS': '语音合成',
                'VG': '视频生成',
                'OMNI': '全模态',
                'TR': '向量模型',
                'RK': '排序模型',
                'AU': '音频理解',
                'IP': '图片处理'
            }
            for model in data['data']['DataV2']["data"]["data"]["list"]:
                for item in model["items"]:
                    llm_tags = item.get("capabilities", [])
                    llm_type = model_type_mapping.get(llm_tags[0], "文本生成")
                    sub_res = {
                        "llm_label": item.get("name", ""),
                        "llm_name": item.get("model", ""),
                        "llm_desc": item.get("description", ""),
                        "llm_tags": llm_tags,
                        "llm_type": llm_type,
                        "max_tokens": item.get("contextWindow", None),
                    }
                    result.append(sub_res)
        with open("dashscope_models.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        # 更新至数据库

        from app.models.configure_center.llm_kernel import LLMSupplierInfo
        dashscope_row = LLMSupplierInfo.query.filter_by(supplier_name="阿里云百炼").first()
        if not dashscope_row:
            dashscope_row = LLMSupplierInfo(
                supplier_code="dashscope",
                supplier_name="阿里云百炼",
                supplier_desc="阿里云推出的大模型一站式服务平台，集成了通义千问等模型，为企业提供精调、部署和集成服务。",
                supplier_icon="/images/bailian.svg",
                supplier_website="https://bailian.aliyun.com",
                supplier_status="正常",
                supplier_type="国内",
                supplier_api_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        dashscope_row.supplier_models = result
        flag_modified(dashscope_row, "supplier_models")
        db.session.add(dashscope_row)
        db.session.commit()


if __name__ == "__main__":
    update_dashscope_models()

