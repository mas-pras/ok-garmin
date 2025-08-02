@echo off

echo === Schritt 1: Virtuelle Umgebung erstellen ===
python -m venv venv

echo === Schritt 2: Pip in der venv aktualisieren ===
venv\Scripts\python.exe -m pip install --upgrade pip

echo === Schritt 3: requirements.txt Instalieren ===
venv\Scripts\pip.exe install -r requirements.txt

echo === Schritt 4: Main-Skript starten ===
venv\Scripts\python.exe main_online.py

pause
