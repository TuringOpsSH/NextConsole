#! /usr/bin/python
# -*- coding: UTF-8 -*-

import re
import time
import logging
import os
import sys
import random

log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app.log')
if not os.path.isfile(log_file):
    open(log_file, 'a').close()

logging.basicConfig(level=logging.INFO, filename=log_file, encoding='UTF-8',
                    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    global_pyeek = os.path.join(os.path.dirname(__file__), '../eek-pyeek')
    sys.path.insert(0, global_pyeek)
    import pyeek
except Exception as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)

try:
    buildin_pyeek = os.path.join(os.path.dirname(__file__), './pyeek')
    sys.path.insert(0, buildin_pyeek)
    import pypandoc
except Exception as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)

os.environ['PYPANDOC_PANDOC'] = r'..\eek-pandoc\pandoc.exe'
green = """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAhhJREFUOBGFUz1oU1EU/s57Sf2rtTUIcTCLKPQF3Fo61EU0kEGoFBFXaUGpUwcXUXTpZqcGHbo6STsqKZjFTnZQ1HTwbyiKDiKoCUhf8q7fufe++BIED7x7fu75znfOffcKBuXl5TJ24zkYVAApgQb1DkQ2gO4qJteaWYj0nObFIbTNMvOvERS4uG7bAt6VhP59HJBFlB/tatAVUHDLPIExZ1zmf1aRBoalqkUck2X+B1jJVVT32cxVDEXwfLaMBK/I7tvWcCoDI/TGYTXhOAFOBUiMHhjBTLYsXltWLl6PBHtx4+gMxGjA5lhsDkYqZE8pCcjYPjoS7kN9/DamDp5ETgIsfV73O1LRKiXHwhixp4fHMTM2mWFW8C0LftH6iAdf637P5pfYAQ0dlVLMj+JxdBN7JI9Lb+/h6Y/XqEeOWcFnt+/ie6ftknVNDKGbF/RiRGl0oVjFyvF5xEkH735/QbT/GCy4eceDM4yBbIe4Ep1gC1PpIW61P+Bb/BPnCxM4kj+UAbdc69rt32N6qAU+MXSVh+cHAbZa722R4tAozr1h2/EvD9bTJ1qo9TdC5h3o2ewKTLIwSJGXHGLTYX1fW1U6gQQ1TK9dd5fncLDIpAa3+yQ23T5fD82KQQNjioFeIIo+jEJYZVs125rm2Y9LT9PQtgU1FHL2HSjU96aml0292t05ehUkfM42w+zQ30AYrrLtvuf8ByY83PV7FnYXAAAAAElFTkSuQmCC"""
orange = """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAfNJREFUOBF1Uz1vE0EQnTnWhyCXD4xzhYtghHSNnRRIFJElSmgip6LgF0TiT0T+FxTQIVGDaECijNKTuLnKShGkk+XgcCHxhbvJvD2tdRhnpLnZnZn3ZnZ3jmlO5Eu3R+lony6TNl2nvg3XgozuhQMKGn3eOfhchbDbyNcXSzQaHtIk7oiQ9bN+dU2wVpiEVqNjetja5pffLuCzIQv+eXxS/D6tO1CJWPzloDnmZmcDJB5SJBkeFuendeUnKeAolXe/E9TtnRUtBAywRj51e8XwAG3/J7z8yPos6Xx0rEdVrCkmo31NKI+iJAuPgK4gyEIhtbgnYI2kSbtaYVEn1Th4ZqJYI1epf2uCq7agA5DwNPWNbemWBFsJJFDInC0U54kJMnRgNa9YXTuZxZXArmFVWQfM8P1wIBdnT5GMAu6esL/+8Lz0IaACsL1k1/FSOPB4tdFXNkE7pOos1hy9Iu/JDhXaDRRszuIheFlHG8zZ2+hHnsSbWFfFfxMTTSeUvX9m3e6JYb0wOvL34i2DSO1xa5um6Ul+ptNYOUP2ToE5LqakRXcA80pzXGsphmKyo4yZrj3obHjr0ZGmyuzS/kxIpikJOFQVLF5DK9fL/wC09gglf/n9+7Hby3/pdJ4n7ULf2SbcDTJvJRzcWWv0zet/f+cbbAMC96+Q6dUAAAAASUVORK5CYII="""
red = """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAlpJREFUOBF9U0tPFEEQ/qp7Zh+s+1TxoAETIh5WPRgPcCHiAU1MNvwcozGE+EBD/C/GxAsXjRc8eJDFPXAyGhDhAIiuKzN0l1U9LIKJVtJT1TX11ePrbsJf0r092UpMPMM2apKNc8wMYpeQSzuxS2dLL1+9OAqh/oanpko7BV6ELV5iIPj1I3a2yTSz632o/aJxWljoKjYEBnCePnsTN0g8UvS/It1s1RMe0iRGI7djt+gpaiiSvaA1Q1j+iP5js4kailEs7d6aaKXRwHOBSO2saTtyAf7rOtDthhFMtQpTq2P/00eJIPEJL5I63v85bRLQjBAlXq3uYUdGUHn8BOUHj4BiESiXUda9LHv2XIgJsYJRbMSImhBgJgS3tga3uop4dBTlh3OgQh7R0DDSdhv7GxsIsdpoENukzZs3BK3UqWQjUOkEqnNPJcnF4E3aS/h2/x6wtyd7ZTgL17YjKGmHGfWniLWgfD6z5UuFAsiarP1QI4tjeBj2LtHZw3LSTKWC2vwzRMPnkSy9R7qyEjqpzs0DA0WwxDBnS4wkMkg73ueuajll11ZrgXEF79y9E7qpS0Jz8hSoXAF//yG4rANDaYd2J8daPY6yYzy4RVaqu80NcK8n7EjPAyXoUfr1LwGsPvFyDul0mH7z+ljbsb18OPQ/jDC+/FNtyC0Pvn57JdzE07nKuGG3FY5ISdVjDatvqxbK+j6JVYzWCQn0Tg8WKkMy07KwKRwdkOpdRm7QTl4ls6Fk+YzEHntMmqkv2xPXWgljxjM12VMu0AJOLHEnZzBbf/Pu2HP+De1xQitTK57BAAAAAElFTkSuQmCC"""
blank = """&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;"""


