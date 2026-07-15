import time
import random
import threading
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

# Import dari file terpisah yang sudah dibuat
from proxy_utils import get_random_proxy
from data_generator import generate_random_email, generate_random_password, generate_random_string

# Tambahkan ini di bagian atas script Anda (di luar fungsi)
success_count = 0

def create_account():
    global success_count

    # Setup proxy
    proxy = get_random_proxy()
    if not proxy:
        print("❌ No proxies available!")
        return False

    # Setup user agent
    ua = UserAgent()
    user_agent = ua.random

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    
    # SENJATA PAMUNGKAS: Jangan tunggu loading sama sekali!
    options.page_load_strategy = 'eager'
    options.add_argument("--headless=new")    
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--window-size=1200,800")

    # Setup driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Beri waktu maksimal 30 detik untuk mencari elemen
    driver.implicitly_wait(30) 

    try:
        print(f"[{proxy}] Membuka link referral...")
        driver.get("https://greenlin.run/?ref=28833")
        
        # Berhenti menunggu loading web secara paksa setelah 5 detik
        time.sleep(5)
        driver.execute_script("window.stop();")

        print(f"[{proxy}] Mencari tombol CREATE ACCOUNT...")
        # Mencari tombol Create Account dengan teks (huruf besar/kecil)
        create_btn_xpath = "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create account')]"
        
        create_account_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, create_btn_xpath))
        )
        
        # Paksa klik tombol menggunakan JavaScript (anti gagal)
        driver.execute_script("arguments[0].click();", create_account_button)
        print(f"[{proxy}] Tombol CREATE ACCOUNT berhasil diklik!")
        
        time.sleep(3) # Tunggu animasi form muncul

        # Generate data
        username = generate_random_string(8)
        email = generate_random_email()
        password = generate_random_password()

        print(f"[{proxy}] Mengisi form registrasi...")        
        
        # Isi Username
        login_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @name='login' or @name='username']"))
        )
        login_field.send_keys(username)

        # Isi Email
        email_field = driver.find_element(By.XPATH, "//input[@type='email' or @name='email']")
        email_field.send_keys(email)

        # Isi Password
        password_field = driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
        password_field.send_keys(password)

        print(f"[{proxy}] Submit data...")
        # Klik tombol Register menggunakan JavaScript juga
        submit_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')] | //input[@type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        time.sleep(7) # Tunggu proses loading daftar dari server

        # Cek sukses
        if "Account created successfully" in driver.page_source or "dashboard" in driver.current_url or "games" in driver.current_url:
            success_count += 1
            print(f"✅ BERHASIL DAFTAR {success_count} : {username} | {email} | {password}")

            with open("result.txt", "a", encoding="utf-8") as file:
                file.write(f"{username}|{email}|{password}\n")
                
            return True
        else:
            print(f"❌ GAGAL (Mungkin kena limit/captcha): {username}")
            return False

    except Exception as e:
        print(f"⚠️ ERROR: Gagal menemukan elemen (Web tidak terbuka sempurna / Proxy Mati).")
        return False
    finally:
        driver.quit()

def run_bot_in_threads(num_threads=3, num_accounts=100):
    def worker():
        while True:
            # Berhenti jika target akun sudah tercapai
            with lock:
                if accounts_created[0] >= num_accounts:
                    return
            
            success = create_account()
            
            if success:
                with lock:
                    accounts_created[0] += 1
                    if accounts_created[0] >= num_accounts:
                        return

    accounts_created = [0]
    lock = threading.Lock()
    threads = []

    for _ in range(num_threads):
        t = Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"🎉 Total akun berhasil dibuat: {accounts_created[0]}/{num_accounts}")

if __name__ == "__main__":
    # Jalankan bot dengan 5 thread untuk membuat 20 akun
    run_bot_in_threads(num_threads=3, num_accounts=100)