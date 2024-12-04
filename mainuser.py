import os
import pyfiglet
import csv
from colorama import Fore, Style, init
import ast
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
from rich.layout import Layout

console = Console()

# Inisialisasi colorama
init(autoreset=True)

# Dummy data
users = {"user123": "pw123"}  # Format: {username: password}
patients = {"321": {"name": "el", "age": 18, "history": []}}
doctor_schedule = [
    {"name": "Dr. Joy", "specialty": "Cardiologist", "available_times": ["07:00", "14:00"]},
    {"name": "Dr. Al", "specialty": "Dermatologist", "available_times": ["11:00", "17:00"]}
]
appointments = []
prescriptions = []
payments = []

# Fungsi utilitas
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_title(title):
    print(Fore.CYAN + pyfiglet.figlet_format(title))

def pause():
    input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

def load_csv_data():
    """Memuat data pasien dan jadwal dokter dari file CSV"""
    global patients, doctor_schedule

    # Memuat data pasien
    with open("pasien.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            patients[row["nik"]] = {
                "name": row["name"],
                "age": int(row["age"]),
                "history": ast.literal_eval(row["history"]),
            }

    # Memuat data jadwal dokter
    with open("dokter.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            doctor_schedule.append({
                "name": row["name"],
                "specialty": row["specialty"],
                "available_times": row["available_times"].split(","),
                "diagnosis": row["diagnosis"].split(","),
                "resep": row["resep"].split(","),
            })

# Halaman login
def login():
    clear_screen()
    show_title("Login")
    users = input("Masukkan Username: ")
    password = input("Masukkan Password: ")

    if users == "user" and password == "pass":
            console.print("[bold green]Login berhasil![/bold green]", justify="center")
            pause()
            return True
    else:
        console.print("[bold red]Username atau password salah.[/bold red]", justify="center")
        choice = Prompt.ask("[yellow]Coba lagi? (y/n)[/yellow]")
        if choice.lower() == "n":
            console.print("[bold cyan]Terima kasih, keluar dari program.[/bold cyan]", justify="center")
            return False

# Menu utama
def main_menu():
    while True:
        show_title("Menu Utama")
        table = Table(title="Pilih Menu", box=None, title_style="bold cyan", header_style="bold yellow")
        table.add_column("No", style="bold white")
        table.add_column("Menu", style="bold green")
        table.add_row("1", "Data Pasien")
        table.add_row("2", "Jadwal Dokter")
        table.add_row("3", "Hasil Diagnosa")
        table.add_row("4", "Resep Obat")
        table.add_row("5", "Pembayaran")
        table.add_row("6", "Keluar")

        console.print(Align.center(table))
        choice = Prompt.ask("[cyan]Pilih menu[/cyan]")

        if choice == "1":
            patient_data()
        elif choice == "2":
            doctor_schedule_menu()
        elif choice == "3":
            show_diagnosis()
        elif choice == "4":
            show_prescriptions()
        elif choice == "5":
            handle_payment()
        elif choice == "6":
            console.print("[bold cyan]Terima kasih telah menggunakan aplikasi.[/bold cyan]", justify="center")
            break
        else:
            console.print("[bold red]Pilihan tidak valid.[/bold red]", justify="center")
            pause()

def patient_data():
    """Tampilkan data pasien"""
    show_title("Data Pasien")
    nik = Prompt.ask("[cyan]Masukkan NIK[/cyan]")

    if nik in patients:
        patient = patients[nik]
        patient_panel = Panel.fit(
            f"[bold green]Nama:[/bold green] {patient['name']}\n"
            f"[bold green]Usia:[/bold green] {patient['age']}\n"
            f"[bold green]Riwayat:[/bold green] {', '.join(patient['history']) if patient['history'] else 'Belum ada riwayat'}",
            title="Informasi Pasien",
            border_style="green",
        )
        console.print(patient_panel)
    else:
        console.print("[bold red]Data pasien tidak ditemukan.[/bold red]", justify="center")

    pause()

