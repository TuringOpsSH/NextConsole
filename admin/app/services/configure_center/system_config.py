from app.models.configure_center.system_config import SupportArea
from app.services.configure_center.response_utils import next_console_response


def get_support_area_data():
    """
    获取支持区域数据，并组装成前端需要的数据格式
    data.continent
        data.region
            data.name+(data.iso_code_3)
                data.area
    [
        {
            value: 'guide',  +
            label: 'Guide',
            children: []
        },
    ]
    """
    support_area = SupportArea.query.filter(
        SupportArea.area_status == "正常"
    ).order_by(
        SupportArea.continent,
        SupportArea.country,
        SupportArea.province,
        SupportArea.city
    ).all()
    support_area_list = []
    continent_index_dict = {}
    country_index_dict = {}
    province_index_dict = {}
    for data in support_area:
        if data.continent not in continent_index_dict:
            continent_index_dict[data.continent] = len(support_area_list)
            support_area_list.append({
                "value": data.continent,
                "label": data.continent,
                "children": []
            })
        continent_index = continent_index_dict[data.continent]
        if data.country not in country_index_dict:
            country_index_dict[data.country] = len(support_area_list[continent_index]["children"])
            support_area_list[continent_index]["children"].append({
                "value": data.country,
                "label": data.country,
                "children": []
            })
        country_index = country_index_dict[data.country]
        if data.province not in province_index_dict:
            province_index_dict[data.province] = len(support_area_list[continent_index]["children"][country_index]["children"])
            support_area_list[continent_index]["children"][country_index]["children"].append({
                "value": data.province,
                "label": f"{data.province}",
                "children": []
            })
        province_index = province_index_dict[data.province]
        support_area_list[continent_index]["children"][country_index]["children"][province_index]["children"].append({
            "value": data.city,
            "label": data.city
        })
    return next_console_response(result=support_area_list)


