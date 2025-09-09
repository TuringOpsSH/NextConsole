from sqlalchemy import or_, and_

from app.app import db
from app.models.contacts.company_model import *
from app.models.contacts.department_model import *
from app.models.user_center.user_info import UserFriendsRelation, UserInfo
from app.services.configure_center.response_utils import next_console_response
from app.services.configure_center.system_notice_service import send_add_friend_msg
from app.services.user_center.system_notice_service import add_system_notice_service


def get_friends_service(user_id):
    """
    获取好友列表，为了查看历史记录,补充被动删除的朋友
        判断逻辑，rel_status >=1
        当user_id 为自己，且rel_status in (1,2)
        或者当friend_id 为自己，且rel_status in (1,3)
    :param user_id:
    :return:
    """
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friends_relations = UserFriendsRelation.query.filter(
        UserFriendsRelation.rel_status >= 1,
        or_(
            and_(
                UserFriendsRelation.user_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 2])
            ),
            and_(
                UserFriendsRelation.friend_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 3])
            )
        ),
    ).join(
        UserInfo,
        or_(
            UserInfo.user_id == UserFriendsRelation.user_id,
            UserInfo.user_id == UserFriendsRelation.friend_id
        )
    ).filter(
        UserInfo.user_status == 1,
        UserInfo.user_id != user_id
    ).with_entities(
        UserInfo
    ).order_by(
        UserInfo.user_nick_name_py
    ).all()
    # 更新好友公司名称与部门名称
    plus_account_friends = [friend for friend in friends_relations if friend.user_account_type == '企业账号']
    all_company_ids = [friend.user_company_id for friend in plus_account_friends]
    all_department_ids = [friend.user_department_id for friend in plus_account_friends]
    all_company = CompanyInfo.query.filter(
        CompanyInfo.id.in_(all_company_ids),
        CompanyInfo.company_status == '正常'
    ).all()
    all_department = DepartmentInfo.query.filter(
        DepartmentInfo.id.in_(all_department_ids),
        DepartmentInfo.department_status == '正常'
    ).all()
    all_company_name_maps = {company.id: company.company_name for company in all_company}
    all_department_name_maps = {department.id: department.department_name for department in all_department}
    res = []
    for friend in friends_relations:
        friend_dict = friend.to_dict()
        if friend.user_account_type == "企业账号":
            friend_dict["user_company"] = all_company_name_maps.get(friend.user_company_id, friend.user_company)
            friend_dict["user_department"] = all_department_name_maps.get(
                friend.user_department_id, friend.user_department)
        res.append(friend_dict)
    return next_console_response(result={
        "total": len(res),
        "data": res
    })


