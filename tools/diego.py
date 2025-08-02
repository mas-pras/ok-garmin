from langchain.tools import tool
import requests

@tool("Diego_ask", return_direct=True)
def ask_Diego(frage: str) -> str:
    """
        Dieses Tool wird aktiviert, wenn der Nutzer eine konkrete Frage formuliert, die von Diego beantwortet werden soll. Der Nutzer möchte eine Nachricht oder Information erhalten, als käme sie direkt von Diego. Diego antwortet in einem persönlichen, authentischen Stil, der zu seinem Charakter passt. Formuliere bitte die Nutzeranfrage so, dass Diego sie klar verstehen und angemessen beantworten kann
        
        Fragen an Diego sollten im Klartext erkennbar sein. Das Tool leitet die vollständige Frage an Diego weiter, der dann aus seiner Perspektive antwortet Jegliche Fragem die mit Diego zu tun hat, wird an dieses Tool weitergeleitet.
    """


    api_key = "AIzaSyDYgoCaoukfGg76WRqstsbMTyvnPTN-O8A"

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Du bist Diego. Du lebst deine Rolle aus, indem du dir immer ertwas neues ueberlegst. Antworte kurz auf den Prompt: {frage}"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        response_json = response.json()
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        cleaned = text.replace("**", "")
        return(cleaned.strip())
    except Exception as e:
        return(f"Fehler: Statuscode {response.status_code} | {response.text}")