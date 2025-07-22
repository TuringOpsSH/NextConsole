#! /usr/bin/python
# -*- coding: UTF-8 -*-


def param(val):
    if val == "进程ID" or val.startswith("进程类型") or val == "服务器概况" or val == "进程命令行" or val == "内核参数检查":
        return "background-color : %s" % "#B0E0E6"
    elif val == "----split----":
        return "background-color : %s" % "#FAEBD7"
    else:
        return None


def result(val):
    if val == "不符合":
        return "background-color : %s" % "#F08080"
    elif val == "人工复核":
        return "background-color : %s" % "#FFFACD"
    elif val == "符合":
        return "background-color : %s" % "#98FB98"
    elif val == "------------":
        return "background-color : %s" % "#FAEBD7"
    else:
        return None


def split(val):
    if val == "------------":
        return "background-color : %s" % "#FAEBD7"
    else:
        return None


def set_width_ip_data(writer, current_ip):
    worksheet = writer.sheets[current_ip]
    worksheet.column_dimensions["A"].width = 30
    worksheet.column_dimensions["B"].width = 15
    worksheet.column_dimensions["C"].width = 55
    worksheet.column_dimensions["D"].width = 50
    worksheet.column_dimensions["E"].width = 50



def set_width_ip_list(writer):
    worksheet = writer.sheets["服务器列表"]
    worksheet.column_dimensions["A"].width = 25
    worksheet.column_dimensions["B"].width = 25
    worksheet.column_dimensions["C"].width = 25



def set_width_result(writer):
    worksheet = writer.sheets["问题项总览"]
    worksheet.column_dimensions["A"].width = 15
    worksheet.column_dimensions["B"].width = 10
    worksheet.column_dimensions["C"].width = 30
    worksheet.column_dimensions["D"].width = 15
    worksheet.column_dimensions["E"].width = 40
    worksheet.column_dimensions["F"].width = 25
    worksheet.column_dimensions["G"].width = 30


def set_width_system(writer):
    worksheet = writer.sheets["系统列表"]
    worksheet.column_dimensions["A"].width = 30
    worksheet.column_dimensions["B"].width = 20
    worksheet.column_dimensions["C"].width = 10
    worksheet.column_dimensions["D"].width = 10
    worksheet.column_dimensions["E"].width = 18
    worksheet.column_dimensions["F"].width = 25
    worksheet.column_dimensions["G"].width = 25