def doctor_schedule_menu():
    """Tampilkan jadwal dokter dengan pilihan terpusat"""
    show_title("Jadwal Dokter")
    table = Table(title="Jadwal Dokter", box=None, title_style="bold cyan", header_style="bold yellow")
    table.add_column("No", justify="center", style="bold white")
    table.add_column("Nama Dokter", style="bold green")
    table.add_column("Spesialis", style="bold cyan")
    table.add_column("Jam Tersedia", style="bold magenta")

    for idx, doctor in enumerate(doctor_schedule, 1):
        table.add_row(str(idx), doctor["name"], doctor["specialty"], ", ".join(doctor["available_times"]))

    console.print(Align.center(table))

    choice = Prompt.ask("[cyan]Pilih dokter berdasarkan nomor[/cyan]", default="0")
    if choice.isdigit() and 0 < int(choice) <= len(doctor_schedule):
        doctor = doctor_schedule[int(choice) - 1]
        time_choice = Prompt.ask(f"[magenta]Pilih jam untuk {doctor['name']} ({', '.join(doctor['available_times'])})[/magenta]")
        if time_choice in doctor["available_times"]:
            appointments.append({"doctor": doctor["name"], "time": time_choice})
            console.print("[bold green]Antrean berhasil ditambahkan.[/bold green]", justify="center")
        else:
            console.print("[bold red]Jam tidak valid.[/bold red]", justify="center")
    pause()

def show_diagnosis():
    """Tampilkan diagnosa dokter"""
    show_title("Hasil Diagnosa")
    for idx, doctor in enumerate(doctor_schedule, 1):
        panel = Panel.fit(
            f"[bold cyan]Nama Dokter:[/bold cyan] {doctor['name']}\n"
            f"[bold cyan]Spesialis:[/bold cyan] {doctor['specialty']}\n"
            f"[bold cyan]Diagnosa:[/bold cyan] {', '.join(doctor['diagnosis'])}",
            title=f"Dokter {idx}",
            border_style="cyan",
        )
        console.print(panel)
    pause()

def show_prescriptions():
    """Tampilkan resep obat berdasarkan dokter"""
    show_title("Resep Obat")
    for idx, doctor in enumerate(doctor_schedule, 1):
        panel = Panel.fit(
            f"[bold cyan]Nama Dokter:[/bold cyan] {doctor['name']}\n"
            f"[bold cyan]Spesialis:[/bold cyan] {doctor['specialty']}\n"
            f"[bold cyan]Resep:[/bold cyan] {', '.join(doctor['resep'])}",
            title=f"Dokter {idx}",
            border_style="cyan",
        )
        console.print(panel)
    pause()

def handle_payment():
    """Tampilkan pembayaran dalam format struk"""
    show_title("Pembayaran")
    bpjs = Prompt.ask("[cyan]Apakah menggunakan BPJS? (y/n)[/cyan]").lower()
    if bpjs == "y":
        console.print("[bold green]Pembayaran ditanggung oleh BPJS.[/bold green]", justify="center")
    else:
        biaya_rawat = Prompt.ask("[yellow]Masukkan biaya rawat inap (0 jika tidak ada)[/yellow]", default="0")
        biaya_dokter = Prompt.ask("[yellow]Masukkan biaya konsultasi dokter[/yellow]")
        biaya_obat = Prompt.ask("[yellow]Masukkan biaya obat[/yellow]")
        total = int(biaya_rawat) + int(biaya_dokter) + int(biaya_obat)

        struk = (
            f"[bold yellow]--- STRUK PEMBAYARAN ---[/bold yellow]\n"
            f"[bold green]Biaya Rawat Inap  : Rp {biaya_rawat}[/bold green]\n"
            f"[bold green]Biaya Dokter      : Rp {biaya_dokter}[/bold green]\n"
            f"[bold green]Biaya Obat        : Rp {biaya_obat}[/bold green]\n"
            f"[bold white]Total            : Rp {total}[/bold white]"
        )
        console.print(Align.center(struk))
    pause()

# Program utama
if __name__ == "__main__":
    load_csv_data()
    if login():
        main_menu()
    else:
        console.print("[bold cyan]Program selesai. Sampai jumpa![/bold cyan]", justify="center")