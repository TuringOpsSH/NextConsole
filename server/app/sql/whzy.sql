
CREATE TABLE "next_console"."zypricedatainfo" (
  id SERIAL PRIMARY KEY,
  start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  end_time TIMESTAMP NOT NULL DEFAULT '0001-01-01 00:00:00',
  product_name VARCHAR(255) NOT NULL,
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  wholesale_price DOUBLE PRECISION NOT NULL,
  recommended_retail_price DOUBLE PRECISION NOT NULL,
  city VARCHAR(255) NOT NULL,
  purchase_price DOUBLE PRECISION,
  sale_price DOUBLE PRECISION,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
WITH (
    FILLFACTOR = 100,
    OIDS = FALSE
)
;

COMMENT ON TABLE "next_console"."zypricedatainfo"  IS 'ZY产品价格数据信息';
COMMENT ON COLUMN "next_console"."zypricedatainfo".id IS '自增id';
COMMENT ON COLUMN "next_console".zypricedatainfo.start_time IS '数据统计开始时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.end_time IS '数据统计完成时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_name IS '产品名称';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zypricedatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zypricedatainfo.wholesale_price IS '批发价格';
COMMENT ON COLUMN "next_console".zypricedatainfo.recommended_retail_price IS '建议零售价';
COMMENT ON COLUMN "next_console".zypricedatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zypricedatainfo.purchase_price IS '进货价';
COMMENT ON COLUMN "next_console".zypricedatainfo.sale_price IS '出货价';
COMMENT ON COLUMN "next_console".zypricedatainfo.status IS '数据状态';
COMMENT ON COLUMN "next_console".zypricedatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zypricedatainfo.update_time IS '更新时间';
CREATE TRIGGER update_zypricedatainfo_trigger BEFORE UPDATE ON "next_console"."zypricedatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
---------------------------------------------------------------------------------------
CREATE TABLE "next_console".zyinventorydatainfo (
  id SERIAL PRIMARY KEY,
  start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  end_time TIMESTAMP NOT NULL DEFAULT '0001-01-01 00:00:00',
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  product_inventory DOUBLE PRECISION,
  product_remain_days INTEGER,
  city VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE "next_console".zyinventorydatainfo IS 'ZY产品库存数据信息';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.id IS '自增id';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.start_time IS '数据开始时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.end_time IS '数据结束时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_inventory IS '产品库存';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.product_remain_days IS '产品库存可销天数';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.status IS '数据状态';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zyinventorydatainfo.update_time IS '更新时间';

CREATE TRIGGER update_zyinventorydatainfo_trigger BEFORE UPDATE ON "next_console"."zyinventorydatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();


---------------------------------------------------------------------------------------
CREATE TABLE "next_console"."zypurchasedatainfo" (
  id SERIAL PRIMARY KEY,
  start_time VARCHAR(255) NOT NULL,
  end_time VARCHAR(255) NOT NULL,
  product_level VARCHAR(255) NOT NULL,
  product_specification VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  customer_level VARCHAR(255) NOT NULL,
  avg_purchase DOUBLE PRECISION,
  avg_purchase_all DOUBLE PRECISION,
  status VARCHAR(255) NOT NULL DEFAULT '正常',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add table comment
COMMENT ON TABLE "next_console".zypurchasedatainfo IS '产品采购数据信息';

-- Add column comments
COMMENT ON COLUMN "next_console".zypurchasedatainfo.id IS '自增id';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.start_time IS '开始时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.end_time IS '结束时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.product_level IS '产品等级';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.product_specification IS '产品规格';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.city IS '城市';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.customer_level IS '客户等级';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.avg_purchase IS '户均投放条数';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.avg_purchase_all IS '户均进货条数';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.status IS '状态';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.create_time IS '创建时间';
COMMENT ON COLUMN "next_console".zypurchasedatainfo.update_time IS '更新时间';
CREATE TRIGGER update_zypurchasedatainfo_trigger BEFORE UPDATE ON "next_console"."zypurchasedatainfo" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
