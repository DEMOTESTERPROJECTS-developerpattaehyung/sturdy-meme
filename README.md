
# 🖼️ Meme Maker (Python + Tkinter + Pillow)

A simple and fun **GUI Meme Generator** built using **Python**, **Tkinter**, and **Pillow**.  
Create classic-style memes with top and bottom text in just a few clicks!

---

## 🚀 Features
- 🖼️ Load images (JPG, PNG, BMP, GIF)
- ✍️ Add **Top** and **Bottom** text
- 🔤 Adjust **Font Size** and **Stroke Width**
- 👁️ Live **Preview**
- 💾 Save final meme as PNG
- ⚙️ Cross-platform (Windows / macOS / Linux)

---

## 🧠 Requirements
- Python 3.8 or higher  
- Pillow library  

Install Pillow:
```bash
pip install pillow
````

---

## 🖥️ How to Run

1. Clone or download this repository.
2. Open a terminal in the folder containing `meme_maker.py`.
3. Run the app:

   ```bash
   python meme_maker.py
   ```
4. Use the interface:

   * **Open Image** → choose your image
   * Type **Top Text** and **Bottom Text**
   * Adjust font size or stroke width
   * Click **Save Meme** to export your creation 🎉

---

## ⚡ Example Output

| Original                                                           | Meme Example                                                                    |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| ![input](https://via.placeholder.com/300x200.png?text=Input+Image) | ![meme](https://via.placeholder.com/300x200.png?text=TOP+TEXT%0A%0ABOTTOM+TEXT) |

---

## 🛠️ Optional: Create an Executable

Want to share your meme app easily?

Install **PyInstaller**:

```bash
pip install pyinstaller
```

Build a one-file app:

```bash
pyinstaller --onefile --windowed meme_maker.py
```

Your standalone executable will appear in the `dist/` folder.

---

## 🧩 Notes

* The app tries to use the **Impact** font (classic meme font).
  If unavailable, it falls back to **DejaVuSans-Bold** or the default PIL font.
* Works best with wide images and bold text.
* Customize fonts by editing the font path in the script.

---

## 🧑‍💻 Author

**Leo**
Fun open-source meme project built with ❤️ using Python.

---

## 📜 License

MIT License — free to use, modify, and share.

---

```

---


