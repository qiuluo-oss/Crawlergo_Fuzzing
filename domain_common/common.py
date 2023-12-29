from config import config
import subprocess
import os
import sqlite3


def cms_temptales(cms):
    """
    根据指纹识别的结果，返回对应的template名称。方便后续漏扫
    """
    # 提取cms中的指纹逗号前的第一个值，为了防止误扫描
    cms = cms.split("|")[1]
    if "," in cms:
        cms = cms.split(",")[0]

    templates_name_list = set()

    # 创建链接
    db_path = os.getcwd() + "\\domain_common\\" + "cms_templates.db"
    # print(db_path)
    con = sqlite3.connect(db_path)
    # 创建游标对象
    cur = con.cursor()
    # 编写sql语句
    cms_name = "select id, cms_name from cms_templates_name"
    # 执行语句
    try:
        cur.execute(cms_name)
        # 获取结果集，获取所有数据
        cms_name_all = cur.fetchall()
        for cms_name_info in cms_name_all:
            if cms_name_info[1] in cms:
                templates_name = f"select template_name from cms_templates_name where id={cms_name_info[0]}"
                cur.execute(templates_name)
                templates_name_all = cur.fetchall()

                # 将数据库查询出来的template_name添加到templates_name_list列表中
                for template_name_all in templates_name_all:
                    if template_name_all[0] !="0":
                        templates_name_list.add(template_name_all[0])
    except Exception as e:
        print(f"{config.bcolors.FAIL}Error: {e}{config.bcolors.ENDC}")
    finally:
        cur.close()
        con.close()
    templates_name_list = list(templates_name_list)
    return templates_name_list


def process_url_common(url, cms, proxies):
    """common模式扫描，使用nuclei-template模板扫描"""
    # 定义输出文件名
    output_common_filename = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_') +"_common.json"
    # common_templates路径
    path = os.getcwd() + "\\domain_common\\common_templates\\"

    templates_name = cms_temptales(cms)
    for template_name in templates_name:
        template_name_path = path + template_name
        # print("template_name_path:", template_name_path)
        print(f'{config.bcolors.OK}----------开始common模式{template_name}扫描: {url} ----------{config.bcolors.ENDC}')
        print(f'{config.bcolors.OK}---------- 请注意：若没有任何输出，则代表没有漏洞 ----------{config.bcolors.ENDC}')
        if proxies != "":
            cmd_nuclei = f"{config.nuclei_path} -t {template_name_path} -u {url} -pi {proxies} -o ./result/{output_common_filename}"
        else:
            cmd_nuclei = f"{config.nuclei_path} -t {template_name_path} -u {url} -o ./result/{output_common_filename}"
        print(f"{config.bcolors.OKBLUE}{cmd_nuclei}{config.bcolors.ENDC}")
        try:
            rsp = subprocess.Popen(cmd_nuclei, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = rsp.communicate()
            print(stdout.decode())
            # print(stderr.decode())
            print(f'{config.bcolors.OK}----------结束common模式{template_name}扫描: {url} ----------{config.bcolors.ENDC}')
        except FileNotFoundError as e:
            print(f"{config.bcolors.FAIL}Error: {e}{config.bcolors.ENDC}")

