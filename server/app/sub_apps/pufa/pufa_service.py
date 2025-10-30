import pandas as pd
import io
import requests
import markdown


def convert_markdown_to_excel_and_upload(data):
    """
    将Markdown表格转换为Excel并上传到第三方服务的业务逻辑
    """


    markdown_table = data.get("markdown_table")
    user_id = data.get("user_id")

    # 将Markdown表格转换为DataFrame
    try:
        df = pd.read_csv(io.StringIO(markdown.markdown(markdown_table)), sep="|", skipinitialspace=True)
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])  # 删除无用列
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse markdown table: {str(e)}"}

    # 将DataFrame保存为Excel文件
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_buffer.seek(0)

    # 上传Excel文件到第三方服务
    upload_url = "https://third-party-service.com/upload"
    files = {'file': ('table.xlsx', excel_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post(upload_url, files=files, data={'user_id': user_id})

    if response.status_code == 200:
        return {"status": "success", "message": "File uploaded successfully", "response": response.json()}
    else:
        return {"status": "error", "message": f"Failed to upload file: {response.text}"}
