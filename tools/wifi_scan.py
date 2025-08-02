from langchain.tools import tool
import subprocess
import re

@tool
def scan_wifi(dummy: str = "") -> str:
    """
    Führt einen WLAN-Scan durch, öffnet ein CMD-Fenster mit den verfügbaren Netzwerken.
    Gibt eine formelle Bestätigung und den Namen des aktuell verbundenen WLANs zurück.
    Nur für Windows geeignet. Denke dir keine scheisse aus.

    Beispiel:
        - "Was sind Netzwerke in meiuner Umgebung"
        - "Zeige mir Netzwerke in meiner Umgebung"
        - "Starte einen WLAN Scan"
    """
    try:
        subprocess.Popen("start cmd /k netsh wlan show networks mode=bssid", shell=True)

        # Aktuell verbundenes WLAN abfragen
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True, encoding="utf-8", errors="ignore")
        match = re.search(r"^\s*SSID\s+:\s+(.+)$", result, re.MULTILINE)
        ssid = match.group(1).strip() if match else "nicht ermittelbar"

        return (
            "Der WLAN-Scan wurde erfolgreich gestartet. "
            "Ein neues CMD-Fenster zeigt die verfügbaren Netzwerke mit SSID, Signalstärke und Sicherheitsstandard an.\n"
            f"Aktuell verbundenes Netzwerk (SSID): {ssid}"
        )

    except Exception as e:
        return f"Beim Ausführen des WLAN-Scans ist ein Fehler aufgetreten: {e}"


@tool
def connected_devices(dummy: str = "") -> str:
    """
    Öffnet ein CMD-Fenster, in dem alle aktuell bekannten Netzwerkgeräte (laut ARP-Tabelle) aufgelistet werden.
    Gibt eine formelle Bestätigung zurück. Nur für Windows geeignet. Denke dir keine scheisse aus.
    """
    try:
        subprocess.Popen("start cmd /k arp -a", shell=True)
        return (
            "Die Liste der derzeit erkannten Netzwerkgeräte wurde erfolgreich geöffnet. "
            "Ein CMD-Fenster zeigt die Inhalte der lokalen ARP-Tabelle mit IP- und MAC-Adressen an."
        )
    except Exception as e:
        return f"Beim Öffnen des CMD-Fensters zur Anzeige der Netzwerkgeräte ist ein Fehler aufgetreten: {e}"
