export interface IDepart {
  company_id: number;
  create_time: string;
  department_code: string;
  department_desc: string;
  department_logo: string | null;
  department_name: string;
  department_status: string;
  id: number;
  parent_department_id: number | null;
  update_time: string;
}

export interface IDepartTree extends IDepart {
  children: IDepartTree[];
}

export interface IParentDepart {
  value: string;
  label: string;
  children: IParentDepart[];
  disabled?: boolean;
}

export interface ICompany {
  company_address: string;
  company_area: string;
  company_code: string;
  company_country: string;
  company_desc: string;
  company_email: string | null;
  company_industry: string;
  company_logo: string;
  company_name: string;
  company_phone: string | null;
  company_scale: string;
  company_status: string;
  company_type: string | null;
  company_website: string | null;
  create_time: string;
  id: number;
  parent_company_id: number | null;
}

export interface ICompanyInfo {
  id?: string;
  code?: string;
  name?: string;
  country?: string;
  area?: string;
  address?: string;
  desc?: string;
  status?: string;
  type?: string;
  industry?: string;
  scale?: string;
  phone?: string;
  email?: string;
  website?: string;
}

export interface IDepartForm {
  department_name?: string;
  department_code?: string;
  company_id?: string;
  parent_department_id?: string;
  department_desc?: string;
  department_logo?: string;
  department_status?: string;
  department_id?: string;
}
