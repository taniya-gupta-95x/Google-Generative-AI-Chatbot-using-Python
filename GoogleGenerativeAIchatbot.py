import google.generativeai as genai
import tkinter
from tkinter import *
from tkinter import scrolledtext
import threading
import queue

#Initialising a queue to maintain the responses
response_queue = queue.Queue()

# Configure Google Generative AI
API_KEY = "AIzaSyArKqt_xE4mzE6KbUK4ewQ00wJf4q96i9E"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

def send_message_async(text):
    """Send message to Gemini API in a separate thread."""
    try:
        response = chat.send_message(text)
        response_lines = response.text.splitlines()[:5]  # Limit to 5 lines
        limited_response = "\n".join(response_lines)
        response_queue.put(("success", limited_response))
    except Exception as e:
        response_queue.put(("error", str(e)))

def OnClick(event=None):
    """Handle Send button click or Ctrl+Enter."""
    text = inputText.get("1.0", END).strip()
    inputText.delete("1.0", END)
    if not text:
        return "break"  # Ignore empty input
    # Disable UI elements
    send.configure(state=DISABLED)
    inputText.configure(state=DISABLED)
    displayText.configure(state=NORMAL)
    displayText.insert(END, "YOU: " + text + "\n", "user")
    displayText.insert(END, "BOT: Typing...\n", "bot")  
    displayText.see(END)
    displayText.configure(state=DISABLED)
    # Start API call in a separate thread
    threading.Thread(target=send_message_async, args=(text,), daemon=True).start()
    # Check queue for response
    root.after(100, check_queue)
    return "break"  # Prevent default Enter behavior

def check_queue():
    """Check queue for API response and update UI."""
    try:
        status, result = response_queue.get_nowait()
        displayText.configure(state=NORMAL)
        # Remove "Typing..." message
        displayText.delete("end-2l", "end-1l")
        if status == "success":
            displayText.insert(END, "BOT: " + result + "\n\n", "bot")
        else:
            displayText.insert(END, "BOT: Error: " + result + "\n\n", "bot")
        displayText.see(END)
        displayText.configure(state=DISABLED)
        # Re-enable UI elements
        send.configure(state=NORMAL)
        inputText.configure(state=NORMAL)
        inputText.focus_set()
    except queue.Empty:
        # No response yet, check again after 100ms
        root.after(100, check_queue)

#Funtion to reset the chat on hitting back button
def NewChat():
    displayText.configure(state=NORMAL)
    displayText.delete("1.0", END)
    inputText.delete("1.0", END)
    page1.tkraise()

#Setting the root window
root = tkinter.Tk()
root.geometry("1200x800")
root.title("Chat Bot") 
root.resizable(False, False)

#Adding multiple frames
page1 = Frame(root)
page2 = Frame(root)
page1.configure(bg="FloralWhite")
page2.configure(bg="FloralWhite") 

#Showing one page at a time
for page in (page1, page2):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

#Setting up first page
welcome_container = Frame(page1, bg="FloralWhite")
welcome_container.pack(expand=True)

#Packing label and button in single frame for better visuals
front = Label(welcome_container, text="Welcome User!", font="Gabriela 40 bold", bg="FloralWhite", fg="DarkRED")
front.pack(anchor="center", pady=10)

start = Button(welcome_container, text="Start Chat", command=lambda: page2.tkraise(), font="Gabriela 15 bold", bg="DarkRed", fg="white")
start.pack(anchor="center", pady=10, ipadx=20, ipady=5)

#Setting up second page
header = Frame(page2, bg="FloralWhite")
header.pack(expand=True)

#Packing label and button in single frame for better visuals
back = Button(header, text="←", command=NewChat, bg="DarkRed", font="Gabriela 17 bold", fg="white")
back.pack(side=LEFT,anchor="w", pady=5, expand=True)

name = Label(header, text="Your Chat Bot", font="Gabriela 35 bold", bg="FloralWhite", fg="DarkRed")
name.pack(side=RIGHT,anchor="center", pady=5, expand=True, ipadx=405)

#Setting two scrolled text area
displayText = scrolledtext.ScrolledText(page2, wrap=tkinter.WORD, height=15, state=tkinter.DISABLED, bg="Lavender", font="Gabriela")
displayText.pack(fill=tkinter.BOTH, expand=True, pady=10, padx=10)
displayText.tag_config("user", foreground='Indigo')
displayText.tag_config("bot", foreground='DarkRed')

input = Label(page2, text="Type here...", font="Gabriela 15 bold", bg="FloralWhite", fg="DarkRed")
input.pack(anchor="w", padx=10, expand=True)

inputText = scrolledtext.ScrolledText(page2, wrap=tkinter.WORD, height=2, bg="LightGoldenRodYellow", font="Gabriela")
inputText.pack(fill=tkinter.BOTH, expand=True, padx=10)
inputText.focus_set()

# Bind Ctrl+Enter to OnClick
inputText.bind("<Control-Return>", OnClick)

send = Button(page2, text="Send", command=OnClick, bg="DarkRed", font="Gabriela 12 bold", fg="white")
send.pack(anchor=CENTER, pady=20, ipadx=15, ipady=3, padx=20)

#Ensuring the first page opens always
page1.tkraise()

root.mainloop()

