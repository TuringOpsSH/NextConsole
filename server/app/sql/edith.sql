CREATE TABLE "next_console"."edith_client_meta_info" (
  id SERIAL PRIMARY KEY,
  client_name VARCHAR(255) NOT NULL,
  client_desc VARCHAR(255) NOT NULL,
  client_icon TEXT NOT NULL,
  support_os TEXT,
  client_version VARCHAR(255) NOT NULL,
  client_sub_version VARCHAR(255) NOT NULL,
  client_raw_path TEXT NOT NULL,
  client_download_path TEXT NOT NULL,
  client_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "next_console"."edith_client_meta_info" IS 'edith版本信息';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_name IS '客户端名称';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_desc IS '客户端描述';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_icon IS '客户端图标';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".support_os IS '支持操作系统';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_version IS '版本号';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_sub_version IS '子版本号';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_raw_path IS '客户端原始路径';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_download_path IS '客户端下载路径';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".client_status IS '客户端状态';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_client_meta_info".update_time IS '更新时间';

CREATE TRIGGER update_edith_client_meta_info_trigger BEFORE UPDATE ON "next_console"."edith_client_meta_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."edith_report_info" (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  edith_task_id INTEGER NOT NULL,
  report_code VARCHAR(255) NOT NULL,
  report_name TEXT NOT NULL,
  report_desc TEXT,
  report_type VARCHAR(255) NOT NULL,
  report_data_dir TEXT NOT NULL,
  report_generate_config VARCHAR(255) NOT NULL,
  celery_id VARCHAR(255),
  task_trace TEXT,
  report_path TEXT,
  report_download_url TEXT,
  report_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  run_model VARCHAR(20)
);

-- 表注释
COMMENT ON TABLE "next_console"."edith_report_info" IS 'edith巡检报告信息表';

-- 列注释
COMMENT ON COLUMN "next_console"."edith_report_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_report_info".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."edith_report_info".edith_task_id IS 'edith巡检任务id';
COMMENT ON COLUMN "next_console"."edith_report_info".report_code IS '报告编号';
COMMENT ON COLUMN "next_console"."edith_report_info".report_name IS '报告名称';
COMMENT ON COLUMN "next_console"."edith_report_info".report_desc IS '报告描述';
COMMENT ON COLUMN "next_console"."edith_report_info".report_type IS '报告类型';
COMMENT ON COLUMN "next_console"."edith_report_info".report_data_dir IS '报告数据目录';
COMMENT ON COLUMN "next_console"."edith_report_info".report_generate_config IS '报告生成配置';
COMMENT ON COLUMN "next_console"."edith_report_info".celery_id IS '任务id';
COMMENT ON COLUMN "next_console"."edith_report_info".task_trace IS '任务日志';
COMMENT ON COLUMN "next_console"."edith_report_info".report_path IS '报告路径';
COMMENT ON COLUMN "next_console"."edith_report_info".report_download_url IS '报告下载地址';
COMMENT ON COLUMN "next_console"."edith_report_info".report_status IS '报告状态';
COMMENT ON COLUMN "next_console"."edith_report_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_report_info".update_time IS '更新时间';
COMMENT ON COLUMN "next_console"."edith_report_info".run_model IS '运行模式';

CREATE TRIGGER update_edith_report_info_trigger BEFORE UPDATE ON "next_console"."edith_report_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();

------------------------------------------------------------

CREATE TABLE "next_console"."edith_task_info" (
  id SERIAL PRIMARY KEY,
  task_code VARCHAR(255) NOT NULL,
  session_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  task_name VARCHAR(255) NOT NULL,
  task_desc VARCHAR(255) NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  task_stage VARCHAR(255) NOT NULL,
  task_data_dir TEXT NOT NULL,
  edith_client_id INTEGER,
  task_parent_id INTEGER,
  task_status VARCHAR(255) NOT NULL,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 表注释
COMMENT ON TABLE "next_console"."edith_task_info" IS 'edith巡检任务信息表';

-- 列注释
COMMENT ON COLUMN "next_console"."edith_task_info".id IS '自增id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_code IS '巡检任务编号';
COMMENT ON COLUMN "next_console"."edith_task_info".session_id IS '会话id';
COMMENT ON COLUMN "next_console"."edith_task_info".user_id IS '用户id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_name IS '任务名称';
COMMENT ON COLUMN "next_console"."edith_task_info".task_desc IS '任务描述';
COMMENT ON COLUMN "next_console"."edith_task_info".task_type IS '任务类型';
COMMENT ON COLUMN "next_console"."edith_task_info".task_stage IS '任务阶段';
COMMENT ON COLUMN "next_console"."edith_task_info".task_data_dir IS '任务上传数据目录';
COMMENT ON COLUMN "next_console"."edith_task_info".edith_client_id IS 'edith客户端id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_parent_id IS '父任务id';
COMMENT ON COLUMN "next_console"."edith_task_info".task_status IS '任务状态';
COMMENT ON COLUMN "next_console"."edith_task_info".create_time IS '创建时间';
COMMENT ON COLUMN "next_console"."edith_task_info".update_time IS '更新时间';

CREATE TRIGGER update_edith_task_info_trigger BEFORE UPDATE ON "next_console"."edith_task_info" FOR EACH ROW
EXECUTE FUNCTION update_update_time();
