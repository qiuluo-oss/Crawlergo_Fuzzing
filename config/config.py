from colorama import init, Fore, Back, Style
from fake_useragent import UserAgent
import os


class bcolors:
    HEADER = Fore.CYAN
    OKBLUE = Fore.BLUE
    OK = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    ENDC = Fore.RESET
    BOLD = Style.BRIGHT
    UNDERLINE = Style.DIM


def get_random_headers():
    """随机UA头"""
    headers = {'User-Agent': UserAgent().random}
    return headers


def ensure_directories_exist(directories):
    """若目录不存在则创建"""
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


# 相关工具配置路径，不能有中文路径
crawlergo_path = "D:/Crawlergo_Fuzzing/tools/crawlergo/crawlergo.exe"
nuclei_path = "D:/Crawlergo_Fuzzing/tools/nuclei/nuclei.exe"
fuzzing_template_path = "D:/Crawlergo_Fuzzing/tools/fuzzing-templates"
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# 只能配置ehole的绝对路径，不能包含ehole.exe
ehole_path = "D:/Crawlergo_Fuzzing/tools/ehole/"


# 设置全局代理
# socks5
ip = 'xx.xx.xx.xx'
port = 1080
username = 'xxx'
password = 'xxx'
proxies = {
	'http://': f'socks5://{username}:{password}@{ip}:{port}',
	'https://': f'socks5://{username}:{password}@{ip}:{port}'
}
# http代理
# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }
