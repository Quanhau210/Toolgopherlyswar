import subprocess
import sys

# Hàm cài đặt thư viện
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Cài đặt thư viện pycryptodome và requests nếu chưa có
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except ImportError:
    install("pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

try:
    import requests
except ImportError:
    install("requests")
    import requests  # Import lại sau khi cài đặt

# Các thư viện khác trong code
import random
from datetime import datetime
from atexit import register
from time import sleep, strftime, time
import json, re, sys, random
import threading, base64
import socket
import os

# Lấy ngày và giờ hiện tại
ngay_hien_tai = datetime.now().strftime('%d/%m/%Y')
gio_hien_tai = datetime.now().strftime('%H:%M:%S')

def get_local_ip():
    try:
        # Kết nối đến một địa chỉ ngoài để xác định IP cục bộ
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 1))
        ip_cua_ban = s.getsockname()[0]
    except Exception:
        ip_cua_ban = "Không thể lấy IP cục bộ"
    finally:
        s.close()
    return ip_cua_ban

# Sử dụng hàm lấy IP cục bộ
ip_cuc_bo = get_local_ip()

os.system("clear")

dau = "\033[1;31m[\033[1;37m×.×\033[1;31m] \033[1;37m➩"
banner = f"""
\033[1;33m╔═══════════════════════════════════════════════╗
\033[1;33m║\033[1;35m██╗░░██╗██████╗██████═╗░██╗░░░░██░░░░██╗██████╗\033[1;33m║
\033[1;33m║\033[1;33m██║░░██║██░░░░║██░░░██╝░██║░░░░░██░░██╔╝██░░░░║\033[1;33m║
\033[1;33m║\033[1;39m███████║██████║██████╚╗░██║░░░░░░████╔╝░██████║\033[1;33m║
\033[1;33m║\033[1;36m██╔══██║██░░░░║██╔══██╚╗██║░░░░░░░██╔╝░░░░░░██║\033[1;33m║
\033[1;33m║\033[1;32m██║░░██║██████║██║░░░██║███████╗░░██║░░░██████║\033[1;33m║ 
\033[1;33m║\033[1;30m╚═╝░░╚═╝╚═════╝╚═╝░░░╚═╝╚══════╝░░╚═╝░░░╚═════╝\033[1;33m║ 
\033[1;33m║\033[1;30m░░░░╔██═╗░░╔███╗░░╔═██╗░░██═╗░░░██████═╗░░░░░░░\033[1;33m║ 
\033[1;33m║\033[1;31m░░░░╚╗██╚╗╔╝███╚╗╔╝██╔╝░████╚╗░░██░░░██╝░░░░░░░\033[1;33m║ 
\033[1;33m║\033[1;32m░░░░░╚╗██╚╝██░██╚╝██╔╝░██░░██╚╗░██████╚╗░░░░░░░\033[1;33m║ 
\033[1;33m║\033[1;33m░░░░░░╚╗████╔═╗████╔╝░████████╚╗██╔══██╚╗░░░░░░\033[1;33m║ 
\033[1;33m║\033[1;34m░░░░░░░╚╗██╔╝░╚╗██╔╝░██╔═════██║██║░░░██║░░░░░░\033[1;33m║ 
\033[1;33m║\033[1;35m░░░░░░░░╚══╝░░░╚══╝░░╚═╝░░░░░╚═╝╚═╝░░░╚═╝░░░░░░\033[1;33m║ 
\033[1;33m╠═══════════════════════════════════════════════╣
\033[1;33m║\033[1;34m▶ Nhóm Zalo  : \033[1;35mzalo.me/g/rbpywb976             \033[1;33m║
\033[1;33m║\033[1;34m▶ FaceBook : \033[1;35mfacebook.com/QuanHau210           \033[1;33m║
\033[1;33m║\033[1;34m▶ Zalo : \033[1;35m0961386638                            \033[1;33m║
\033[1;33m║\033[1;34m▶ Mua Key Vip Cứ Liên Hệ Zalo Nhé              \033[1;33m║
\033[1;33m║\033[1;34m▶ Nếu Có Lỗi Vui Lòng Báo Cho Facebook Nhé     \033[1;33m║
\033[1;33m╚═══════════════════════════════════════════════╝
\033[1;32m-------------------------------------------------
"""

