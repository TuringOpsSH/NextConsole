from app.services.configure_center.response_utils import next_console_response
from app.models.user_center.user_info import *
from .whzy_model import *


def get_salesData_price(params):
    """
    获取销售数据
    :param params:
    :return:
    """
    user_id = params.get("user_id")
    startTime = params.get("startTime")
    endTime = params.get("endTime")
    productName = params.get("productName", [])
    productLevel = params.get("productLevel", [])
    productSpecification = params.get("productSpecification", [])
    wholesalePrice = params.get("wholesalePrice", [])
    recommendRetailPrice = params.get("recommendRetailPrice", [])
    city = params.get("city", [])
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    all_conditions = [
        ZYSalesDataInfo.status == '正常',
    ]
    if startTime:
        all_conditions.append(ZYSalesDataInfo.start_time >= startTime)
    if endTime:
        all_conditions.append(ZYSalesDataInfo.end_time <= endTime)
    if productName:
        all_conditions.append(ZYSalesDataInfo.product_name.in_(productName))
    if productLevel:
        all_conditions.append(ZYSalesDataInfo.product_level.in_(productLevel))
    if productSpecification:
        all_conditions.append(ZYSalesDataInfo.product_specification.in_(productSpecification))
    if wholesalePrice:
        try:
            first_price = float(wholesalePrice[0])
        except:
            first_price = 0
        try:
            second_price = float(wholesalePrice[1])
        except:
            second_price = None
        all_conditions.append(ZYSalesDataInfo.wholesale_price >= first_price)
        if second_price:
            all_conditions.append(ZYSalesDataInfo.wholesale_price <= second_price)
    if recommendRetailPrice:
        try:
            first_price = float(recommendRetailPrice[0])
        except:
            first_price = 0
        try:
            second_price = float(recommendRetailPrice[1])
        except:
            second_price = None
        all_conditions.append(ZYSalesDataInfo.recommended_retail_price >= first_price)
        if second_price:
            all_conditions.append(ZYSalesDataInfo.recommended_retail_price <= second_price)
    if city:
        all_conditions.append(ZYSalesDataInfo.city.in_(city))
    sales_data = ZYSalesDataInfo.query.filter(
        *all_conditions
    ).order_by(
        ZYSalesDataInfo.start_time,
        ZYSalesDataInfo.end_time,
        ZYSalesDataInfo.city,
    ).all()
    # 补充所有条件的选项
    minStartTime = ZYSalesDataInfo.query.with_entities(func.min(ZYSalesDataInfo.start_time)).first()[0]
    maxEndTime = ZYSalesDataInfo.query.with_entities(func.max(ZYSalesDataInfo.end_time)).first()[0]
    allProductName = ZYSalesDataInfo.query.with_entities(ZYSalesDataInfo.product_name).distinct().all()
    allProductLevel = ZYSalesDataInfo.query.with_entities(ZYSalesDataInfo.product_level).distinct().all()
    allProductSpecification = ZYSalesDataInfo.query.with_entities(ZYSalesDataInfo.product_specification).distinct().all()
    allCity = ZYSalesDataInfo.query.with_entities(ZYSalesDataInfo.city).distinct().all()
    all_options = {
        "startTime": minStartTime.strftime('%Y-%m-%d %H:%M:%S'),
        "endTime": maxEndTime.strftime('%Y-%m-%d %H:%M:%S'),
        "productName": [i[0] for i in allProductName],
        "productLevel": [i[0] for i in allProductLevel],
        "productSpecification": [i[0] for i in allProductSpecification],
        "city": [i[0] for i in allCity],
    }
    result = {
        "data": [i.to_dict() for i in sales_data],
        "total": len(sales_data),
        "options": all_options
    }
    return next_console_response(result=result)


def get_salesData_inventory(params):
    """
    获取销售数据
    :param params:
    :return:
    """
    user_id = params.get("user_id")
    startTime = params.get("startTime")
    endTime = params.get("endTime")
    productLevel = params.get("productLevel", [])
    city = params.get("city", [])
    productSpecification = params.get("productSpecification", [])
    productInventory = params.get("productInventory", [])
    productRemainDays = params.get("productRemainDays", [])

    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！", error_code=1002)
    all_conditions = [
        ZYInventoryDataInfo.status == '正常',
    ]
    if startTime:
        all_conditions.append(ZYInventoryDataInfo.start_time >= startTime)
    if endTime:
        all_conditions.append(ZYInventoryDataInfo.end_time <= endTime)
    if productLevel:
        all_conditions.append(ZYInventoryDataInfo.product_level.in_(productLevel))
    if productSpecification:
        all_conditions.append(ZYInventoryDataInfo.product_specification.in_(productSpecification))
    if productInventory:
        try:
            first_price = float(productInventory[0])
        except:
            first_price = 0
        try:
            second_price = float(productInventory[1])
        except:
            second_price = None
        all_conditions.append(ZYInventoryDataInfo.product_inventory >= first_price)
        if second_price:
            all_conditions.append(ZYInventoryDataInfo.product_inventory <= second_price)
    if productRemainDays:
        try:
            first_price = float(productRemainDays[0])
        except:
            first_price = 0
        try:
            second_price = float(productRemainDays[1])
        except:
            second_price = None
        all_conditions.append(ZYInventoryDataInfo.product_remain_days >= first_price)
        if second_price:
            all_conditions.append(ZYInventoryDataInfo.product_remain_days <= second_price)
    if city:
        all_conditions.append(ZYInventoryDataInfo.city.in_(city))
    sales_data = ZYInventoryDataInfo.query.filter(
        *all_conditions
    ).order_by(
        ZYInventoryDataInfo.start_time,
        ZYInventoryDataInfo.end_time,
        ZYInventoryDataInfo.city,
    ).all()
    # 补充所有条件的选项
    minStartTime = ZYInventoryDataInfo.query.with_entities(func.min(ZYInventoryDataInfo.start_time)).first()[0]
    maxEndTime = ZYInventoryDataInfo.query.with_entities(func.max(ZYInventoryDataInfo.end_time)).first()[0]
    allProductLevel = ZYInventoryDataInfo.query.with_entities(ZYInventoryDataInfo.product_level).distinct().all()
    allProductSpecification = ZYInventoryDataInfo.query.with_entities(ZYInventoryDataInfo.product_specification).distinct().all()
    allCity = ZYInventoryDataInfo.query.with_entities(ZYInventoryDataInfo.city).distinct().all()
    all_options = {
        "startTime": minStartTime.strftime('%Y-%m-%d %H:%M:%S'),
        "endTime": maxEndTime.strftime('%Y-%m-%d %H:%M:%S'),
        "productLevel": [i[0] for i in allProductLevel],
        "productSpecification": [i[0] for i in allProductSpecification],
        "city": [i[0] for i in allCity],
    }
    result = {
        "data": [i.to_dict() for i in sales_data],
        "total": len(sales_data),
        "options": all_options
    }
    return next_console_response(result=result)
