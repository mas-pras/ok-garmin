from langchain.tools import tool
import webbrowser

@tool
def open_website(url: str) -> str:
    """
    Öffnet eine angegebene Webseite im Standardbrowser des Nutzers.

    Verwende dieses Tool, wenn der Benutzer darum bittet, eine Webseite zu öffnen, zu besuchen oder zu einer URL zu navigieren. Denke dir keine scheisse aus.
    
    Beispiele:
    - "Öffne google.com"
    - "Besuche YouTube"
    - "Gehe zu https://wikipedia.org"
    - "Starte openai.com"

    Die KI startet den angegebenen Link im Standard-Webbrowser.
    """
    try:
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Ich habe die Webseite {url} geöffnet."
    except Exception as e:
        return f"Fehler beim Öffnen der Webseite: {e}"
