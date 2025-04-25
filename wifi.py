import subprocess
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()


def show_banner():
    banner_text = Text("""
   _____      ______________
  / __/ | /| / /  _/ __/  _/
 / _/  | |/ |/ // // _/_/ /
/_/    |__/|__/___/_/ /___/
""", style="bold green")

    subtitle = Text("📶 FWİFİ: Wi-Fi Analyzer", style="bold cyan")
    panel = Panel.fit(subtitle, border_style="cyan", title="🐍 by MrRobotroot", subtitle="🛰️ Wifi")

    console.print(banner_text)
    console.print(panel)



def get_wifi_info():
    try:
        result = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Wi-Fi tarama başarısız.")
        wifi_data = json.loads(result.stdout)
        return wifi_data
    except Exception as e:
        console.print(f"[bold red]Hata:[/bold red] {e}")
        return []

def display_wifi_networks(networks):
    table = Table(title="📡 Yakındaki Wi-Fi Ağları")

    table.add_column("SSID", style="cyan", no_wrap=True)
    table.add_column("BSSID (MAC)", style="magenta")
    table.add_column("Sinyal Gücü (dBm)", justify="center", style="green")
    table.add_column("Frekans (MHz)", justify="center", style="yellow")
    table.add_column("Güvenlik", style="red")

    for net in networks:
        ssid = net.get("ssid", "Bilinmiyor")
        bssid = net.get("bssid", "Yok")
        level = str(net.get("level", ""))
        freq = str(net.get("frequency", ""))
        cap = net.get("capabilities", "Bilinmiyor")

        table.add_row(ssid, bssid, level, freq, cap)

    console.print(table)


if __name__ == "__main__":
    show_banner()
    console.print("[bold blue]🔍 Wi-Fi ağları taranıyor...[/bold blue]")
    wifi_networks = get_wifi_info()
    if wifi_networks:
        display_wifi_networks(wifi_networks)
    else:
        console.print("[bold red]Hiçbir Wi-Fi ağı bulunamadı veya konum izni verilmedi.[/bold red]")
