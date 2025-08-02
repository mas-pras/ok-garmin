import subprocess
from langchain.tools import tool

@tool
def open_app(app: str) -> str:
    """Öffnet eine Anwendung anhand eines vorgegebenen Pfads. Beispiel-Eingabe: 'discord' oder wenn der Nutzer mit seinen Freunden sprechen moechte. Denke dir keine scheisse aus."""
    apps = {
        "discord": r"C:\Users\Laurens\AppData\Local\Discord\Update.exe --processStart Discord.exe"
    }

    app = app.lower().strip()
    if app not in apps:
        return f"❌ Die Anwendung '{app}' ist nicht vordefiniert."

    try:
        subprocess.Popen(apps[app], shell=True)
        return f"✅ Die Anwendung '{app}' wurde geöffnet."
    except Exception as e:
        return f"❌ Fehler beim Öffnen von '{app}': {str(e)}"
