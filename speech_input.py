import speech_recognition as sr

def get_audio():

    print(">>> get_audio function started")

    r = sr.Recognizer()

    try:
        with sr.Microphone(device_index=1) as source:
            print("🎤 Adjusting noise...")

            r.adjust_for_ambient_noise(source, duration=2)

            print("🎤 Listening... Speak NOW!")

            # ⬇ increased time
            audio = r.listen(source, timeout=10, phrase_time_limit=7)

        print("Processing...")

        text = r.recognize_google(audio)
        print("You said:", text)

        return text

    except sr.WaitTimeoutError:
        print("❌ You didn't speak in time")
        return "No speech detected"

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return "Could not understand"

    except Exception as e:
        print("ERROR:", e)
        return "Error occurred"