from flask import jsonify


def next_console_response(error_status=False, error_code=0, error_message="", result=None):
    """
    xiaoyi 返回格式的标准化
    :param error_status: 异常状态
    :param error_code:  状态码
    :param error_message:  异常信息
    :param result: 返回结果
    :return:
    """
    response = {
        "error_status": error_status,
        "error_code": error_code,
        "error_message": error_message,
        "result": result
    }
    try:
        return jsonify(response)
    except Exception as e:
        return jsonify(e.args)


def edith_response(error_status=False, error_code=0, error_message="", result={}):
    """
    edith 返回格式的标准化
    :param error_status: 异常状态
    :param error_code:  状态码
    :param error_message:  异常信息
    :param result: 返回结果
    :return:
    {
  "status": 400,
  "code": "EB0001",
  "message": "参数错误",
  "suggestion": "请检查参数是否正确",
  "more_info": "https://example.com/docs/error-codes/EB0001"
}
    """
    if error_status:
        response = {
            "status": error_status,
            "code": error_code,
            "message": result,
            "suggestion": error_message,
            "more_info": {}
        }
    else:
        response = {
            "status": 200,
            "data": {
                "content": result,
                "meta": {}
            }

        }

    return jsonify(response)


def edith_params_check(params):
    """
    对edith的入参进行检验
    whoami
    user
    scene
    stage
    task
    user_input
    is_retry
    """
    if "user_input" not in params or "text" not in params["user_input"] or not params["user_input"]["text"]:
        return False, "用户输入未提交！"
    return True, ""


def llm_response(error_status=False, error_code=0, error_message="", result={}):
    """
    llm 返回格式的标准化
    :param error_status: 异常状态
    :param error_code:  状态码
    :param error_message:  异常信息
    :param result: 返回结果
    :return:
    """
    response = {
        "error_status": error_status,
        "error_code": error_code,
        "error_message": error_message,
        "result": result
    }
    try:
        return jsonify(response)
    except Exception as e:
        return jsonify(e.args)
