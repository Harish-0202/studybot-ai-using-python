import os
import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# Patch PyAudioWPatch into pyaudio for Python 3.14 compatibility
import pyaudiowpatch as pyaudio
sys.modules['pyaudio'] = pyaudio

import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ---------- GEMINI API SETUP ----------
# Fetch API key from environment variable, or paste your newly regenerated key below:
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please set your Gemini API key before running StudyBot AI."
    )

client = genai.Client(api_key=api_key)

# ---------- AUDIO SETUP ----------

def speak_worker(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def speak(text):
    threading.Thread(target=speak_worker, args=(text,), daemon=True).start()

def listen_worker():
    mic_btn.config(text="Listening...", bg="#ef4444")
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source, phrase_time_limit=6)

        spoken_text = r.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, spoken_text)
        send_message()
    except sr.UnknownValueError:
        bot("Sorry, I could not understand what you said.")
    except sr.RequestError:
        bot("Speech recognition service is currently unavailable.")
    except Exception as e:
        bot(f"Microphone error: {e}")
    finally:
        mic_btn.config(text="🎤 Mic", bg="#4f46e5")

def start_listening():
    threading.Thread(target=listen_worker, daemon=True).start()

# ---------- APP WINDOW ----------

root = tk.Tk()
root.title("StudyBot AI")
root.geometry("500x750")
root.minsize(420, 620)
root.configure(bg="#f4f6fb")

def add_message(message, kind):
    chat.config(state="normal")
    if kind == "bot":
        chat.insert(tk.END, "🤖 StudyBot\n", "bot_name")
        chat.insert(tk.END, message + "\n\n", "bot_text")
    else:
        chat.insert(tk.END, "You\n", "user_name")
        chat.insert(tk.END, message + "\n\n", "user_text")
    chat.config(state="disabled")
    chat.see(tk.END)

def bot(text):
    add_message(text, "bot")
    speak(text)

def user(text):
    add_message(text, "user")

def clear_menu():
    for w in menu.winfo_children():
        w.destroy()

def button(text, command):
    tk.Button(
        menu, text=text, command=command, font=("Segoe UI", 9),
        bg="white", fg="#3730a3", activebackground="#e0e7ff",
        relief="solid", bd=1, cursor="hand2", padx=8, pady=5
    ).pack(fill="x", pady=2)

# ---------- MAIN MENU ----------

def main_menu():
    clear_menu()
    bot("What would you like help with? Click a button, ask anything, or use the mic.")
    button("📚 Study Tips", study_menu)
    button("📝 Exam Preparation", exam_menu)
    button("💻 Programming", programming_menu)
    button("🌐 Web Development", web_menu)
    button("🎯 Career & Skills", career_menu)
    button("🚀 Project Ideas", project_menu)

# ---------- STUDY ----------

def study_menu():
    user("Study Tips")
    clear_menu()
    bot("Choose a study topic.")
    button("⏰ How to study effectively", lambda: answer(
        "How to study effectively",
        "Study for 30 to 45 minutes, take a short break, practice what you learned, and revise regularly."
    ))
    button("🧠 How to remember topics", lambda: answer(
        "How to remember topics",
        "Understand the concept first, make short notes, explain it in your own words, practice questions, and revise after a gap."
    ))
    button("📅 Study schedule", lambda: answer(
        "Study schedule",
        "Example: 1 hour college subject, 1 hour programming, 30 minutes revision, and 30 minutes project practice."
    ))
    button("🔄 Revision tips", lambda: answer(
        "Revision tips",
        "Use short notes, practice without looking at answers, solve previous questions, and revise difficult topics regularly."
    ))
    button("⬅ Main Menu", main_menu)

# ---------- EXAMS ----------

def exam_menu():
    user("Exam Preparation")
    clear_menu()
    bot("Choose an exam topic.")
    button("📖 How to start", lambda: answer(
        "How to start exam preparation",
        "Check the syllabus, divide topics into easy and difficult, study important topics first, practice questions, then revise."
    ))
    button("📋 Important topics", lambda: answer(
        "Important topics",
        "Check previous papers, identify repeated concepts, ask your teacher about important units, and practice those topics."
    ))
    button("⏱ Last-minute preparation", lambda: answer(
        "Last-minute preparation",
        "Revise short notes, important questions, formulas and definitions. Avoid starting many new topics and get enough sleep."
    ))
    button("⬅ Main Menu", main_menu)

# ---------- PROGRAMMING ----------

