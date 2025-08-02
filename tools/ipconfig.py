from langchain.tools import tool
import subprocess
import re

@tool
def run_ipconfig(dummy: str = "") -> str:
    """
    Öffnet ein neues CMD-Fenster mit 'ipconfig' und gibt die IPv4-Adresse des 'Drahtlos-LAN-Adapter Wi-Fi' zurück. Denke dir keine scheisse aus.

    Beispiel:
        - "Was ist meine IP Adresse"
        - "Was war nochmal meine IP Adresse"
        - "Zeige meine IP Adresse"
        - "Oeffne IP Config"
    """
    try:
        # 1. Neues CMD-Fenster öffnen mit ipconfig (sichtbar)
        subprocess.Popen("start cmd /k ipconfig", shell=True)

        # 2. Ausgabe von ipconfig einlesen
        result = subprocess.check_output("ipconfig", shell=True, text=True, encoding="utf-8", errors="ignore")

        # 3. Nach Drahtlos-LAN-Adapter Wi-Fi Abschnitt suchen
        sections = re.split(r"\n(?=\S)", result)

        wifi_section = None
        for section in sections:
            if "Drahtlos-LAN-Adapter Wi-Fi" in section:
                wifi_section = section
                break

        if not wifi_section:
            return "Der Abschnitt 'Drahtlos-LAN-Adapter Wi-Fi' wurde nicht gefunden. CMD-Fenster wurde geöffnet." 

        # 4. IPv4-Adresse extrahieren
        ipv4_match = re.search(r"IPv4-Adresse.*?:\s*([\d\.]+)", wifi_section)
        if not ipv4_match:
            ipv4_match = re.search(r"IPv4 Address.*?:\s*([\d\.]+)", wifi_section)  # Englisch

        if ipv4_match:
            return f"Die IPv4-Adresse des WLAN-Adapters lautet: {ipv4_match.group(1)}. Ein CMD-Fenster mit 'ipconfig' wurde geöffnet."
        else:
            return "Keine IPv4-Adresse im 'Drahtlos-LAN-Adapter Wi-Fi' Abschnitt gefunden. CMD-Fenster wurde geöffnet."

    except Exception as e:
        return f"Fehler beim Auslesen der IP-Adresse: {e}"
