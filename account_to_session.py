import os
import pyfiglet
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from opentele.td import TDesktop
from opentele.api import UseCurrentSession

# Ganti dengan API ID dan Hash Anda
api_id = '2040'
api_hash = 'b18441a1ff607e10a989891a5462e627'

# Buat folder sesi jika belum ada
session_folder = 'sessions_tele'
os.makedirs(session_folder, exist_ok=True)

def print_welcome_message():
    # Membuat efek ASCII art dengan tulisan "MPEANUT"
    ascii_art = pyfiglet.figlet_format("MPEANUT")
    print(ascii_art)
    
    # Menampilkan GitHub username Anda
    print("GitHub: @riskimeji")
    print("Channel Tele: @mpeanutx\n")

async def login_with_phone():
    # Meminta nomor telepon dari pengguna secara manual
    phone_number = input('Masukkan nomor telepon Anda (dengan kode negara, misalnya +62 untuk Indonesia): ')

    # Tentukan path untuk file sesi
    session_file = os.path.join(session_folder, 'telethon_phone.session')

    # Buat instance TelegramClient dengan nama session di folder 'sessions_tele'
    client = TelegramClient(session_file, api_id, api_hash)

    # Hubungkan ke Telegram
    await client.connect()

    # Jika session tidak tersimpan, lakukan login dengan nomor telepon
    if not await client.is_user_authorized():
        print(f"Login menggunakan nomor {phone_number}")
        await client.send_code_request(phone_number)
        
        # Masukkan kode yang dikirim melalui SMS atau Telegram
        code = input('Masukkan kode verifikasi: ')
        try:
            # Jika tidak ada password dua faktor, login langsung
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            # Jika ada password dua faktor, minta password tambahan
            password = input('Masukkan password akun Telegram Anda: ')
            await client.sign_in(password=password)

    # Verifikasi login dengan mencetak informasi pengguna
    me = await client.get_me()
    print(f"Login berhasil sebagai {me.first_name} (ID: {me.id})")

    # Pastikan koneksi terputus dengan baik setelah selesai
    await client.disconnect()

async def login_with_tdata():
    # Meminta path tdata dari pengguna secara manual
    tdata_folder = input(r"Masukkan path folder tdata Anda (misal: C:\Users\<username>\AppData\Roaming\Telegram Desktop\tdata): ")

    # Load TDesktop client dari folder tdata
    tdesk = TDesktop(tdata_folder)

    # Periksa apakah akun telah dimuat
    if not tdesk.isLoaded():
        print("Tidak dapat memuat akun dari tdata. Pastikan path yang Anda masukkan benar.")
        return

    # Convert TDesktop ke Telethon menggunakan session yang ada
    client = await tdesk.ToTelethon(session=os.path.join(session_folder, "telethon_tdata.session"), flag=UseCurrentSession)

    # Hubungkan ke Telegram dan cetak semua sesi yang terhubung
    await client.connect()
    me = await client.get_me()
    print(f"Login berhasil sebagai {me.first_name} (ID: {me.id})")

    # Pastikan koneksi terputus dengan baik setelah selesai
    await client.disconnect()

async def main():
    # Tampilkan pesan selamat datang dengan ASCII art
    print_welcome_message()

    # Tampilkan menu pilihan
    print("Pilih metode login:")
    print("1. Login menggunakan tdata")
    print("2. Login menggunakan nomor telepon")
    
    choice = input("Masukkan pilihan Anda (1 atau 2): ")

    if choice == "1":
        await login_with_tdata()
    elif choice == "2":
        await login_with_phone()
    else:
        print("Pilihan tidak valid. Harap pilih antara 1 atau 2.")

# Menjalankan main loop
asyncio.run(main())