# Hàm mã hóa
def encrypt(data, secret_key):
    cipher = AES.new(secret_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Hàm lưu trữ key và IP vào file (sử dụng mã hóa)
def save_key(ip, key):
    secret_key = os.urandom(16)  # Tạo khóa ngẫu nhiên
    data = {'ip': ip, 'key': key, 'timestamp': time()}
    iv, ct = encrypt(json.dumps(data), secret_key)
    with open('KeyToolHerlys.json', 'w') as f:
        json.dump({'iv': iv, 'ct': ct}, f)

def is_key_expired():
    if os.path.exists('KeyToolHerlys.json'):
        with open('KeyToolHerlys.json', 'r') as f:
            data = json.load(f)
            if 'timestamp' not in data:
                return True
            if time() - data['timestamp'] > 86400:  # 86400 giây = 24 giờ
                return True
            else:
                return False
    return True

# Hàm lấy địa chỉ IP của người dùng
def get_ip():
    return requests.get('https://api64.ipify.org?format=json').json()['ip']

# Hàm tạo key dựa trên IP và ngày hiện tại
def create_key(ip):
    ngay = int(strftime('%d'))
    if ':' in ip:  # Kiểm tra địa chỉ IPv6
        ip_part = ip.split(':')[-1]  # Lấy phần cuối của địa chỉ IPv6
    else:  # Địa chỉ IPv4
        ip_part = ip.split('.')[-1]  # Lấy phần cuối của địa chỉ IPv4
    key1 = str(ngay * 9999 + int(ip_part, 16))[-4:]  # Lấy 4 số cuối dựa trên IP
    return 'Herlys-' + key1

for h in banner:
    sys.stdout.write(h)
    sys.stdout.flush()
    sleep(0.0003)

# Kiểm tra và tạo key mới nếu cần thiết
ip = get_ip()
if is_key_expired():
    key = create_key(ip)
    save_key(ip, key)
else:
    with open('KeyToolHerlys.json', 'r') as f:
        data = json.load(f)
        key = data['key']

keyv1 = "HerlysVip3112280520102008"

# Rút gọn URL với khóa key bằng API link4m.co
url = 'keyherlyswar.x10.mx/key.html?key=' + key
token_link1s = '6685a9375cd7941ad61c38f7'
link1s = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link1s}&url={url}').json()
if link1s['status'] == "error":
    print(link1s['message'])
    quit()
else:
    link_key = link1s['shortenedUrl']

# Đọc nội dung từ file KeyToolHerlys.txt
try:
    with open('KeyToolHerlys.txt', 'r') as f:
        thien = f.read()
except FileNotFoundError:
    thien = ""
if thien == keyv1 or thien == key:
    
    sleep(1)
    exec(requests.get('https://c142792b34d14887b6caa3b58025b219.api.mockbin.io/').text)
else:

    print('\033[1;32mTool Free Bạn Vui Lòng Không Đem Bán Nhé !')
    print('\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══')

print('\033[1;33mLink Lấy Key Của Bạn Là :\033[1;31m ' + link_key)
print('\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══')
keynhap = input('\033[1;31m[\033[1;37m×.×\033[1;31m] \033[1;37m➩ \033[1;32mBạn Vui Lòng Nhập Key\033[1;33m :\033[1;36m ')
print("\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══")

if keynhap == key:
    print('\033[1;32mKey Free Của Bạn Đã Đúng, Đăng Nhập Thành Công !')
    print("\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══")
    sleep(2)
    with open('KeyToolHerlys.txt', 'w') as f:
        f.write(keynhap)
    exec(requests.get('https://c142792b34d14887b6caa3b58025b219.api.mockbin.io/').text)
elif keynhap == keyv1:
    print('\033[1;32mKey Vip Của Bạn Đã Đúng, Đăng Nhập Thành Công !')
    print("\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══")
    sleep(2)
    with open('KeyToolHerlys.txt', 'w') as f:
        f.write(keynhap)
    exec(requests.get('https://c142792b34d14887b6caa3b58025b219.api.mockbin.io/').text)
else:
    print('\033[1;33mKey Đăng Nhập Của Bạn Đã Sai !')
    print("\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══\033[1;34m══\033[1;35m══\033[1;36m══\033[1;30m══\033[1;31m══\033[1;32m══\033[1;33m══")
