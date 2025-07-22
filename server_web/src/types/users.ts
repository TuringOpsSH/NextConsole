export interface Users{
    user_id?: string|number,
    user_code?: string ,
    user_name?: string,
    user_nick_name?: string,
    user_nick_name_py?: string,
    user_email?: string,
    user_phone?: string,
    user_gender?: string,
    user_age?: number,
    user_avatar?: string,
    user_department?: string,
    user_company?: string | null,
    user_account_type?: string,
    user_resource_limit?: number,
    create_time?: string,
    update_time?: string,
    user_expire_time?: string,
    last_login_time?: string,
    user_role?: [string],
    user_status?: string,
    user_source?: string,
    user_wx_nickname?: string,
    user_wx_avatar?: string,
    user_wx_openid?: string,
    user_wx_union_id?: string,
    user_position?: string | null,
    user_area?: string | null,
    user_department_id?: number,
    user_company_id?: number,
    user_invite_code?: string,
    [property: string]: any;
}

export interface UserAccount{
    user_id: string,
    account_id: string,
    account_type: string,
    balance: number,
    frozen_balance: number,
    account_status: string,
    create_time: string,
    update_time: string,
    [property: string]: any;

}


export interface SystemNotice{
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * ID 编号，ID 编号
     */
    id: string;
    /**
     * 通知内容，通知内容
     */
    notice_content: string;
    /**
     * 通知图标，通知图标
     */
    notice_icon: string;
    /**
     * 通知等级，通知等级
     */
    notice_level: string;
    /**
     * 通知状态，通知状态
     */
    notice_status: string;
    /**
     * 通知标题，通知标题
     */
    notice_title: string;
    /**
     * 通知类型，通知图标
     */
    notice_type: string;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    /**
     * 用户id，用户id
     */
    user_id: string;
}

export interface PointTransaction{
    id: number,
    transaction_id: string,
    account_id: string,
    transaction_type: string,
    transaction_amount: number,
    transaction_status: string,
    order_id: string,
    transaction_desc: string,
    create_time: string,
    update_time: string,
}
export interface Product {
    /**
     * 支付方式，1=纯积分 2=现金 3=积分+现金
     */
    accept_payment_methods: number;
    /**
     * 商品种类，商品种类
     */
    category_name: string;
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * ID 编号，ID 编号
     */
    id: number;
    /**
     * 所需人民币，所需人民币
     */
    money_cost_in_rmb: number;
    /**
     * 所需积分，所需积分
     */
    point_cost: number;
    /**
     * 商品编码，商品编码
     */
    product_code: string;
    /**
     * 商品描述，商品描述
     */
    product_desc: string;
    /**
     * 商品图片，商品图片
     */
    product_image: string;
    /**
     * 商品名称，商品名称
     */
    product_name: string;
    /**
     * 商品状态，（0下架/1上架/2预售）
     */
    product_status: string;
    /**
     * 商品库存，商品库存
     */
    product_stock: number;
    product_sales: number;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    [property: string]: any;
}
export interface OrderInfo{
    /**
     * 支付账户id，支付账户id
     */
    account_id: number;
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * 运输信息，运输信息
     */
    delivery_message: string;
    /**
     * 运输状态，运输状态
     */
    delivery_status: string;
    /**
     * 自增id，自增id
     */
    id: number;
    /**
     * 支付钱，支付金额
     */
    money_cost_in_rmb: number;
    /**
     * 订单编号，订单id订单编号
     */
    order_code: string;
    /**
     * 订单描述，订单描述
     */
    order_desc: string;
    /**
     * 订单状态，待支付，支付完成，支付失败，取消，交付完成
     */
    order_status: string;
    /**
     * 订单类型，订单类型
     */
    order_type: string;
    /**
     * 支付方式，1:积分，2：钱，3积分加钱
     */
    payment_method: string;
    /**
     * 支付积分，支付积分
     */
    point_cost: number;
    /**
     * 商品id，商品id
     */
    product_id: number;
    /**
     * 商品数量，商品数量
     */
    quantity: number;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    /**
     * 用户id，用户id
     */
    user_id: number;
    [property: string]: any;
}
export interface OrderItem{
    /**
     * 创建时间，创建时间
     */
    create_time: string;
    /**
     * ID 编号，ID 编号
     */
    id: number;
    /**
     * 人民币价格，人民币价格
     */
    money_cost_in_rmb: number;
    /**
     * 订单id，订单id
     */
    order_id: number;
    /**
     * 订单商品描述，订单商品描述
     */
    order_item_desc: string;
    /**
     * 订单商品图片，订单商品图片
     */
    order_item_image: string;
    /**
     * 订单商品名称，订单商品名称
     */
    order_item_name: string;
    /**
     * 订单商品状态，待交付，已交付，交付异常
     */
    order_item_status: string;
    /**
     * 积分价格，积分价格
     */
    point_cost: number;
    /**
     * 产品id，产品id
     */
    product_id: number;
    /**
     * 商品实例id，商品实例id
     */
    product_item_id: number;
    /**
     * 兑换码，兑换码
     */
    redemption_code: string;
    /**
     * 更新时间，更新时间
     */
    update_time: string;
    [property: string]: any;
}