def ymd():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


ymd = ymd()

CHAPTER_LEVEL = """
# 告警级别定义

告警定义如下：

|风险等级|颜色|标识|定义|
|:---|:---|:---|:---|
|高风险|红色|![]({})|经检查发现的最高级别告警，告警级别基于工程师从问题严重性、时间紧迫性、影响范围等方面的判断，建议及时进行处理。|
|中风险|橙色|![]({})|经检查发现的中等级别告警，一般为仍然处在发展变化过程中且尚未转化为高风险告警的问题，建议关注问题发展趋势，结合实际情况进行处理。|
|低风险|绿色|![]({})|包括经检查未发现问题的，或虽然存在问题但一般情况下影响可以忽略的告警。此外，对于最佳实践方面的检查结果也归为此类。|

""".format(red, orange, green)

DANGER_IMG = "![]({})".format(red)
WARN_IMG = "![]({})".format(orange)
OK_IMG = "![]({})".format(green)

CHAPTER_PLAN = """# 重要告警及处理计划

下表为重要告警及处理进度。如为“待服务台安排人员处理”，后续项目经理会跟踪直到解决，如状态为“等客户通知再处理”，还请您密切关注，发现问题及时联系项目经理安排处理。

涉及IP地址|异常问题|实例名|处理建议|处理进度（已现场处理/客户自行处理/待服务台安排人员处理/等客户通知再处理）|备注|
|:---|:---|:---|:---|:---|:---|
|||||||
"""


CHAPTER_SUMMARY = """# 巡检告警详情汇总

## 告警数量统计

按应用系统及IP地址进行的统计结果列表如下：

|应用系统|IP地址|高风险告警数量|中风险告警数量|正常数量|
|:---|:---|:---|:---|:---|
"""


CHAPTER_LIST_DANGER = """
## 风险及建议列表

### 高风险

|IP地址|进程|类型|检查内容|当前值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
"""

CHAPTER_LIST_WARN = """### 中风险

|IP地址|进程|类型|检查内容|当前值|告警|建议|
|:---|:---|:---|:---|:---|:---|:---|
"""

CHAPTER_LIST_OK = """### 正常

|IP地址|进程|类型|检查内容|当前值|告警|
|:---|:---|:---|:---|:---|:---|
"""

CHAPTER_LIST_INFO = """# 中间件基本信息

|IP地址|进程|类型|项目|当前值|
|:---|:---|:---|:---|:---|
"""

CHAPTER_LIST_ONLY_NAME = """# 检查项列表

|巡检项名称|巡检项名称|
|:---|:---|
"""