def search_friends_service(params):
    """
    根据条件搜索好友
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_keyword = params.get("friend_keyword")
    page_size = params.get("page_size", 100)
    page_num = params.get("page_num", 1)
    fetch_all = params.get("fetch_all", True)
    filter_conditions = []
    if friend_keyword:
        filter_conditions.append(
            or_(
                UserInfo.user_nick_name.like("%{}%".format(friend_keyword)),
                UserInfo.user_nick_name_py.like("%{}%".format(friend_keyword)),
                UserInfo.user_email.like("%{}%".format(friend_keyword))
            )
        )

    friends_relations = UserFriendsRelation.query.filter(
        UserFriendsRelation.rel_status >= 1,
        or_(
            and_(
                UserFriendsRelation.user_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 2])
            ),
            and_(
                UserFriendsRelation.friend_id == user_id,
                UserFriendsRelation.rel_status.in_([1, 3])
            )
        ),
    ).join(
        UserInfo,
        or_(
            UserInfo.user_id == UserFriendsRelation.user_id,
            UserInfo.user_id == UserFriendsRelation.friend_id
        )
    ).filter(
        UserInfo.user_status == 1,
        UserInfo.user_id != user_id,
        *filter_conditions
    ).with_entities(
        UserInfo
    ).order_by(
        UserInfo.user_nick_name_py
    )
    total = friends_relations.count()
    if fetch_all:
        friends_relations = friends_relations.all()
    else:
        friends_relations = friends_relations.paginate(page=page_num, per_page=page_size, error_out=False)

    # 更新好友公司名称与部门名称
    plus_account_friends = [friend for friend in friends_relations if friend.user_account_type == '企业账号']
    all_company_ids = [friend.user_company_id for friend in plus_account_friends]
    all_department_ids = [friend.user_department_id for friend in plus_account_friends]
    all_company = CompanyInfo.query.filter(
        CompanyInfo.id.in_(all_company_ids),
        CompanyInfo.company_status == '正常'
    ).all()
    all_department = DepartmentInfo.query.filter(
        DepartmentInfo.id.in_(all_department_ids),
        DepartmentInfo.department_status == '正常'
    ).all()
    all_company_name_maps = {company.id: company.company_name for company in all_company}
    all_department_name_maps = {department.id: department.department_name for department in all_department}
    res = []
    for friend in friends_relations:
        friend_dict = friend.to_dict()
        if friend.user_account_type == "企业账号":
            friend_dict["user_company"] = all_company_name_maps.get(friend.user_company_id, friend.user_company)
            friend_dict["user_department"] = all_department_name_maps.get(
                friend.user_department_id, friend.user_department)
        res.append(friend_dict)
    return next_console_response(result={
        "total": total,
        "data": res
    })


def add_friends_service(params):
    """
    申请好友，
        检查已有关系
        添加申请记录
        发送申请消息
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_id = params.get("friend_id")
    friend_user = UserInfo.query.filter(
        UserInfo.user_id == friend_id,
        UserInfo.user_status == 1
    ).first()
    if not friend_user:
        return next_console_response(error_status=True, error_message="好友不存在！")
    # 检查是否已经是好友
    friends_relation = UserFriendsRelation.query.filter(
        or_(
            UserFriendsRelation.user_id == user_id,
            UserFriendsRelation.friend_id == user_id
        ),
        or_(
            UserFriendsRelation.user_id == friend_id,
            UserFriendsRelation.friend_id == friend_id
        )
    ).first()
    if friends_relation:
        if friends_relation.rel_status == 1:
            return next_console_response(error_status=True, error_message="已经是好友！")
        if friends_relation.rel_status == 0:
            return next_console_response(error_status=True, error_message="已经申请，请等等！")
        if friends_relation.rel_status == -1:
            return next_console_response(error_status=True, error_message="已经拒绝！")
        if friends_relation.rel_status in (2, 3, 4):
            friends_relation.rel_status = 0
            db.session.add(friends_relation)
            db.session.commit()
            send_add_friend_msg({
                "user_id": friend_id,
                "data": target_user.show_info()
            })
            return next_console_response(result=friends_relation.to_dict())
    new_relation = UserFriendsRelation(
        user_id=user_id,
        friend_id=friend_id,
        rel_status=0
    )
    db.session.add(new_relation)
    db.session.commit()
    # 发送websocket通知
    send_add_friend_msg({
        "user_id": friend_id,
        "data":  target_user.show_info()
    })
    # 发送站内信通知
    add_system_notice_service(
        {
            "user_id": friend_id,
            "notice_title": "好友申请",
            "notice_content": f"您收到一条好友申请 ，请及时查看。",
            "notice_icon": "notice_primary.svg",
        }
    )
    return next_console_response(result=new_relation.to_dict())


def accept_friends_service(params):
    """
    接受好友申请
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_id = params.get("friend_id")
    friend_user = UserInfo.query.filter(
        UserInfo.user_id == friend_id,
        UserInfo.user_status == 1
    ).first()
    if not friend_user:
        return next_console_response(error_status=True, error_message="好友不存在！")
    friends_relation = UserFriendsRelation.query.filter(
        UserFriendsRelation.user_id == friend_id,
        UserFriendsRelation.friend_id == user_id
    ).first()
    if not friends_relation:
        return next_console_response(error_status=True, error_message="好友申请不存在！")
    if friends_relation.rel_status != 0:
        return next_console_response(error_status=True, error_message="好友申请状态错误！")
    friends_relation.rel_status = 1
    db.session.add(friends_relation)
    db.session.commit()
    add_system_notice_service(
        {
            "user_id": friend_id,
            "notice_title": "好友申请",
            "notice_content": f"您的好友申请已经通过 ，请及时查看。",
            "notice_icon": "notice_success.svg",
        }
    )
    return next_console_response(result=friends_relation.to_dict())


def reject_friends_service(params):
    """
    拒绝好友申请
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_id = params.get("friend_id")
    friend_user = UserInfo.query.filter(
        UserInfo.user_id == friend_id,
        UserInfo.user_status == 1
    ).first()
    if not friend_user:
        return next_console_response(error_status=True, error_message="好友不存在！")
    friends_relation = UserFriendsRelation.query.filter(
        UserFriendsRelation.user_id == friend_id,
        UserFriendsRelation.friend_id == user_id
    ).first()
    if not friends_relation:
        return next_console_response(error_status=True, error_message="好友申请不存在！")
    if friends_relation.rel_status != 0:
        return next_console_response(error_status=True, error_message="好友申请状态错误！")
    friends_relation.rel_status = -1
    db.session.add(friends_relation)
    db.session.commit()
    add_system_notice_service(
        {
            "user_id": friend_id,
            "notice_title": "好友申请",
            "notice_content": f"您的好友申请已被拒绝 ，请及时查看。",
            "notice_icon": "notice_warning.svg",
        }
    )
    return next_console_response(result=friends_relation.to_dict())


