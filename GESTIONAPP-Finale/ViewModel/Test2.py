import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def mostrar_imagen(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        resp.raise_for_status()  

        img_data = resp.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((300, 300))
        tk_img = ImageTk.PhotoImage(img)

        lbl_imagen.config(image=tk_img)
        lbl_imagen.image = tk_img

    except Exception as e:
        print("Error cargando imagen:", e)

# ================== UI ==================
root = tk.Tk()
root.title("Prueba Imagen Tkinter + PIL")

lbl_texto = tk.Label(root, text="URL de la imagen:")
lbl_texto.pack(pady=5)

entrada = tk.Entry(root, width=50)
entrada.pack(pady=5)

btn = tk.Button(root, text="Mostrar", command=lambda: mostrar_imagen(entrada.get()))
btn.pack(pady=5)

lbl_imagen = tk.Label(root)
lbl_imagen.pack(pady=10)

# URL de prueba inicial
entrada.insert(0, "https://picsum.photos/id/237/300/300")

root.mainloop()
