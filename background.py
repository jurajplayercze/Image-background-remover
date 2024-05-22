from rembg import remove
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

photo = None

def remove_background():
    input_path = input_image_path.get()
    output_path = output_image_path.get()
    with open(input_path, "rb") as f:
        input_image = f.read()
    output_image = remove(input_image)
    with open(output_path, "wb") as f:
        f.write(output_image)

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        input_image_path.set(filepath)
        load_image(filepath)

def choose_output_path():
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filepath:
        output_image_path.set(filepath)

def load_image(filepath):
    global photo
    try:
        image = Image.open(filepath)
        w, h = root.winfo_width(), root.winfo_height()
        image.thumbnail((w - 20, h - 20))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
    except Exception as e:
        messagebox.showerror("Chyba", str(e))

def update_image():
    print("UPDATE")
    if input_image_path.get():
        load_image(input_image_path.get())

root = tk.Tk()
root.title("Program pro odstranění pozadí")
root.geometry("400x400")

button_open = tk.Button(root, text="Vybrat obrázek", command=open_file)
button_open.pack(pady=5)

input_image_path = tk.StringVar()
input_entry = tk.Entry(root, textvariable=input_image_path, state="readonly", width=30)
input_entry.pack(pady=5)

button_output = tk.Button(root, text="Vybrat výstupní cestu", command=choose_output_path)
button_output.pack(pady=5)

output_image_path = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_image_path, state="readonly", width=30)
output_entry.pack(pady=5)

convert_button = tk.Button(root, text="Odstranit pozadí", command=remove_background)
convert_button.pack(pady=10)

label = tk.Label(root)
label.pack(expand=True, fill="both")

resize_timer = None

def on_resize(event):
    global resize_timer
    if resize_timer is not None:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, update_image)

root.bind("<Configure>", on_resize)

root.mainloop()
