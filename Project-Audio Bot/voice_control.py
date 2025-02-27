import speech_recognition as sr
import pyautogui
import os
import webbrowser
import time
import threading

# Initialize Recognizer Once
recognizer = sr.Recognizer()

# Function to recognize voice command
def listen_command():
    with sr.Microphone() as source:
        print("🎤 Listening for commands...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)  # Faster noise reduction
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)  # Faster response
            command = recognizer.recognize_google(audio, language="en-GB").lower()
            print(f"🗣 Raw command detected: [{command}]")  # Debugging
            return command.strip()
        except sr.UnknownValueError:
            return None  # Skip errors for faster processing
        except sr.RequestError:
            print("⚠️ Speech recognition error.")
            return None
        except sr.WaitTimeoutError:
            return None

# Function to execute commands
def execute_command(command):
    if not command:
        return

    commands_map = {
        "minimise": lambda: pyautogui.hotkey("win", "down"),
        "minimize": lambda: pyautogui.hotkey("win", "down"),
        "maximize": lambda: pyautogui.hotkey("win", "up"),
        "full screen": lambda: pyautogui.hotkey("win", "up"),
        "close": lambda: pyautogui.hotkey("alt", "f4"),
        "open notepad": lambda: os.system("notepad"),
        "open chrome": lambda: os.system("start chrome"),
        "scroll up": lambda: pyautogui.scroll(300),
        "scroll down": lambda: pyautogui.scroll(-300),
        "volume up": lambda: pyautogui.press("volumeup"),
        "volume down": lambda: pyautogui.press("volumedown"),
        "mute": lambda: pyautogui.press("volumemute"),
        "take screenshot": lambda: pyautogui.screenshot(f"screenshot_{int(time.time())}.png"),
    }

    # Execute command if found
    for key, action in commands_map.items():
        if key in command:
            action()
            print(f"✅ Executed: {key}")
            return

    # Handle Google Search
    if "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        print(f"🔍 Searching Google for: {query}")

    else:
        print("❌ Command not recognized.")

# Main loop (Faster with threading)
def run_voice_control():
    while True:
        command = listen_command()
        if command:
            if "exit" in command or "stop" in command:
                print("👋 Exiting voice assistant.")
                break
            threading.Thread(target=execute_command, args=(command,)).start()  # Run in parallel

# Start voice control
run_voice_control()