def write_to_summary_word(datadir, system_stat_list):
    report_dir = os.path.join(datadir, 'report')
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)

    preset = pyeek.PreSet()
    user = preset.get('name')
    if not user:
        user = "(工程师姓名)"

    CHAPTER_META = """
---
title: 中间件健康检查汇总报告
subtitle:
author:
- 工程师:{}
date: {}
---

"""

    mdfile = os.path.join(
        report_dir, "中间件健康检查汇总报告-{}.md".format(ymd.replace('-', '', -1)))

    names = ['张立志', '王天桥',]
    CHAPTER_VERSION = """# 文档版本信息

|版本|日期&#160;&#160;&#160;&#160;&#160;&#160;|作者&#160;&#160;&#160;&#160;&#160;&#160;|说明&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{}|{}|编写|
|2|{}|{}|审核|
|||||
""".format(ymd, user, ymd, random.sample(names, 1)[0])

    with open(mdfile, "w", encoding="UTF-8") as f:
        f.write(CHAPTER_META.format(user, ymd))
        f.write(CHAPTER_VERSION)
        f.write(CHAPTER_LEVEL)
        f.write(CHAPTER_PLAN)

        ext = ''
        for data in system_stat_list:
            for w in data['summary']:
                ext += '|' + '|'.join(
                    [data['summary'][w]['name'], w, str(data['summary'][w]['danger']), str(data['summary'][w]['warn']), str(data['summary'][w]['ok'])]) + '|\n'
        # md中$要进行转义，否则pandoc无法处理
        ext = ext.replace('$', r'\$')
        f.write(CHAPTER_SUMMARY + ext)

        ext = ''
        for data in system_stat_list:
            for w in data['result_fail']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('不符合', DANGER_IMG), w[8] + '。' + w[6]]) + '|\n'
        ext = ext.replace('$', r'\$')
        f.write(CHAPTER_LIST_DANGER + ext)

        ext = ''
        for data in system_stat_list:
            for w in data['result_man']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('人工复核', WARN_IMG), w[8] + '。' + w[6]]) + '|\n'
        ext = ext.replace('$', r'\$')
        f.write(CHAPTER_LIST_WARN + ext)

        ext = ''
        for data in system_stat_list:
            for w in data['result_ok']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('符合', OK_IMG)]) + '|\n'
        ext = ext.replace('$', r'\$')
        f.write(CHAPTER_LIST_OK + ext)

        f.write(CHAPTER_LIST_ONLY_NAME)

    try:
        pypandoc.convert_file(source_file=mdfile,
                              to="docx",
                              outputfile=mdfile.replace(
                                  ".md", ".docx"),
                              extra_args=['--reference-doc=./templates/template.docx',
                                          '--toc',
                                          '--toc-depth=3',
                                          '--metadata=toc-title:目录'])
        logger.info("* 生成 Word 完成:" + mdfile.replace(
            ".md", ".docx"))
        os.remove(mdfile)
    except Exception as e:
        logger.error(str(e))


def write_to_app_word(datadir, system_stat_list):
    report_dir = os.path.join(datadir, 'report')
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)

    preset = pyeek.PreSet()
    user = preset.get('name')
    if not user:
        user = "(工程师姓名)"

    names = ['张立志', '王天桥',]
    CHAPTER_VERSION = """# 文档版本信息

|版本|日期&#160;&#160;&#160;&#160;&#160;&#160;|作者&#160;&#160;&#160;&#160;&#160;&#160;|说明&#160;&#160;&#160;&#160;&#160;&#160;|
|:---|:---|:---|:---|
|1|{}|{}|编写|
|2|{}|{}|审核|
|||||
""".format(ymd, user, ymd, random.sample(names, 1)[0])

    for data in system_stat_list:
        CHAPTER_META = """
---
title: 中间件健康检查报告
subtitle: {}
author:
- 工程师:{}
date: {}
---

"""

        mdfile = os.path.join(
            report_dir, data['app'] + "- 中间件健康检查报告-{}.md".format(ymd.replace('-', '', -1)))
        with open(mdfile, "w", encoding="UTF-8") as f:
            f.write(CHAPTER_META.format(data.get('app'), user, ymd))
            f.write(CHAPTER_VERSION)
            f.write(CHAPTER_LEVEL)
            f.write(CHAPTER_PLAN)

            ext = ''
            for w in data['summary']:
                ext += '|' + '|'.join(
                    [data['summary'][w]['name'], w, str(data['summary'][w]['danger']), str(data['summary'][w]['warn']), str(data['summary'][w]['ok'])]) + '\n'
            ext = ext.replace('$', r'\$')
            f.write(CHAPTER_SUMMARY + ext)

            ext = ''
            for w in data['result_fail']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('不符合', DANGER_IMG), w[8] + '。' + w[6]]) + '|\n'
            ext = ext.replace('$', r'\$')
            f.write(CHAPTER_LIST_DANGER + ext)

            ext = ''
            for w in data['result_man']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('人工复核', WARN_IMG), w[8] + '。' + w[6]]) + '|\n'
            ext = ext.replace('$', r'\$')
            f.write(CHAPTER_LIST_WARN + ext)

            ext = ''
            for w in data['result_ok']:
                ext += '|' + '|'.join(
                    [w[1], w[2], w[3], w[4], w[7], w[5].replace('符合', OK_IMG)]) + '|\n'
            ext = ext.replace('$', r'\$')
            f.write(CHAPTER_LIST_OK + ext)


            ext = ''
            for w in data['result_info']:
                    ext += '|' + '|'.join(
                        [w[1], w[2], w[3], w[4], w[7]]) + '|\n'
            ext = ext.replace('$', r'\$')
            f.write(CHAPTER_LIST_INFO + ext)

        #try提出with，修改中间件基本信息没写入md就进行转换docx的问题
        try:
            pypandoc.convert_file(source_file=mdfile,
                                  to="docx",
                                  outputfile=mdfile.replace(
                                      ".md", ".docx"),
                                  extra_args=['--reference-doc=./templates/template.docx',
                                              '--toc',
                                              '--toc-depth=3',
                                              '--metadata=toc-title:目录'])
            logger.info("* 生成 Word 完成:" + mdfile.replace(
                ".md", ".docx"))
        except Exception as e:
            logger.error(str(e))
        os.remove(mdfile)
