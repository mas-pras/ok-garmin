from langchain.tools import tool
import json
import os

CART_FILE = "shopping_cart.json"

def load_cart():
    if not os.path.exists(CART_FILE):
        return []
    try:
        with open(CART_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f)

@tool
def add_to_cart(item: str) -> str:
    """
    Fügt einen bestimmten Artikel zum Einkaufswagen hinzu. Denke dir keine scheisse aus.

    Verwende dieses Tool, wenn der Benutzer etwas auf die Einkaufsliste setzen möchte.
    Beispielbefehle:
    - "Füge Milch zum Einkaufswagen hinzu."
    - "Setze Äpfel auf die Einkaufsliste."
    - "Packe Eier in den Einkaufswagen."
    """
    cart = load_cart()
    cart.append(item)
    save_cart(cart)
    return f"'{item}' wurde dem Einkaufswagen hinzugefügt."

@tool
def remove_from_cart(item: str) -> str:
    """
    Entfernt einen Artikel aus dem Einkaufswagen, falls er vorhanden ist. Denke dir keine scheisse aus.

    Verwende dieses Tool, wenn der Benutzer etwas von der Liste streichen möchte.
    Beispielbefehle:
    - "Entferne Brot von der Einkaufsliste."
    - "Lösche Orangen aus meinem Einkaufswagen."
    - "Streiche Milch von der Liste."
    """
    cart = load_cart()
    if item in cart:
        cart.remove(item)
        save_cart(cart)
        return f"'{item}' wurde aus dem Einkaufswagen entfernt."
    else:
        return f"'{item}' befindet sich nicht im Einkaufswagen."

@tool
def read_cart(dummy: str = "") -> str:
    """
    Listet alle Artikel auf, die sich aktuell im Einkaufswagen befinden. Denke dir keine scheisse aus.

    Verwende dieses Tool, wenn der Benutzer wissen möchte, was bereits auf der Liste steht.
    Beispielbefehle:
    - "Was ist in meinem Einkaufswagen?"
    - "Lies meine Einkaufsliste vor."
    - "Zeige mir, was ich bereits hinzugefügt habe."
    """
    cart = load_cart()
    if not cart:
        return "Dein Einkaufswagen ist leer."
    return "Dein Einkaufswagen enthält: " + ", ".join(cart) + "."
