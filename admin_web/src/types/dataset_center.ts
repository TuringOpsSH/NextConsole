export interface DataSetMeta{
    id: number,
    dataset_name: string,
    dataset_type: string,
    dataset_desc: string,
    instruction_id:number,
    user_id: number,
    dataset_status: number,
    create_time: string,
    update_time: string,
}

export interface DataSetSample{
    id: number,
    msg_id: number,
    session_id: number|null,
    msg_content: string |null,
    user_id: number | null,
    user_name: string | null,
    instruction_id: number,
    sample_desc: string,
    sample_model_name: string,
    sample_params: object,
    sample_prompt: string,
    sample_result: string,
    sample_status: string,
    create_time: string,
    update_time: string,
    tags: DataSetSampleTagsMap[] | null,
}

export interface DataSetSampleRelation{
    id: number,
    data_set_id: number,
    data_sample_id: number,
    rel_status: string,
    create_time: string,
    update_time: string,
}

export interface DataSetSampleTag{
    id: number,
    data_sample_id: number,
    tag_name: string | null,
    tag_desc: string | null,
    tag_type: string | null,
    tag_value_history: string | number| boolean|null,
    tag_value_correct: string | null,
    tag_value_comment: string | null,
    tag_source: string | null,
    tag_status: string | null,
    create_time: string | null,
    update_time: string | null,
}

export interface DataSetSampleTagsMap{
    [key: string]: DataSetSampleTag
}
export interface TagFilter{
    tag_name:string,
    tag_value_history: string[],
    tag_value_correct: string[],
    tag_result: boolean [],
}
export interface DataSetSampleTagFilter{
    [key: string]: TagFilter
}
