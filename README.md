# 特色

1、本漏洞库已经拥有OA系列、大华、海康威视、用友、spring、fastjson等21个指纹的漏洞信息，共315个payload，后面会持续更新。

2、对web网站指纹识别后，可采用common模式：只漏扫对应指纹的漏洞，针对性扫描，提升渗透效率。

3、若指纹没有识别出，可采用fuzz模式：crawlergo爬取网页所有包含参数的url，然后使用fuzzing-templates进行FUZZ，用于检测 XSS、SQLi、SSRF、Open-Redirect 等。Web 应用程序中的漏洞。


# 功能及流程介绍

1、若设置代理，验证代理的可用性。

2、httpx对输入的域名进行存活验证，若存活，则进行下一步；反之直接结束。

3、针对网站识别web指纹，若模式为common，则扫描对应指纹的漏洞。

4、若域名存活，crawlergo爬取网页所有包含参数的url，然后进行FUZZ，用于检测 XSS、SQLi、SSRF、Open-Redirect 等。Web 应用程序中的漏洞。

5、该项目有三种模式，一种是COMMON（使用nuclei-templates对目标进行扫描）；一种是FUZZ（使用fuzzing-templates对目标FUZZ）；另外一种是ALL（COMMON和FUZZ）。

6、针对模式，建议使用fuzz，不要使用all，速度会很慢，后面会慢慢优化。


# 输出

## fuzz模式
![image](https://github.com/qiuluo-oss/Crawlergo_Fuzzing/assets/72497146/ef5e5927-96bd-4c99-86ed-bbc01b61bad1)

## common模式
![image](https://github.com/qiuluo-oss/Crawlergo_Fuzzing/assets/72497146/c68df50f-7d05-4601-859b-348b29b22296)


# 参数介绍

usage: Crawlergo_Fuzzing.py [-h] [-u URL] [-f FILE] [-m MODEL]

options:
  -h, --help            show this help message and exit

  -u URL, --url URL     The scan url

  -f FILE, --file FILE  The scan ip list file

  -m MODEL, --model MODEL
                        The scan model, They are: common, fuzz, all


# 安装

1、在config/config.py配置相关工具的路径及代理配置
![image](https://github.com/qiuluo-oss/Crawlergo_Fuzzing/assets/72497146/3a4b07aa-acd2-4d91-b563-9deb68d3c72c)

2、安装依赖库
pip3 install -r requirements.txt


# 使用

### COMMON模式

python3 .\Crawlergo_Fuzzing.py -u testasp.vulnweb.com -m common

### FUZZ模式

python3 .\Crawlergo_Fuzzing.py -u testasp.vulnweb.com -m fuzz

### ALL模式

python3 .\Crawlergo_Fuzzing.py -u testasp.vulnweb.com -m all


# 未来开发计划

1、针对common模式：编写更多漏洞库。

2、针对fuzz模式：优化规则、新增规则。


### 本程序仅供于学习交流，请使用者遵守《中华人民共和国网络安全法》，勿将此工具用于非授权的测试，程序开发者不负任何连带法律责任。
