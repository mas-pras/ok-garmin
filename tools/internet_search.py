from langchain.tools import tool
from duckduckgo_search import DDGS

@tool("internet_search", return_direct=True)
def internet_search(abfrage: str) -> str:
    """
    Führt eine Websuche mit DuckDuckGo durch und gibt das oberste Ergebnis zurück. Denke dir keine scheisse aus.
    Verwende dieses Tool, wenn der Nutzer eine Frage stellt, die aktuelle Informationen erfordert. Nehezu jede Information, die nicht bereit gestellt werden kann soll gegoogelt werden.
    Es soll ueberprueft werden, ob der nutzer eine frage hat, die gesucht oder gegoogelt werden muss.

    Beispiele für Anfragen:
    - "Wie ist das Wetter heute in Paris?"
    - "Suche nach den neuesten Techniknachrichten"
    - "Bitte suche nach aktuellen KI-Nachrichten"

    Eingabe:
    - Ein natürlicher Spracheingabetext (String).
    """
    with DDGS() as ddgs:
        ergebnis = ddgs.text(abfrage, region='de-De', safesearch='Moderate', max_results=10)
        ergebnis_liste = list(ergebnis)

        if not ergebnis_liste:
            return f"Entschuldigung, ich konnte keine Ergebnisse finden für: \"{abfrage}\"."

        top = ergebnis_liste[0]
        return (
            f"Hier ist das oberste Ergebnis für: \"{abfrage}\"\n\n"
            f"Titel: {top['title']}\n"
        )
