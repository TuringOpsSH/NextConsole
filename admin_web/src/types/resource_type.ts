import {UploadRawFile} from "element-plus";
import {Users} from "@/types/users";
import {Colleague, Company, Department, Friend} from "@/types/contacts";

export interface ResourceItem{
    id?: number;
    resource_parent_id?: number;
    user_id?: number;
    resource_name?: string;
    resource_type?: string;
    resource_type_cn?: string | null;
    resource_title?: string;
    resource_desc?: string;
    resource_icon?: string;
    resource_format?: string;
    resource_size_in_MB?: number;
    resource_path?: string | null;
    resource_status?: string;
    resource_source?: string| null;
    resource_source_url?: string | null;
    resource_show_url?: string |null;
    resource_download_url?: string | null;
    resource_feature_code?: string | null;
    rag_status?: string |null;
    resource_language?: string | null;
    create_time?: string;
    update_time?: string;
    delete_time?: string | null;
    show_buttons?: boolean | null;
    resource_is_selected?: boolean | null;
    resource_parent_name?: string | null;
    sub_resource_dir_cnt?: number | null;
    sub_resource_file_cnt?: number | null;
    sub_rag_file_cnt?: number | null;
    resource_is_supported?: boolean | null;
    resource_view_support?: boolean | null;
    resource_content?: string | null;
    ref_text?: string | null;
    rerank_score?: number | null;
    resource_tags?: ResourceTag[] | null;
    author_info?: Users | null;
    access_list?: string[];
    [property: string]: any;
}
export interface ResourceUploadItem{
    id: number| null;
    resource_parent_id: number| null;
    resource_id: number| null;
    resource_name: string| null;
    resource_size_in_mb: number| null;
    resource_type: string| null;
    resource_format: string| null;
    content_max_idx: number| null;
    content_finish_idx: number| null;
    resource_md5: string| null;
    task_icon: string| null;
    task_source: string | null;
    task_status: string| null;
    create_time: string| null;
    update_time: string| null;
    raw_file: UploadRawFile | null;
    task_error_msg?: string | null;
}
export interface ResourceShortCut{
    id: number;
    user_id: number;
    resource_id: number;
    resource_name: string;
    resource_icon: string;
    shortcut_status: string;
    create_time: string;
    update_time: string;
}
export interface ResourceType{
    icon: string;
    title: string;
    type: string;
    show: boolean;
}
export interface ResourceTag{
    id: number | null;
    user_id?: number | null;
    tag_name: string | null;
    tag_value: string | null;
    tag_type: string | null;
    tag_source: string | null;
    tag_desc: string | null;
    tag_color: string| null;
    tag_icon: string| null;
    tag_status?: string| null;
    create_time?: string;
    update_time?: string;
    tag_count?: number | null;
    tag_active?: boolean | null;
}
export interface ResourceAccess{
    type: string;
    id: number;
    auth_type: string;
    meta?: Friend | Company | Department | Colleague;
}
/**
 * resource_download_cooling_record，资源下载冷却记录表
 */
export interface ResourceDownloadCoolingRecord {
    /**
     * 作者是否允许继续下载，作者是否允许继续下载
     */
    author_allow?: boolean;
    /**
     * 作者新增次数，作者新增次数
     */
    author_allow_cnt?: number;
    /**
     * 资源作者id，资源作者id
     */
    author_id?: number;
    /**
     * 是否通知作者，是否通知作者
     */
    author_notice?: boolean;
    /**
     * 创建时间，创建时间
     */
    create_time?: string;
    /**
     * ID 编号，ID 编号
     */
    id?: number;
    /**
     * 目标资源id，目标资源id
     */
    resource_id?: number;
    /**
     * 更新时间，更新时间
     */
    update_time?: string;
    /**
     * 目标用户id，目标用户id
     */
    user_id?: number;
    [property: string]: any;
}