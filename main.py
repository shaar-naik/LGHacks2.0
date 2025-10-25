import tkinter as tk
import sys
import textwrap
from tkinter import OptionMenu
from tkinter.constants import VERTICAL

introText = """
Are you interested in volunteering? Do you have a hard time looking for what volunteering places suit you? 
Use this app to help decide what volunteering places you're interested in!
"""
question1 = """
What are your interests?
If other, please write it out

Here are the list of volunteering opportunities:
"""
outputTextString1 = "Anime is a unique form of Japanese animation that blends art, storytelling, and emotion in powerful ways. It covers a wide range of genres, from action and romance to science fiction and slice of life. Unlike many Western cartoons, anime often explores deep themes about life, identity, and human connection. Its vibrant visuals and expressive characters attract fans worldwide. Beyond entertainment, anime inspires creativity, art, and culture, making it a global phenomenon that continues to grow in influence and popularity."

window = tk.Tk()
window.title("Volunteer App")
window.attributes('-fullscreen', True)
window.configure()

def closewindow():
    sys.exit(0)

def decide():
    chunks = textwrap.wrap(outputTextString1, 73)
    printOutputText = "\n"
    for chunk in chunks:
        printOutputText = printOutputText + chunk + "\n"
    outputText = tk.Canvas(window, width=1250, height=500)
    outputText.create_text(5, -20, text=printOutputText, anchor="nw", fill="black", font=("Arial", 18))
    outputText.place(relx=0.4, rely=0.25, anchor="nw")

label = tk.Label(window, text="Welcome to MyVolunteer!", font=("Arial", 40))
label.place(relx=0.5, rely=0.05, anchor='n')

backgroundText = tk.Canvas(window, width=1250, height=50)
backgroundText.create_text(625, 25, text=introText, anchor="center", fill="black", font=("Arial", 18))
backgroundText.place(relx=0.5, rely=0.15, anchor='n')

inputText = tk.Canvas(window, width=1250, height=500)
inputText.create_text(5, -20,  text=question1, anchor="nw",  fill="black", font=("Arial", 18))
inputText.place(relx=0.0, rely=0.25, anchor="nw")

clicked = tk.StringVar()
clicked.set("Tech")
interestList = tk.OptionMenu(window,clicked, "Tech", "Education", "Healthcare", "Environment", "Other")
interestList.place(relx=0.20, rely=0.255, anchor="nw")

otherInterest = tk.Entry(window, width=15)
otherInterest.place(relx=0.01, rely=0.33, anchor="nw")

# Example list of volunteers
volunteerList = ["Tech Interactive", "Aviation", "Cutting Trees", "t", "t", "t"]

# Create a frame to hold both the listbox and the scrollbar
listFrame = tk.Frame(window)
listFrame.place(relx=0.01, rely=0.4, anchor="nw")

# Create the scrollbar
scrollBox = tk.Scrollbar(listFrame)
scrollBox.pack(side=tk.RIGHT, fill=tk.Y)

# Create the listbox and attach the scrollbar
volunteerListBox = tk.Listbox(listFrame, height=15, width=75, yscrollcommand=scrollBox.set)
volunteerListBox.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure scrollbar to control listbox
scrollBox.config(command=volunteerListBox.yview)

# Insert the volunteer list
for volunteer in volunteerList:
    volunteerListBox.insert(tk.END, volunteer)

decideButton = tk.Button(text="Decide", command=decide, font=("Arial", 18), width=10, height=2)
decideButton.place(relx=0.01, rely=0.73, anchor="nw")

exitWindow = tk.Button(text="Exit Window", command=closewindow, font=("Arial", 18), width=10, height=2)
exitWindow.place(relx=0.13, rely=0.73, anchor="nw")

window.mainloop()

