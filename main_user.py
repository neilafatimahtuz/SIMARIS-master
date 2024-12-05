import os
import pyfiglet
from colorama import Fore, Style, init

# Inisialisasi Colorama
init(autoreset=True)

# Dummy data
users = {"user123": {"password": "pw123", "nik": "321", "name": "El"}}
patients = {
    "321": {
        "name": "El",
        "age": 18,
        "history": [{"diagnosis": "Flu", "date": "2024-12-01"}],
    }
}
doctor_schedule = [
    {"name": "Dr. Joy", "specialty": "Cardiologist", "available_times": ["07:00", "14:00"]},
    {"name": "Dr. Al", "specialty": "Dermatologist", "available_times": ["11:00", "17:00"]},
]
appointments = []  # Untuk menyimpan jadwal yang dipilih pasien

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_title(title):
    clear_screen()
    ascii_art = pyfiglet.figlet_format(title)
    print(Fore.CYAN + ascii_art)

def login():
    while True:
        show_title("LOGIN")
        print(Fore.YELLOW + "Silakan login ke sistem")
        username = input(Fore.CYAN + "Username: ")
        password = input(Fore.CYAN + "Password: ")

        if username in users and users[username]["password"] == password:
            print(Fore.GREEN + "Login berhasil!")
            input(Fore.YELLOW + "Tekan Enter untuk melanjutkan...")
            return users[username]
        else:
            print(Fore.RED + "Username atau password salah.")
            retry = input(Fore.YELLOW + "Coba lagi? (y/n): ").lower()
            if retry != 'y':
                return None

def main_menu(user):
    while True:
        show_title("MENU UTAMA")
        print(Fore.YELLOW + "1. Data Pasien")
        print(Fore.YELLOW + "2. Jadwal Dokter")
        print(Fore.YELLOW + "3. Antrean Pasien")
        print(Fore.YELLOW + "4. Hasil Diagnosa")
        print(Fore.YELLOW + "5. Riwayat Pemeriksaan")
        print(Fore.YELLOW + "6. Resep Obat")
        print(Fore.YELLOW + "7. Pembayaran")
        print(Fore.YELLOW + "8. Keluar")

        choice = input(Fore.CYAN + "Pilih menu: ")
        if choice == "1":
            show_patient_data(user)
        elif choice == "2":
            schedule_appointment(user)
        elif choice == "3":
            show_appointments(user)
        elif choice == "4":
            show_diagnosis(user)
        elif choice == "5":
            show_history(user)
        elif choice == "6":
            show_prescriptions(user)
        elif choice == "7":
            handle_payment(user)
        elif choice == "8":
            print(Fore.GREEN + "Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_patient_data(user):
    show_title("DATA PASIEN")
    patient = patients[user["nik"]]
    print(Fore.GREEN + f"NIK: {user['nik']}")
    print(Fore.GREEN + f"Nama: {patient['name']}")
    print(Fore.GREEN + f"Usia: {patient['age']}")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def schedule_appointment(user):
    show_title("JADWAL DOKTER")
    print(Fore.YELLOW + "Pilih jadwal dokter:")
    for idx, doctor in enumerate(doctor_schedule, start=1):
        print(Fore.CYAN + f"{idx}. {doctor['name']} ({doctor['specialty']}) - {', '.join(doctor['available_times'])}")
    
    choice = input(Fore.CYAN + "Pilih dokter berdasarkan nomor (tekan Enter untuk kembali): ")
    if choice.isdigit() and 1 <= int(choice) <= len(doctor_schedule):
        doctor = doctor_schedule[int(choice) - 1]
        time_choice = input(Fore.MAGENTA + f"Pilih jam untuk {doctor['name']} ({', '.join(doctor['available_times'])}): ")
        if time_choice in doctor["available_times"]:
            appointments.append({"nik": user["nik"], "doctor": doctor["name"], "time": time_choice})
            print(Fore.GREEN + "Jadwal berhasil disimpan.")
        else:
            print(Fore.RED + "Jam tidak valid.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_appointments(user):
    show_title("ANTREAN PASIEN")
    patient_appointments = [app for app in appointments if app["nik"] == user["nik"]]
    if patient_appointments:
        for app in patient_appointments:
            print(Fore.GREEN + f"Dokter: {app['doctor']}, Jam: {app['time']}")
    else:
        print(Fore.RED + "Belum ada antrean.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_diagnosis(user):
    show_title("HASIL DIAGNOSA")
    patient = patients[user["nik"]]
    if "history" in patient and patient["history"]:
        print(Fore.GREEN + f"Diagnosa terakhir: {patient['history'][-1]['diagnosis']}")
    else:
        print(Fore.RED + "Belum ada diagnosa.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_history(user):
    show_title("RIWAYAT PEMERIKSAAN")
    patient = patients[user["nik"]]
    if "history" in patient and patient["history"]:
        for idx, record in enumerate(patient["history"], start=1):
            print(Fore.GREEN + f"{idx}. {record['diagnosis']} - {record['date']}")
    else:
        print(Fore.RED + "Tidak ada riwayat pemeriksaan.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_prescriptions(user):
    show_title("RESEP OBAT")
    print(Fore.GREEN + "Resep obat disesuaikan dengan hasil diagnosa dokter.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def handle_payment(user):
    show_title("PEMBAYARAN")
    print(Fore.YELLOW + "Tidak ada pembayaran yang perlu dilakukan saat ini.")
    input(Fore.YELLOW + "Tekan Enter untuk kembali...")

if __name__ == "__main__":
    user = login()
    if user:
        main_menu(user)
    else:
        print(Fore.CYAN + "Program selesai. Sampai jumpa!")
