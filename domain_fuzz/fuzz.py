from config import config
import subprocess


def process_url_fuzz(url, param_filename, proxies):
    """fuzz模式扫描"""
    # 定义输出文件名
    output_fuzz_filename = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_') +"_fuzz.json"

    print(f'{config.bcolors.OK}----------开始fuzzing扫描: {param_filename} ----------{config.bcolors.ENDC}')
    if proxies != "":
        cmd_nuclei = f"{config.nuclei_path} -t {config.fuzzing_template_path} -l {param_filename} -pi {proxies} -o ./result/{output_fuzz_filename}"
    else:
        cmd_nuclei = f"{config.nuclei_path} -t {config.fuzzing_template_path} -l {param_filename} -o ./result/{output_fuzz_filename}"
    print(f"{config.bcolors.OKBLUE}{cmd_nuclei}{config.bcolors.ENDC}")
    try:
        rsp = subprocess.Popen(cmd_nuclei, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = rsp.communicate()
        print(stdout.decode())
        print(f"{config.bcolors.OK}---------- {url} fuzzing扫描结束----------{config.bcolors.ENDC}")
        print("\n\t")
    except FileNotFoundError as e:
        print(f"{config.bcolors.FAIL}Error: {e}{config.bcolors.ENDC}")