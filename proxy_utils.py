import requests
import random

def get_proxies():
    # URL sudah diganti ke link yang baru
    url = "https://raw.githubusercontent.com/ProxyScrape/free-proxy-list/refs/heads/main/proxies/all/data.txt"
    try:
        response = requests.get(url, timeout=10)
        lines = response.text.strip().split('\n')
        
        valid_proxies = []
        for line in lines:
            if line.strip(): # Memastikan baris tidak kosong
                # Langsung masukkan karena formatnya sudah benar (protokol://ip:port)
                valid_proxies.append(line.strip()) 
                
        return valid_proxies
    except Exception as e:
        print(f"⚠️ Gagal mengambil daftar proxy: {e}")
        return []

def get_random_proxy():
    proxies = get_proxies()
    return random.choice(proxies) if proxies else None