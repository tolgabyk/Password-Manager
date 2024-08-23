from cryptography.fernet import Fernet
import os

# Şifreleme anahtarını oluştur veya yükle
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    return key

# Şifreleme ve çözme işlemleri
def encrypt_password(key, password):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Şifreleri dosyaya kaydetme
def save_password(site_name, encrypted_password):
    with open("passwords.txt", "a") as file:
        file.write(f"{site_name}:{encrypted_password.decode()}\n")

# Şifreleri görüntüleme
def view_passwords(key):
    if os.path.exists("passwords.txt"):
        with open("passwords.txt", "r") as file:
            for line in file.readlines():
                site_name, encrypted_password = line.strip().split(":")
                decrypted_password = decrypt_password(key, encrypted_password.encode())
                print(f"Site: {site_name} | Şifre: {decrypted_password}")
    else:
        print("Henüz kayıtlı şifre yok.")

# Ana menü
def main():
    key = load_key()

    while True:
        choice = input("Ne yapmak istiyorsunuz? (kaydet/görüntüle/çıkış): ").lower()
        if choice == "kaydet":
            site_name = input("Site adını girin: ")
            password = input("Şifreyi girin: ")
            encrypted_password = encrypt_password(key, password)
            save_password(site_name, encrypted_password)
            print("Şifre kaydedildi!")
        elif choice == "görüntüle":
            view_passwords(key)
        elif choice == "çıkış":
            break
        else:
            print("Geçersiz seçenek, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
