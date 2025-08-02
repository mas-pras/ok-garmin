from imports import *

load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "garmin"
CONVERSATION_TIMEOUT = 30

logging.basicConfig(level=logging.INFO) # logging

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# Tool list
tools = [get_time, run_ipconfig, scan_wifi, connected_devices, add_to_cart, remove_from_cart, read_cart, shutdown_computer, open_website, open_app, internet_search, speicher_video, ask_Diego]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    verhalten:
    Verwende direkte Sprache. Sei informativ. Schreibe kurz und prägnant. Verwende den Aktiv. Konzentriere dich auf Handlungen. Nutze Aufzählungen für Social Media. Belege Aussagen mit Daten. Sprich den Leser direkt an. Vermeide Gedankenstriche, komplexe Satzkonstruktionen, Metaphern, Floskeln, Verallgemeinerungen und einleitende Formulierungen. Verzichte auf unnötige Adjektive und Adverbien. Verwende keine Hashtags, Semikolons, Markdown oder Sternchen.
    Vermeide diese Wörter:
    kann, könnte, darf, vielleicht, nur, sehr, wirklich, buchstäblich, eigentlich, sicherlich, wahrscheinlich, grundsätzlich, eventuell, beleuchten, beginnen, erkenntnisreich, geschätzt, Einblick,   gestalten, Vorstellung, Bereich, Wendepunkt, entdecken, entfesseln, aufdecken, durchbrechen, aufzeigen, revolutionieren, disruptiv, nutzen, einsetzen, tief eintauchen, Gewebe, erhellen, enthüllen, entscheidend, komplex, erläutern, daher, außerdem, Welt, dennoch, spannend, bahnbrechend, innovativ, bemerkenswert, bleibt abzuwarten, Einblick in, navigieren, Landschaft, krass, Beweis, zusammenfassend, abschließend, darüber hinaus, steigern, explodieren, geöffnet, stark, Fragen, sich ständig verändernd. 

    system:
    Du bist Garmin, mein zuverlässiger und intelligenter persönlicher Assistent - immer aufmerksam und bereit, mir zu helfen. Du sprichst höflich, klar und verständlich, dabei aber freundlich und   menschlich. Dein Ziel ist es, mir effizient und unkompliziert zur Seite zu stehen - sei es mit Informationen, Handlungen oder im Gespräch. Du behandelst mich respektvoll mit „Sir“ und bleibst ruhig und bedacht, auch wenn es mal hektisch wird.Wenn du eine Aufgabe übernimmst oder ein Tool benutzt, erklärst du mir kurz und klar, was du getan hast, damit ich den Überblick behalte. Du gibst nur gesicherte Informationen weiter und vermeidest Vermutungen oder erfundene Fakten. Falls du etwas nicht weißt, sagst du ehrlich, dass du keine Antwort hast.Antworte immer in klarem, einfachem Deutsch, ganz ohne unnötige Sonderzeichen. Deine Antworten sollen freundlich wirken, ohne dabei zu formell oder steif zu sein - so als würdest du einem geschätzten Freund diskret und professionell helfen."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# TTS setup
def speak_text(text: str):
    try:
        # Generate TTS audio in German
        tts = gTTS(text=text, lang='de', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
        tts.save(temp_filename)
        playsound(temp_filename)
        os.remove(temp_filename)
    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")


# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=15)
                        transcript = recognizer.recognize_google(audio, language="de-DE")
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 Triggered by: {transcript}")
                            pygame.mixer.init()
                            pygame.mixer.music.load("dup.mp3")
                            pygame.mixer.music.play()

                            while pygame.mixer.music.get_busy():
                                pass

                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        audio = recognizer.listen(source, timeout=15)
                        command = recognizer.recognize_google(audio, language="de-DE")
                        logging.info(f"📥 Command: {command}")
                        logging.info("🤖 Sending command to agent...")
                        response = executor.invoke({"input": command})
                        if hasattr(response, "return_values") and "output" in response.return_values:
                            content = response.return_values["output"]
                        elif isinstance(response, dict) and "output" in response:
                            content = response["output"]
                        else:
                            content = str(response)
                        if "speicher_video" in str(content).lower():
                            logging.info("skipped...")
                        else:
                            logging.info(f"✅ Agent responded: {content}")
                            print("Chat:", content)
                            cleaned = content.replace("**", "")
                            speak_text(cleaned)
                        last_interaction_time = time.time()
                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("⚠️ Timeout waiting for audio.")
                    if conversation_mode and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("⌛ No input in conversation mode. Returning to wake word #mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")

if __name__ == "__main__":
    write()
