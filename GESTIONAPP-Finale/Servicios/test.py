from ImageStorage import SUPABASE_URL, SUPABASE_KEY, ImageStorage
from tkinter.filedialog import askopenfilename
import tkinter as tk

storage = ImageStorage(SUPABASE_URL, SUPABASE_KEY)

def subir_imagen():
    path = askopenfilename()
    if path:
        url = storage.upload_image(path, folder="productos")
        print("URL pública:", url)

if __name__ == "__main__":
    a = subir_imagen()
    a