def programming_menu():
    user("Programming")
    clear_menu()
    bot("Choose a programming area.")
    button("🐍 Python", python_menu)
    button("🧩 DSA", dsa_menu)
    button("☕ Java", lambda: answer(
        "Java",
        "Important Java topics include classes, objects, inheritance, polymorphism, exceptions and collections."
    ))
    button("💻 C Programming", lambda: answer(
        "C Programming",
        "Important C topics include variables, conditions, loops, arrays, functions, pointers and structures."
    ))
    button("⬅ Main Menu", main_menu)

def python_menu():
    user("Python")
    clear_menu()
    bot("Choose a Python topic.")
    button("📦 Variables & Data Types", lambda: answer(
        "Variables & Data Types",
        "Variables store values. Common Python types are int, float, string, boolean, list and dictionary."
    ))
    button("🔁 Loops", lambda: answer(
        "Loops",
        "Loops repeat code. Python mainly uses for loops and while loops."
    ))
    button("🔧 Functions", lambda: answer(
        "Functions",
        "A function is reusable code defined with def."
    ))
    button("📋 Lists", lambda: answer(
        "Lists",
        "A list stores multiple values, such as numbers = [10, 20, 30]."
    ))
    button("📖 Dictionaries", lambda: answer(
        "Dictionaries",
        "A dictionary stores key-value pairs."
    ))
    button("⬅ Programming", programming_menu)

def dsa_menu():
    user("DSA")
    clear_menu()
    bot("Choose a DSA topic.")
    button("🔎 Searching", lambda: answer(
        "Searching",
        "Searching means finding an element. Common methods are Linear Search and Binary Search."
    ))
    button("🔃 Sorting", lambda: answer(
        "Sorting",
        "Sorting arranges elements. Examples include Bubble Sort, Selection Sort and Insertion Sort."
    ))
    button("📚 Stack & Queue", lambda: answer(
        "Stack & Queue",
        "Stack follows LIFO: Last In, First Out. Queue follows FIFO: First In, First Out."
    ))
    button("🌳 Trees & Graphs", lambda: answer(
        "Trees & Graphs",
        "A tree is hierarchical. A graph contains vertices and edges."
    ))
    button("⬅ Programming", programming_menu)

# ---------- WEB ----------

def web_menu():
    user("Web Development")
    clear_menu()
    bot("Choose a web topic.")
    button("🏗 HTML", lambda: answer(
        "HTML",
        "HTML creates webpage structure using headings, paragraphs, images, and links."
    ))
    button("🎨 CSS", lambda: answer(
        "CSS",
        "CSS controls webpage appearance such as colors, fonts, spacing, layouts and animations."
    ))
    button("⚡ JavaScript", lambda: answer(
        "JavaScript",
        "JavaScript adds interaction and dynamic behavior to webpages."
    ))
    button("🖥 Backend", lambda: answer(
        "Backend",
        "Backend handles server-side logic. Common choices include Flask, Django and Node.js."
    ))
    button("⬅ Main Menu", main_menu)

# ---------- CAREER ----------

def career_menu():
    user("Career & Skills")
    clear_menu()
    bot("Choose a career topic.")
    button("💻 Skills for CSE", lambda: answer(
        "Skills for CSE",
        "Useful skills include programming, DSA, web development, databases, Git, problem solving and communication."
    ))
    button("📄 Resume", lambda: answer(
        "Resume",
        "A student resume can include education, technical skills, projects, certifications, and achievements."
    ))
    button("🐙 Git & GitHub", lambda: answer(
        "Git & GitHub",
        "Git is used for version control. GitHub is used to store and share code."
    ))
    button("🎓 Courses", lambda: answer(
        "Courses",
        "For software development, useful areas include Python, DSA, web development, SQL and Git."
    ))
    button("⬅ Main Menu", main_menu)

# ---------- PROJECTS ----------

def project_menu():
    user("Project Ideas")
    clear_menu()
    bot("Choose a project level.")
    button("🟢 Beginner Projects", lambda: answer(
        "Beginner Projects",
        "Calculator, quiz application, number guessing game, to-do list and simple chatbot."
    ))
    button("🟡 Intermediate Projects", lambda: answer(
        "Intermediate Projects",
        "Student management system, expense tracker, library management system and weather application."
    ))
    button("🔵 Python Projects", lambda: answer(
        "Python Projects",
        "StudyBot, quiz application, password manager and student management system."
    ))
    button("⬅ Main Menu", main_menu)

# ---------- AI & DISPATCH ----------

def answer(question, response):
    user(question)
    bot(response)

