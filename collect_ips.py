import requests
from bs4 import BeautifulSoup
import re

urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html',
    'https://ip.164746.xyz'
]

def fetch_ips_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[错误] 获取 {url} 失败: {e}")
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    # 匹配 IPv4 地址段格式：x.x.x.x/xx 或单独 IP
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b", text)
    print(f"[信息] 从 {url} 获取 {len(ips)} 个 IP")
    return set(ips)

def main():
    all_ips = set()
    for url in urls:
        all_ips.update(fetch_ips_from_url(url))

    if all_ips:
        sorted_ips = sorted(all_ips)
        with open("ip.txt", "w") as f:
            for ip in sorted_ips:
                f.write(ip + "\n")
        print(f"[成功] 共保存 {len(sorted_ips)} 个唯一 IP 到 ip.txt")
    else:
        print("[警告] 未获取到任何 IP，未写入文件。")

if __name__ == "__main__":
    main()