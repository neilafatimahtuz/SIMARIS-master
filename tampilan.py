import os
import pyfiglet
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

def tampilkan_simores():
    os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar terminal

    # Membuat header dengan pyfiglet
    judul = pyfiglet.figlet_format("+ SIMORES +")
    subjudul = "Sistem Informasi Manajemen Rumah Sakit"

    # Menampilkan header dengan warna dan dekorasi
    print(Fore.GREEN + Style.BRIGHT + "+" + "-" * 60 + "+")
    print(Fore.RED + Style.BRIGHT + judul)
    print(Fore.GREEN + Style.BRIGHT + "+" + "-" * 60 + "+")
    print(Fore.BLUE + subjudul.center(60))
    print(Fore.GREEN + Style.BRIGHT + "+" + "-" * 60 + "+")

# Panggil fungsi untuk menampilkan tampilan
tampilkan_simores()
