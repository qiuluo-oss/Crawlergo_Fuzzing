import json
import re
import subprocess
import simplejson
import requests
import urllib3
from config import config


def get_all_request(target_url):
    """添加http头"""
    # url检测，传入的url是否为完整的域名，若仅为IP+port需要添加协议头
    isHTTPS = True  # 将是否为https首先标志为True
    if ("https" not in target_url) & ("http" not in target_url):
        try:
            url = "https://" + target_url
            requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 忽略ssl验证警告
            requests.get(url=url, verify=False, timeout=3)  # 设置忽略ssl证书安全性警告，设置3s的延迟保证程序健壮性
        except Exception as e:
            isHTTPS = False
        finally:
            if isHTTPS:
                target_url = "https://" + target_url
            else:
                target_url = "http://" + target_url
    return target_url


def crawl_url(url, proxies):
    """爬虫函数"""
    print(f"{config.bcolors.OK}----------开始爬虫: {url} ----------{config.bcolors.ENDC}")

    # 构造文件名
    param_filename = './param/' + url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_') + "_param.txt"

    # 构造crawlergo命令并执行
    if proxies != "":
        cmd = [config.crawlergo_path, "-c", config.chrome_path, "-t", "20", "-f", "smart", "--fuzz-path", "--custom-headers",json.dumps(config.get_random_headers()), "--output-mode", "json", url, "--push-to-proxy", proxies]
    else:
        cmd = [config.crawlergo_path, "-c", config.chrome_path, "-t", "20", "-f", "smart", "--fuzz-path", "--custom-headers",json.dumps(config.get_random_headers()), "--output-mode", "json", url]
    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = rsp.communicate()
    try:
        # 处理爬虫结果
        result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
        # print(result)
    except Exception as e:
        print(f"{config.bcolors.FAIL}----------爬虫失败: {e} ----------{config.bcolors.ENDC}")
        return None, None
    req_list = result["req_list"]
    print(f"{config.bcolors.OK}----------爬虫结束，开始处理爬取结果----------{config.bcolors.ENDC}")
    if req_list:
        for req in req_list:
            url = req['url']
            if '=' in url and '?' in url:
                # 将"http://testhtml5.vulnweb.com/comment?id={{item.value._id}}&username=zhangsan&password=123456"中的=xxx 替换为=FUZZ，不然后面fuzz测试有问题
                modified_url = re.sub(r'=[^&#?/]+', '=FUZZ', url)
                # print(modified_url)
                with open(param_filename, 'a') as f:
                    f.write(modified_url + '\n')
        print(f"{config.bcolors.OK}----------爬取结果处理完成----------{config.bcolors.ENDC}")
        print("\n\t")
    return param_filename