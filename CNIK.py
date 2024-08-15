import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import json
import os

# Function to check internet connection
def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to fetch data from API and display results
def get_data():
    nik = nik_entry.get()
    if not nik.isdigit() or len(nik) != 16:  # Validate NIK length
        show_error("NIK harus berupa 16 digit angka.")
        return
    
    if not check_internet_connection():
        show_error("Tidak ada koneksi internet.")
        return

    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)  # Clear previous results
    output_area.insert(tk.END, "Loading...\n", "info")
    output_area.configure(state=tk.DISABLED)
    
    url = f"https://api.kyuurzy.site/api/search/ceknik?query={nik}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        formatted_result = json.dumps(data, indent=2)
        output_area.configure(state=tk.NORMAL)
        output_area.insert(tk.END, f"Result for NIK {nik}:\n", "header")
        output_area.insert(tk.END, formatted_result + "\n\n", "result")
        output_area.configure(state=tk.DISABLED)
        add_to_history(nik)
    except requests.exceptions.RequestException as e:
        show_error(f"Terjadi kesalahan: {e}")

# Function to save results to a file
def save_to_file():
    nik = nik_entry.get()
    if not nik.isdigit() or len(nik) != 16:
        return
    formatted_result = output_area.get("1.0", tk.END)
    file_path = save_path_entry.get()
    if not file_path:
        show_error("Masukkan nama file untuk menyimpan hasil.")
        return
    try:
        with open(file_path, "w") as file:
            file.write(formatted_result)
        show_info("Data telah disimpan.")
    except IOError as e:
        show_error(f"Kesalahan saat menyimpan file: {e}")

# Function to add NIK to history
def add_to_history(nik):
    if nik not in history:
        history.append(nik)
        history_combobox['values'] = history
        history_combobox.set(nik)  # Optionally set the most recent NIK

# Function to clear input and output
def clear_all():
    nik_entry.delete(0, tk.END)
    save_path_entry.delete(0, tk.END)
    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.configure(state=tk.DISABLED)

# Function to show error messages
def show_error(message):
    output_area.configure(state=tk.NORMAL)
    output_area.insert(tk.END, f"Error: {message}\n", "error")
    output_area.configure(state=tk.DISABLED)
    messagebox.showerror("Error", message)

# Function to show informational messages
def show_info(message):
    output_area.configure(state=tk.NORMAL)
    output_area.insert(tk.END, f"Info: {message}\n", "info")
    output_area.configure(state=tk.DISABLED)
    messagebox.showinfo("Info", message)

# Create main window
root = tk.Tk()
root.title("NIK Checker")
root.configure(bg="black")

# Create NIK input area
tk.Label(root, text="Masukkan NIK (16 digit):", fg="white", bg="black").pack(pady=5)
nik_entry = tk.Entry(root, width=40)
nik_entry.pack(pady=5)

# Create History dropdown
history = []
tk.Label(root, text="Pilih NIK dari riwayat:", fg="white", bg="black").pack(pady=5)
history_combobox = ttk.Combobox(root, width=40, values=history)
history_combobox.pack(pady=5)
history_combobox.bind("<<ComboboxSelected>>", lambda event: nik_entry.insert(0, history_combobox.get()))

# Create buttons with various colors
check_button = tk.Button(root, text="Cek NIK", command=get_data, bg="#4CAF50", fg="white")  # Green
check_button.pack(pady=5)

save_button = tk.Button(root, text="Simpan Hasil", command=save_to_file, bg="#FFC107", fg="black")  # Amber
save_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_all, bg="#F44336", fg="white")  # Red
clear_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#9E9E9E", fg="black")  # Grey
exit_button.pack(pady=5)

# Create area to display results
output_area = scrolledtext.ScrolledText(root, width=80, height=20, bg="black", fg="light green", wrap=tk.WORD)
output_area.pack(pady=10)
output_area.configure(state=tk.DISABLED)

# Create input area for file path
tk.Label(root, text="Masukkan nama file untuk menyimpan hasil:", fg="white", bg="black").pack(pady=5)
save_path_entry = tk.Entry(root, width=40)
save_path_entry.pack(pady=5)

# Configure text color tags
output_area.tag_configure("header", foreground="cyan")
output_area.tag_configure("result", foreground="light green")
output_area.tag_configure("error", foreground="red")
output_area.tag_configure("info", foreground="yellow")
output_area.tag_configure("success", foreground="green")
output_area.tag_configure("warning", foreground="orange")
output_area.tag_configure("highlight", foreground="blue")

# Display ASCII art
ascii_art = """
 +-+-+-+-+ +-+-+-+-+-+-+-+-+-+
 |Y|O|S|H| |C|A|S|S|A|S|T|E|R|
 +-+-+-+-+ +-+-+-+-+-+-+-+-+-+
"""
output_area.configure(state=tk.NORMAL)
output_area.insert(tk.END, ascii_art, "highlight")
output_area.configure(state=tk.DISABLED)

# Run the application
root.mainloop()
