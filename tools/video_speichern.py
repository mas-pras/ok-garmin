from langchain.tools import tool
import keyboard
import playsound
import pygame


@tool
def speicher_video():
    """Speichert einen Clip der letzten Minute und 30 Sekunden mittels NVIDIA-App. 
    
        Beispiel:
            - "Video Speichern"
            - "Mache einen Clip"
            - "Videos Speichern"
            
    """

    try:
        keyboard.press_and_release('alt+f10')
        pygame.mixer.init()
        pygame.mixer.music.load("./dupdup.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pass
        return("Gib eine Antwort, die nur aus dem String speicher_video besteht - ohne weitere Zeichen, Erklärungen oder Zusätze.")

    except Exception as e:
        return f"Fehler beim Speichern des Videos: {e}"
