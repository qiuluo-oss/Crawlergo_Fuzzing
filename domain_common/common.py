from config import config
import subprocess


def process_url_common(url, proxies):
    """common模式扫描，使用nuclei-template模板扫描"""
    # 定义输出文件名
    output_common_filename = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_') +"_common.json"

    print(f'{config.bcolors.OK}----------开始common扫描: {url} ----------{config.bcolors.ENDC}')
    if proxies != "":
        cmd_nuclei = f"{config.nuclei_path} -u {url} -pi {proxies} -o ./result/{output_common_filename}"
    else:
        cmd_nuclei = f"{config.nuclei_path} -u {url} -o ./result/{output_common_filename}"
    print(f"{config.bcolors.OKBLUE}{cmd_nuclei}{config.bcolors.ENDC}")
    try:
        rsp = subprocess.Popen(cmd_nuclei, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = rsp.communicate()
        print(stdout.decode())
        print(f"{config.bcolors.OK}---------- {url} common扫描结束----------{config.bcolors.ENDC}")
    except FileNotFoundError as e:
        print(f"{config.bcolors.FAIL}Error: {e}{config.bcolors.ENDC}")