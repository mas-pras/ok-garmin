@echo off

echo === Schritt 1: Virtuelle Umgebung erstellen ===
python -m venv venv

echo === Schritt 2: Main-Skript starten ===
venv\Scripts\python.exe main_offline.py

pause
