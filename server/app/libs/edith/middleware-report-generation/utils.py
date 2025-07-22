#! /usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json

import pandas


class SystemInfo:

    def __init__(self, name):
        self.name = name
        self.leader = ""
        self.ips = list()
        self.total_items = 0
        self.total_pass = 0
        self.total_fail = 0
        self.total_man = 0

    def set_name(self, name):
        self.name = name

    def set_leader(self, leader):
        self.leader = leader

    def append_ip(self, ip):
        self.ips.append(ip)

    def plus_total_items(self):
        self.total_items = self.total_items + 1

    def plus_total_fail(self):
        self.total_fail = self.total_fail + 1

    def plus_total_man(self):
        self.total_man = self.total_man + 1

    def calculation_total_pass(self):
        self.total_pass = self.total_items - (self.total_fail + self.total_man)

    def __eq__(self, other):
        return self.name == other.name


class SystemInfoList:
    list = list()

    def get_system(self, name):
        systemInfo = SystemInfo(name)
        for item in self.list:
            if (item == systemInfo):
                return item
        self.list.append(systemInfo)
        return systemInfo



def load_system_list_from_excel(excel_file):
    system_list = SystemInfoList()
    data = pandas.read_excel(excel_file)
    total_lines = len(data)

    for line in range(total_lines):
        one_system = system_list.get_system(data.loc[line][0])
        if not data.loc[line][1] in one_system.ips:
            one_system.append_ip(data.loc[line][1])
            one_system.set_leader(data.loc[line][2])
    return system_list

def load_error_list_from_excel(excel_file):
    data = pandas.read_excel(excel_file, sheet_name="问题项总览")
    return data


def version_to_num(version):
    nums = version.split(".")
    multiple = pow(10, (len(nums) - 1))
    total = 0
    for int_item in nums:
        if int_item.isdigit():
            total += int(int_item) * multiple
            multiple = multiple / 10
        else:
            total = 0
            break
    return total


def json_to_format_dict_list(file_path):
    dict_list = list()
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as text:
            json_data_utf8 = json.load(text)
            for dict_item in json_data_utf8:
                dict_list.append(dict_item)
    except:
        with open(file_path, 'r', encoding="gbk", errors="ignore") as text:
            json_data_gbk = json.load(text)
            for dict_item in json_data_gbk:
                dict_list.append(dict_item)
    return dict_list


def gate_day_8():
    return datetime.date.today().strftime("%Y%m%d")


def get_day_10():
    return datetime.date.today().strftime("%Y-%m-%d")


# set encoding
def convert(input_json_str):
    if isinstance(input_json_str, dict):
        return {convert(key): convert(value) for key, value in input_json_str.items()}
    elif isinstance(input_json_str, list):
        return [convert(element) for element in input_json_str]
    else:
        return input_json_str


units = {"KB": 1, "K": 1, "MB": 10 ** 3, "M": 10 ** 3, "GB": 10 ** 6, "G": 10 ** 6, "TB": 10 ** 9, "T": 10 ** 9}


def parse_size_to_kb(size_str):
    try:
        size_str_space = size_str.upper().replace("K", " K").replace("M", " M").replace("G", " G").replace("T", " T")
        number, unit = [string.strip() for string in size_str_space.split()]
        return int(float(number) * units[unit])
    except:
        print("Error--->" + size_str)
        return 0


def grep(key, list):
    for item in list:
        if key in item:
            return True, item
    return False, None


def match_first(ip, list):
    for item in list:
        if ip in item:
            return True
    return False


def uniq_dict_list(ll):
    set_temp = set()
    for dict in ll:
        set_temp.add(json.dumps(dict))
    list_final = list()
    for str in set_temp:
        list_final.append(json.loads(str))
    return list_final
