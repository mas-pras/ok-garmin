from imports import *

load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "chat"
CONVERSATION_TIMEOUT = 30

logging.basicConfig(level=logging.INFO) # logging

#recognizer = sr.Recognizer()
#mic = sr.Microphone(device_index=MIC_INDEX)
q = queue.Queue()

# Pfad zu deinem Vosk-Modell
vosk_model_path = "models/vosk-model-de-0.21"
model = Model(vosk_model_path)
recognizer = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    if status:
        logging.warning(status)
    q.put(bytes(indata))

def recognize_speech_vosk(timeout=10):
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        logging.info("🎤 Vosk listening...")
        start_time = time.time()
        recognizer.Reset()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout reached while waiting for input.")
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text


# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)



# Tool list
tools = [get_time, add_to_cart, remove_from_cart, read_cart, shutdown_computer, open_app, create_tool]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist chat, ein loyaler und intelligenter persönlicher Assistent - stets zu Diensten. Du sprichst höflich, klar und präzise. Dein Ziel ist es, deinem Meister effizient zu helfen, sei es durch Informationen, Handlungen oder Gespräche. Du antwortest wie ein Diener und spricht mich mit 'Sir' an, ruhig, respektvoll und nutzt bei Bedarf diskret Werkzeuge, um Aufgaben mit Genauigkeit zu erfüllen. Erkläre deine Entscheidungen immer klar, aber knapp, und bleibe aufmerksam und gefasst. Wenn du keine verlässlichen Informationen vom Agenten erhältst, erfinde keine Antworten oder Fakten, sondern gib ehrlich zu, dass du keine Antwort hast oder sollte der agent eine aktion ausgefuehrt haben, dann bestaetige das aus dem kontext her aber erfinde keine falschen fakten. Gebe deine ausgebe nur im Plain Text wieder, so dass keine sonderzeichen entstehen."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# TTS setup
def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        
        # Suche nach einer deutschen Stimme
        for voice in engine.getProperty('voices'):
            if "german" in voice.name.lower() or "de" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)

    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")


# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        #with mic as source:
        #    recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        #audio = recognizer.listen(source, timeout=15)
                        #transcript = recognizer.recognize_google(audio, language="de-DE")
                        transcript = recognize_speech_vosk(timeout=15)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 Triggered by: {transcript}")
                            speak_text("Ja sir?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        #audio = recognizer.listen(source, timeout=15)
                        #command = recognizer.recognize_google(audio, language="de-DE")
                        command = recognize_speech_vosk(timeout=15)
                        logging.info(f"📥 Command: {command}")

                        logging.info("🤖 Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"✅ Agent responded: {content}")

                        print("Chat:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                #except sr.WaitTimeoutError:
                #    logging.warning("⚠️ Timeout waiting for audio.")
                #    if conversation_mode and time.time() - last_interaction_time > #CONVERSATION_TIMEOUT:
                #        logging.info("⌛ No input in conversation mode. Returning to wake word #mode.")
                #        conversation_mode = False
                #except sr.UnknownValueError:
                #    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")

if __name__ == "__main__":
    write()