def generate_with_retry(prompt, model_name="gemini-2.5-flash", max_retries=3):
    """Executes content generation with exponential backoff for transient 503 errors."""
    delay = 1.5
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are StudyBot, a concise, friendly academic and tech career assistant for students. "
                        "Keep answers practical, direct, plain text (no markdown formatting like asterisks or bullet points), "
                        "and under 3 to 4 sentences so it sounds natural when read out loud by text-to-speech."
                    )
                )
            )
        except APIError as e:
            if (getattr(e, 'code', None) == 503 or "503" in str(e)) and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e

def ask_ai_worker(prompt):
    try:
        bot("Thinking... 🤖")
        
        # Primary call targeting gemini-2.5-flash
        try:
            response = generate_with_retry(prompt, model_name="gemini-2.5-flash")
        except APIError as e:
            # Fallback to gemini-1.5-flash if 2.5 is unavailable
            if getattr(e, 'code', None) == 503 or "503" in str(e):
                response = generate_with_retry(prompt, model_name="gemini-1.5-flash")
            else:
                raise e

        if response and response.text:
            bot(response.text.strip())
        else:
            bot("I couldn't generate an answer for that. Please try rephrasing.")
            
    except APIError as e:
        bot("The AI service is experiencing heavy traffic right now. Please try again shortly.")
    except Exception as e:
        bot(f"Error querying Gemini: {e}")

def handle_query(raw_text):
    q = raw_text.lower().strip()
    if q in ("hi", "hello", "hey"):
        bot("Hello! 👋 How can I help you study today?")
    elif q in ("bye", "exit", "quit"):
        bot("Goodbye! Keep learning! 👋")
        entry.config(state="disabled")
        send_btn.config(state="disabled")
        mic_btn.config(state="disabled")
    elif q == "python":
        python_menu()
    elif q == "dsa":
        dsa_menu()
    elif q == "exam":
        exam_menu()
    elif q == "study":
        study_menu()
    elif q == "web":
        web_menu()
    elif q == "career":
        career_menu()
    elif q == "project":
        project_menu()
    elif q in ("menu", "home"):
        main_menu()
    else:
        threading.Thread(target=ask_ai_worker, args=(raw_text,), daemon=True).start()

def send_message():
    text = entry.get().strip()
    if not text:
        return
    user(text)
    entry.delete(0, tk.END)
    handle_query(text)

# ---------- UI LAYOUT ----------

header = tk.Frame(root, bg="#4f46e5", height=70)
header.pack(side="top", fill="x")
header.pack_propagate(False)

tk.Label(
    header, text="🤖 StudyBot AI", font=("Segoe UI", 16, "bold"),
    fg="white", bg="#4f46e5"
).pack(anchor="w", padx=20, pady=(10, 0))

tk.Label(
    header, text="Voice & General AI Enabled Assistant",
    font=("Segoe UI", 9), fg="#e0e7ff", bg="#4f46e5"
).pack(anchor="w", padx=22)

input_frame = tk.Frame(root, bg="#e2e8f0", padx=10, pady=10)
input_frame.pack(side="bottom", fill="x")

entry = tk.Entry(input_frame, font=("Segoe UI", 11), relief="solid", bd=1)
entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
entry.bind("<Return>", lambda event: send_message())

mic_btn = tk.Button(
    input_frame, text="🎤 Mic", command=start_listening,
    font=("Segoe UI", 9, "bold"), bg="#4f46e5", fg="white",
    activebackground="#3730a3", activeforeground="white",
    relief="flat", padx=10, pady=6, cursor="hand2"
)
mic_btn.pack(side="left", padx=(0, 6))

send_btn = tk.Button(
    input_frame, text="Send", command=send_message,
    font=("Segoe UI", 9, "bold"), bg="#10b981", fg="white",
    activebackground="#059669", activeforeground="white",
    relief="flat", padx=14, pady=6, cursor="hand2"
)
send_btn.pack(side="right")

menu = tk.Frame(root, bg="#f4f6fb")
menu.pack(side="bottom", fill="x", padx=12, pady=(0, 8))

chat = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Segoe UI", 10),
    bg="white", bd=0, padx=12, pady=12, state="disabled"
)
chat.pack(side="top", fill="both", expand=True, padx=12, pady=10)

chat.tag_config("bot_name", font=("Segoe UI", 9, "bold"), foreground="#4f46e5")
chat.tag_config("bot_text", font=("Segoe UI", 10), foreground="#1f2937")
chat.tag_config("user_name", font=("Segoe UI", 9, "bold"), foreground="#059669")
chat.tag_config("user_text", font=("Segoe UI", 10), foreground="#1f2937")

bot("Hi! Welcome to StudyBot AI. You can click topics, speak, or ask any open question.")
main_menu()

root.mainloop()