def delete_friends_service(params):
    """
    删除好友
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_id = params.get("friend_id")
    friend_user = UserInfo.query.filter(
        UserInfo.user_id == friend_id,
        UserInfo.user_status == 1
    ).first()
    if not friend_user:
        return next_console_response(error_status=True, error_message="好友不存在！")
    friends_relation = UserFriendsRelation.query.filter(
        or_(
            UserFriendsRelation.user_id == user_id,
            UserFriendsRelation.friend_id == user_id
        ),
        or_(
            UserFriendsRelation.user_id == friend_id,
            UserFriendsRelation.friend_id == friend_id
        )
    ).first()
    if not friends_relation:
        return next_console_response(error_status=True, error_message="好友关系不存在！")
    if friends_relation.user_id == user_id:
        if friends_relation.rel_status == 1:
            friends_relation.rel_status = 3
        elif friends_relation.rel_status == 2:
            friends_relation.rel_status = 4
    else:
        if friends_relation.rel_status == 1:
            friends_relation.rel_status = 2
        elif friends_relation.rel_status == 3:
            friends_relation.rel_status = 4
    db.session.add(friends_relation)
    db.session.commit()
    return next_console_response(result=friends_relation.to_dict())


def get_stranger_service(params):
    """
    获取陌生人信息
        允许用邮箱，手机，查询
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_email = params.get("new_friend_email")
    friend_user = UserInfo.query.filter(
        or_(
            UserInfo.user_email == friend_email,
            UserInfo.user_phone == friend_email,
        ),
        UserInfo.user_status == 1
    ).first()
    if not friend_user:
        return next_console_response()
    from app.models.configure_center.user_config import UserConfig
    # 检查是否可以添加好友
    search_config = UserConfig.query.filter(
        UserConfig.user_id == friend_user.user_id,
        UserConfig.config_status == '正常',
        UserConfig.config_key == 'contact'
    ).first()
    if not search_config or not search_config.config_value.get("allow_search", True):
        return next_console_response()
    friends_relation = UserFriendsRelation.query.filter(
        or_(
            UserFriendsRelation.user_id == user_id,
            UserFriendsRelation.friend_id == user_id
        ),
        or_(
            UserFriendsRelation.user_id == friend_user.user_id,
            UserFriendsRelation.friend_id == friend_user.user_id
        )
    ).first()
    res = friend_user.show_info()
    if friends_relation:
        res["rel_status"] = friends_relation.to_dict()
    # 更新企业名称与部门名称
    if friend_user.user_account_type == "企业账号":
        target_company = CompanyInfo.query.filter(
            CompanyInfo.company_status == '正常',
            CompanyInfo.id == friend_user.user_company_id
        ).first()
        if target_company:
            res["user_company"] = target_company.company_name
        target_department = DepartmentInfo.query.filter(
            DepartmentInfo.department_status == "正常",
            DepartmentInfo.id == friend_user.user_department_id
        ).first()
        if target_department:
            res["user_department"] = target_department.department_name
    return next_console_response(result=res)


def get_friend_request_service(params):
    """
    获取好友申请列表
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_requests = UserFriendsRelation.query.filter(
        or_(
            UserFriendsRelation.friend_id == user_id,
            UserFriendsRelation.user_id == user_id
        )
    ).join(
        UserInfo,
        or_(
            UserInfo.user_id == UserFriendsRelation.user_id,
            UserInfo.user_id == UserFriendsRelation.friend_id
        )
    ).filter(
        UserInfo.user_status == 1,
        UserInfo.user_id != user_id,
    ).with_entities(
        UserFriendsRelation,
        UserInfo
    ).order_by(
        UserFriendsRelation.create_time.desc()
    ).all()
    res = []
    for rel, friend in friend_requests:
        friend_dict = friend.show_info()
        friend_dict["rel_status"] = rel.to_dict()
        res.append(friend_dict)
    return next_console_response(result=res)


def get_friend_request_count(params):
    """
    快速获取好友申请数量
    :param params:
    :return:
    """
    user_id = int(params.get("user_id"))
    target_user = UserInfo.query.filter(
        UserInfo.user_id == user_id,
        UserInfo.user_status == 1
    ).first()
    if not target_user:
        return next_console_response(error_status=True, error_message="用户不存在！")
    friend_requests_count = UserFriendsRelation.query.filter(
        UserFriendsRelation.friend_id == user_id,
        UserFriendsRelation.rel_status == 0
    ).count()
    return next_console_response(result=friend_requests_count)

