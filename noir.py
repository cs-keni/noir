import tkinter as tk
from tkinter import filedialog, messagebox

# Create the main window
root = tk.Tk()
root.title("Noir")

# Set the dark theme for the window frame
root.configure(bg="#1C1C1C")
root.option_add("*foreground", "white")
root.option_add("*background", "#1C1C1C")
root.option_add("*Font", "Consolas 11")

# Set the cursor color to white
root.tk_setPalette(foreground='white', background='#1C1C1C')

# Create a frame to contain the text area and scrollbar
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Create the text area
text_area = tk.Text(frame, undo=True)
text_area.config(selectbackground="#2e79bf")
text_area.config(wrap="none")  # Disable word wrapping
text_area.pack(side="left", fill="both", expand=True)

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(frame, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the file menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)

unsaved_changes = False  # Flag to track unsaved changes
text_was_empty = True  # Flag to track whether the text area was initially empty

def new_file():
    global unsaved_changes, text_was_empty
    if unsaved_changes and not text_was_empty:
        response = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Continue?")
        if not response:
            return
    text_area.delete("1.0", "end")
    unsaved_changes = False
    text_was_empty = True

def open_file():
    global unsaved_changes, text_was_empty
    if unsaved_changes and not text_was_empty:
        response = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Continue?")
        if not response:
            return
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", "end")
            text_area.insert("1.0", file.read())
    unsaved_changes = False
    text_was_empty = not text_area.get("1.0", "end-1c")

def save_file():
    global unsaved_changes
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", "end-1c"))
    unsaved_changes = False

def exit_app():
    global unsaved_changes
    if unsaved_changes:
        response = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Exit without saving?")
        if not response:
            return
    root.destroy()

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Create the edit menu
edit_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

def undo():
    text_area.edit_undo()

def redo():
    text_area.edit_redo()

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

# Zoom functionality with Pillow
current_font_size = 11  # Initial font size

def zoom(event):
    global current_font_size
    if event.state == 4:  # State 4 corresponds to the Ctrl key
        if event.delta > 0:
            current_font_size += 1  # Scrolling up
        elif event.delta < 0:
            current_font_size = max(1, current_font_size - 1)  # Scrolling down

    text_area.config(font=("Consolas", current_font_size))
    text_area.config(wrap=tk.WORD)

text_area.bind("<MouseWheel>", zoom)

# Function to track changes in the text area
def on_text_change(event):
    global unsaved_changes
    if not text_was_empty or text_area.get("1.0", "end-1c"):
        unsaved_changes = True

text_area.bind("<<Modified>>", on_text_change)

# Function to reset the unsaved_changes
def reset_unsaved_changes(event=None):
    global unsaved_changes
    text_area.edit_modified(False)  # Reset the text modification flag
    unsaved_changes = False

# Bind the reset_unsaved_changes function to the text area
text_area.bind("<FocusOut>", reset_unsaved_changes)

# Bind the exit_app function to the window's close event
root.protocol("WM_DELETE_WINDOW", exit_app)

# Run the application
root.mainloop()