/******************************************/
/*   DatabaseName = next_console_dev   */
/*   TableName = zypricedatainfo   */
/******************************************/
CREATE TABLE `zypricedatainfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据统计开始时间',
  `end_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '数据统计完成时间',
  `product_name` varchar(255) NOT NULL COMMENT '产品名称',
  `product_level` varchar(255) NOT NULL COMMENT '产品等级',
  `product_specification` varchar(255) NOT NULL COMMENT '产品规格',
  `wholesale_price` double NOT NULL COMMENT '批发价格',
  `recommended_retail_price` double NOT NULL COMMENT '建议零售价',
  `city` varchar(255) NOT NULL COMMENT '城市',
  `purchase_price` double DEFAULT NULL COMMENT '进货价',
  `sale_price` double DEFAULT NULL COMMENT '出货价',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '正常' COMMENT '数据状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9325 DEFAULT CHARSET=utf8 COMMENT='ZY产品价格数据信息'
;





/******************************************/
/*   DatabaseName = next_console_dev   */
/*   TableName = zyinventorydatainfo   */
/******************************************/
CREATE TABLE `zyinventorydatainfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据开始时间',
  `end_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '数据结束时间',
  `product_level` varchar(255) NOT NULL COMMENT '产品等级',
  `product_specification` varchar(255) NOT NULL COMMENT '产品规格',
  `product_inventory` double DEFAULT NULL COMMENT '产品库存',
  `product_remain_days` int(11) DEFAULT NULL COMMENT '产品库存可销天数',
  `city` varchar(255) NOT NULL COMMENT '城市',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '正常' COMMENT '数据状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3219 DEFAULT CHARSET=utf8 COMMENT='ZY产品库存数据信息'
;

/******************************************/
/*   DatabaseName = next_console_dev   */
/*   TableName = zypurchasedatainfo   */
/******************************************/
CREATE TABLE `zypurchasedatainfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `start_time` varchar(255) NOT NULL COMMENT '开始时间',
  `end_time` varchar(255) NOT NULL COMMENT '结束时间',
  `product_level` varchar(255) NOT NULL COMMENT '产品等级',
  `product_specification` varchar(255) NOT NULL COMMENT '产品规格',
  `city` varchar(255) NOT NULL COMMENT '城市',
  `customer_level` varchar(255) NOT NULL COMMENT '客户等级',
  `avg_purchase` double DEFAULT NULL COMMENT '户均投放条数',
  `avg_purchase_all` double DEFAULT NULL COMMENT '户均进货条数',
  `status` varchar(255) NOT NULL DEFAULT '正常' COMMENT '状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1043 DEFAULT CHARSET=utf8 COMMENT='产品采购数据信息'
;

