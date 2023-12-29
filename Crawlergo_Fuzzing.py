import httpx
from config import config
from domain_httpx import domain_httpx
from domain_Crawlergo import domain_Crawlergo
from domain_common import common
from domain_fuzz import fuzz
import sys
import argparse
import os
from domain_finger import finger


def process_url_all(url, param_filename, cms, proxies):
    """all模式扫描"""
    if os.path.exists(param_filename):
        fuzz.process_url_fuzz(url, param_filename, proxies)
    else:
        print(f"{config.bcolors.FAIL}{param_filename} does not exist{config.bcolors.ENDC}")

    common.process_url_common(url, cms, proxies)


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython3 ' + sys.argv[0] + " -u testhtml5.vulnweb.com -m fuzz")
    parser.add_argument("-u", "--url", help="The scan url")
    parser.add_argument("-f", "--file", help="The scan ip list file")
    parser.add_argument("-m", "--model", help="The scan model, They are: common, fuzz, all", default="fuzz")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


if __name__ == '__main__':
    # 随机生成user-agent
    headers = config.get_random_headers()
    # 若param、result文件夹不存在，创建
    config.ensure_directories_exist(['./param/', './result/'])

    # 验证代理是否可用
    proxies = dict()
    proxy_one = ""
    try:
        proxies = config.proxies
        proxy_one = proxies["http://"]

        check_ip = httpx.get('http://icanhazip.com/', headers=headers, proxies=proxies)
        check_ip = check_ip.text.replace("\n", "")
        if check_ip == config.ip:
            print(f"{config.bcolors.OK}---------- 代理：{config.ip} 可以正常使用  ----------{config.bcolors.ENDC}")
            print("\n\t")
    except Exception as e:
        print(f"{config.bcolors.FAIL}代理没有设置或代理无效，详情：{e}{config.bcolors.ENDC}")
        print("\n\t")

    args = parse_args()

    if args.url:
        url = sys.argv[2]
        # 若没有http://或https，则添加
        url = domain_Crawlergo.get_all_request(url)

        # 验证域名是否存活
        status_httpx = domain_httpx.domain_verify(url, headers, proxies)
        if status_httpx == True:
            print(f"{config.bcolors.OK}---------- {url} 可以正常访问 ----------{config.bcolors.ENDC}")
            print("\n\t")

            # 指纹识别
            cms_res = finger.finger(url)

            if args.model == "all":
                try:
                    param_filename = domain_Crawlergo.crawl_url(url, proxy_one)
                    process_url_all(url, param_filename, cms_res, proxy_one)
                except Exception as e:
                    print(f"{config.bcolors.FAIL}{e} does not exist{config.bcolors.ENDC}")
            elif args.model == "fuzz":
                try:
                    param_filename = domain_Crawlergo.crawl_url(url, proxy_one)
                    fuzz.process_url_fuzz(url, param_filename, proxy_one)
                except Exception as e:
                    print(f"{config.bcolors.FAIL}{e} does not exist{config.bcolors.ENDC}")
            elif args.model == "common":
                common.process_url_common(url, cms_res, proxy_one)
            else:
                print(f"{config.bcolors.FAIL}语法错误！请执行[python3 main.py -h]查看语法帮助！{config.bcolors.ENDC}")
        else:
            print(f"{config.bcolors.FAIL}---------- {url} 无法访问 ----------{config.bcolors.ENDC}")

    elif args.file:
        filename = sys.argv[2]
        for url in open(filename, encoding="utf-8"):
            url = url.replace("\n", "")
            # 若没有http://或https，则添加
            url = domain_Crawlergo.get_all_request(url)

            # 验证域名是否存活
            status_httpx = domain_httpx.domain_verify(url, headers, proxies)
            if status_httpx == True:
                print(f"{config.bcolors.OK}---------- {url} 可以正常访问 ----------{config.bcolors.ENDC}")
                print("\n\t")

                # 指纹识别
                cms_res = finger.finger(url)

                if args.model == "all":
                    try:
                        param_filename = domain_Crawlergo.crawl_url(url, proxy_one)
                        process_url_all(url, param_filename, cms_res, proxy_one)
                    except Exception as e:
                        print(f"{config.bcolors. FAIL}: {e}")
                elif args.model == "fuzz":
                    param_filename = domain_Crawlergo.crawl_url(url, proxy_one)
                    fuzz.process_url_fuzz(url, param_filename, proxy_one)
                elif args.model == "common":
                    common.process_url_common(url, cms_res, proxy_one)
                else:
                    print(f"{config.bcolors.FAIL}语法错误！请执行[python3 main.py -h]查看语法帮助！{config.bcolors.ENDC}")
            else:
                print(f"{config.bcolors.FAIL}---------- {url} 无法访问 ----------{config.bcolors.ENDC}")
                continue