from langchain.tools import tool
import subprocess
import platform

@tool
def shutdown_computer(dummy: str = "") -> str:
    """
    Fährt den Computer vollständig und sicher herunter (nur Windows).

    Verwende dieses Tool, wenn der Benutzer ausdrücklich darum bittet, den PC oder Computer auszuschalten bzw. herunterzufahren.

    Dies bewirkt:
    - Alle laufenden Programme werden geschlossen.
    - Der Systemzustand wird bei Bedarf gespeichert.
    - Das System wird heruntergefahren.
    """
    try:
        if platform.system() != "Windows":
            return "Das Herunterfahren wird mit diesem Tool nur unter Windows unterstützt."

        # Starte Herunterfahren mit 10 Sekunden Verzögerung
        subprocess.run("shutdown /s /t 10", shell=True)
        return "Der Computer wird in 10 Sekunden heruntergefahren. Bitte speichere alle offenen Arbeiten."
    except Exception as e:
        return f"Herunterfahren konnte nicht eingeleitet werden: {e}"
