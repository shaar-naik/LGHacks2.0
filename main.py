import tkinter as tk
import sys
import csv
from data_loader import main as load_opportunities
from SummaryModel import generate_category_summaries
import textwrap
import webbrowser

# --- Run backend ---
print("🚀 Loading volunteer opportunities...")
load_opportunities()  # generates volunteer_opportunities.csv

print("🧠 Generating category summaries...")
category_summaries_df = generate_category_summaries(
    opportunities_csv="csv files/volunteer_opportunities.csv",
    output_csv="csv files/category_summaries.csv"
)

# --- Load CSVs ---
def load_csv(csv_file):
    rows = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

opportunities = load_csv("csv files/volunteer_opportunities.csv")
category_summaries = {row["category"]: row["summary"] for _, row in category_summaries_df.iterrows()}
categories = sorted({row["category"] for row in opportunities})

# --- Tkinter UI ---
window = tk.Tk()
window.title("Volunteer App")
window.attributes('-fullscreen', True)

clicked = tk.StringVar()
clicked.set(categories[0])

def closewindow():
    sys.exit(0)

# --- Functions ---
def open_url(event):
    """Open URL when the user double-clicks a listbox item"""
    selection = volunteerListBox.curselection()
    if not selection:
        return
    selected_text = volunteerListBox.get(selection[0])
    # Extract URL at the end (after last space)
    url = selected_text.split(" - ")[-1]
    if url.startswith("http"):
        webbrowser.open(url)

def decide():
    category = clicked.get()
    volunteerListBox.delete(0, tk.END)

    # Show category summary at top
    summary_text = category_summaries.get(category, "No summary available")
    summary_canvas.delete("all")
    chunks = textwrap.wrap(summary_text, 120)
    y = 5
    for chunk in chunks:
        summary_canvas.create_text(5, y, text=chunk, anchor="nw", fill="black", font=("Arial", 18))
        y += 25

    # Populate listbox with opportunities for this category (only title and URL)
    for row in opportunities:
        if row.get("category") == category:
            display_text = f"{row['title']} - {row['url']}"
            volunteerListBox.insert(tk.END, display_text)


# --- UI Elements ---
label = tk.Label(window, text="Welcome to MyVolunteer!", font=("Helvetica", 40))
label.place(relx=0.5, rely=0.05, anchor='n')

# Category dropdown
interestList = tk.OptionMenu(window, clicked, *categories)
interestList.place(relx=0.2, rely=0.15, anchor="nw")

# Summary canvas
summary_canvas = tk.Canvas(window, width=1250, height=150, bg="white")
summary_canvas.place(relx=0.01, rely=0.25, anchor="nw")

# Listbox for opportunities
listFrame = tk.Frame(window)
listFrame.place(relx=0.01, rely=0.45, anchor="nw")

scrollBox = tk.Scrollbar(listFrame)
scrollBox.pack(side=tk.RIGHT, fill=tk.Y)

volunteerListBox = tk.Listbox(listFrame, height=15, width=120, font=("Arial", 14), yscrollcommand=scrollBox.set)
volunteerListBox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollBox.config(command=volunteerListBox.yview)

# Bind double click to open URL
volunteerListBox.bind("<Double-1>", open_url)

# Buttons
decideButton = tk.Button(text="Decide", command=decide, bg="lightgray", font=("Arial", 18, "bold"), width=10, height=2)
decideButton.place(relx=0.01, rely=0.85, anchor="nw")

exitWindow = tk.Button(text="Exit Window", command=closewindow, bg="lightgray", font=("Arial", 18, "bold"), width=10, height=2)
exitWindow.place(relx=0.88, rely=0.88, anchor="nw")

# Initial display
decide()

window.mainloop()
