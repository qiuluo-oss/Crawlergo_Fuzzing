import httpx
from config import config

def domain_verify(url, headers, proxies):
    """
    验证域名的存活
    """
    status_httpx = False
    try:
        res = httpx.get(url, headers=headers, proxies=proxies, timeout=3, verify=False)
        status_code = res.status_code    # 状态
        if status_code in [200, 301, 302, 401, 403]:
            status_httpx = True
    except Exception as e:
        print(f"{config.bcolors.FAIL}----- 域名存活验证报错：{e} -----{config.bcolors.ENDC}")
    return status_httpx



