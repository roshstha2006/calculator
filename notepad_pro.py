import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# ====== Functions ======
def open_image():
    global img, tk_img
    path = filedialog.askopenfilename(filetypes=[("Image Files","*.png *.jpg *.jpeg *.bmp")])
    if not path:
        return
    img = Image.open(path)
    tk_img = ImageTk.PhotoImage(img.resize((400, 300)))
    image_label.config(image=tk_img)
    image_label.image = tk_img
    status_label.config(text=f"Loaded: {path.split('/')[-1]}")

def add_watermark():
    global img, tk_img
    if img is None:
        messagebox.showerror("Error", "Load an image first")
        return
    text = watermark_var.get()
    if not text:
        messagebox.showerror("Error", "Enter watermark text")
        return
    # Add watermark
    watermarked = img.copy()
    draw = ImageDraw.Draw(watermarked)
    font_size = 30
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    width, height = watermarked.size
    pos = position_var.get()
    # Determine position
    positions = {
        "Top-Left": (10,10),
        "Top-Right": (width-200,10),
        "Bottom-Left": (10,height-50),
        "Bottom-Right": (width-200,height-50),
        "Center": (width//2 - 100, height//2 - 20)
    }
    draw.text(positions[pos], text, font=font, fill=(255,255,255,128))
    tk_img = ImageTk.PhotoImage(watermarked.resize((400,300)))
    image_label.config(image=tk_img)
    image_label.image = tk_img
    global final_img
    final_img = watermarked
    status_label.config(text="Watermark added!")

def save_image():
    global final_img
    if final_img is None:
        messagebox.showerror("Error","No image to save")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Files","*.png"),("JPEG Files","*.jpg")])
    if path:
        final_img.save(path)
        status_label.config(text=f"Saved: {path.split('/')[-1]}")

# ====== GUI ======
root = tk.Tk()
root.title("Image Watermark Tool")
root.geometry("500x550")
root.resizable(False, False)

img = None
final_img = None
tk_img = None

# --- Controls ---
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame,text="Load Image",bg="#4CAF50",fg="white",command=open_image).grid(row=0,column=0,padx=5)
tk.Label(control_frame,text="Watermark:").grid(row=0,column=1,padx=5)
watermark_var = tk.StringVar()
tk.Entry(control_frame,textvariable=watermark_var).grid(row=0,column=2,padx=5)
tk.Label(control_frame,text="Position:").grid(row=0,column=3,padx=5)
position_var = tk.StringVar(value="Bottom-Right")
tk.OptionMenu(control_frame,position_var,"Top-Left","Top-Right","Bottom-Left","Bottom-Right","Center").grid(row=0,column=4,padx=5)
tk.Button(control_frame,text="Add Watermark",bg="#2196F3",fg="white",command=add_watermark).grid(row=0,column=5,padx=5)
tk.Button(control_frame,text="Save Image",bg="#f44336",fg="white",command=save_image).grid(row=0,column=6,padx=5)

# --- Image Display ---
image_label = tk.Label(root)
image_label.pack(pady=10)

# --- Status ---
status_label = tk.Label(root,text="No image loaded",font=("Arial",10))
status_label.pack(pady=5)

root.mainloop()
