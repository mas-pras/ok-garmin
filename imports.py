import os
import logging
import time

import pyttsx3
from gtts import gTTS
import tempfile
from playsound import playsound
import pygame

from dotenv import load_dotenv

import speech_recognition as sr
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from tools.time import get_time 
from tools.ipconfig import run_ipconfig
from tools.wifi_scan import scan_wifi, connected_devices
from tools.shopping_cart import add_to_cart, remove_from_cart, read_cart
from tools.shutdown import shutdown_computer
from tools.website import open_website
from tools.open_app import open_app
from tools.internet_search import internet_search
from tools.video_speichern import speicher_video
from tools.diego import ask_Diego