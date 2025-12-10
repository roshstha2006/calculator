import tkinter as tk
from tkinter import filedialog, messagebox, font
import time

# =================== WINDOW ===================
root = tk.Tk()
root.title("Rosen Notepad Pro")
root.geometry("900x550")

file_path = None
dark_mode_enabled = False

# =================== FONT SETTINGS ===================
font_family = tk.StringVar(value="Consolas")
font_size = tk.IntVar(value=14)
current_font = (font_family.get(), font_size.get())

# =================== LINE NUMBERS ===================
def update_line_numbers(event=None):
    text = text_area.get("1.0", "end-1c")
    lines = text.count("\n") + 1
    line_nums = "\n".join(str(i) for i in range(1, lines + 1))
    line_bar.config(state="normal")
    line_bar.delete("1.0", tk.END)
    line_bar.insert(tk.END, line_nums)
    line_bar.config(state="disabled")

# ================ TEXT AREA + LINE BAR =================
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

line_bar = tk.Text(frame, width=4, padx=5, takefocus=0, border=0,
                   background="#e8e8e8", state="disabled")
line_bar.pack(side="left", fill="y")

text_area = tk.Text(frame, font=current_font, undo=True, wrap="word")
text_area.pack(fill="both", expand=True, side="left")

text_area.bind("<KeyRelease>", lambda e: (update_line_numbers(), update_word_count()))

# ================= WORD COUNT BAR =================
status = tk.Label(root, anchor="e")
status.pack(fill="x")

def update_word_count(event=None):
    words = len(text_area.get("1.0","end-1c").split())
    status.config(text=f"Words: {words}")

# ================= FILE HANDLING =================
def new_file():
    global file_path
    file_path = None
    text_area.delete(1.0, tk.END)

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path,"r",encoding="utf-8") as file:
            text_area.delete(1.0,tk.END)
            text_area.insert(tk.END,file.read())

def save_file():
    global file_path
    if file_path:
        with open(file_path,"w",encoding="utf-8") as file:
            file.write(text_area.get(1.0,tk.END))
    else:
        save_as()

def save_as():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                            filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path,"w",encoding="utf-8") as file:
            file.write(text_area.get(1.0,tk.END))

# =================== DARK MODE ===================
def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled

    if dark_mode_enabled:
        text_area.config(bg="#1e1e1e", fg="white", insertbackground="white")
        line_bar.config(bg="#2a2a2a", fg="white")
        root.config(bg="#1e1e1e")
        status.config(bg="#1e1e1e", fg="white")
    else:
        text_area.config(bg="white", fg="black", insertbackground="black")
        line_bar.config(bg="#e8e8e8", fg="black")
        root.config(bg="SystemButtonFace")
        status.config(bg="SystemButtonFace", fg="black")

# =================== FONT TOOLS ===================
def update_font(*args):
    text_area.config(font=(font_family.get(), font_size.get()))

font_family.trace("w", update_font)
font_size.trace("w", update_font)

# ================= UNDO / REDO =================
def undo(): text_area.edit_undo()
def redo(): text_area.edit_redo()

# ================= AUTO SAVE =================
def auto_save():
    if file_path:
        with open(file_path,"w",encoding="utf-8") as file:
            file.write(text_area.get(1.0,tk.END))
    root.after(15000, auto_save)  # auto save every 15 sec

auto_save()

# ================= MENU BAR =================
menu = tk.Menu(root); root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Dark Mode", command=toggle_dark_mode)

format_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Font", menu=format_menu)

format_menu.add_cascade(label="Font Family", menu=tk.Menu(format_menu))
format_menu.add_cascade(label="Font Size", menu=tk.Menu(format_menu))

# Dropdown GUI
toolbar = tk.Frame(root); toolbar.pack(fill="x")
tk.Label(toolbar,text="Font:").pack(side="left")
tk.OptionMenu(toolbar,font_family,*font.families()).pack(side="left")
tk.Label(toolbar,text="Size:").pack(side="left")
tk.Spinbox(toolbar,from_=8,to=40,textvariable=font_size,width=4).pack(side="left")

root.mainloop()
