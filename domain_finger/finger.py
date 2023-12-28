import subprocess
from config import config
import os


def finger(url):
    """指纹识别，使用ehole进行识别"""
    print(f"{config.bcolors.OK}----------指纹识别开始: {url} ----------{config.bcolors.ENDC}")

    # 构造ehole命令并执行
    old_path = os.getcwd()
    os.chdir(config.ehole_path)
    # cmd = ["ehole.exe", "finger", "-u", url, "-p", proxies]
    cmd = ["ehole.exe", "finger", "-u", url]
    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()
    result = output.decode().split("\n")[1]
    print(result)
    print(f"{config.bcolors.OK}----------指纹识别结束: {url} ----------{config.bcolors.ENDC}")
    print("\n\t")
    os.chdir(old_path)