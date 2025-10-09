#!/usr/bin/env python3
\"\"\"Simple Meme Maker GUI (Tkinter + Pillow)

Features:
- Load an image (JPEG/PNG)
- Add top and bottom text (with automatic wrapping)
- Adjust font size and stroke width
- Preview and save the meme as PNG
- Cross-platform (Windows/macOS/Linux)

Dependencies:
- Python 3.8+
- Pillow (pip install pillow)

Optional for packaging:
- pyinstaller (pip install pyinstaller)
  pyinstaller --onefile --windowed meme_maker.py

Save this file as meme_maker.py and run: python meme_maker.py
\"\"\"

import os
import textwrap
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, Scale, HORIZONTAL, LEFT, RIGHT, X, Frame, Canvas, NW, CENTER
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Attempt to pick a bold font similar to Impact; fallback to default
def get_default_font(font_size):
    # Common Impact-like font paths on different OSes
    candidates = [
        "/usr/share/fonts/truetype/impact/Impact.ttf",  # linux (unlikely)
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",  # linux msttcorefonts
        "/usr/share/fonts/truetype/impact.ttf",
        "/Library/Fonts/Impact.ttf",  # macOS
        "C:\\Windows\\Fonts\\impact.ttf",  # Windows
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
    # fallback to DejaVuSans-Bold often available
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except Exception:
        return ImageFont.load_default()

class MemeMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Maker - Simple")
        self.image = None
        self.preview_imgtk = None

        control_frame = Frame(root)
        control_frame.pack(fill=X, padx=8, pady=6)

        self.open_btn = Button(control_frame, text="Open Image", command=self.open_image)
        self.open_btn.pack(side=LEFT, padx=4)

        self.save_btn = Button(control_frame, text="Save Meme", command=self.save_meme, state="disabled")
        self.save_btn.pack(side=LEFT, padx=4)

        Label(control_frame, text="Top text:").pack(side=LEFT, padx=(10,0))
        self.top_var = StringVar(value="")
        self.top_entry = Entry(control_frame, textvariable=self.top_var, width=20)
        self.top_entry.pack(side=LEFT, padx=4)

        Label(control_frame, text="Bottom text:").pack(side=LEFT, padx=(10,0))
        self.bottom_var = StringVar(value="")
        self.bottom_entry = Entry(control_frame, textvariable=self.bottom_var, width=20)
        self.bottom_entry.pack(side=LEFT, padx=4)

        size_frame = Frame(root)
        size_frame.pack(fill=X, padx=8)
        Label(size_frame, text="Font size:").pack(side=LEFT)
        self.size_scale = Scale(size_frame, from_=14, to=120, orient=HORIZONTAL)
        self.size_scale.set(40)
        self.size_scale.pack(fill=X, expand=True, padx=6)

        stroke_frame = Frame(root)
        stroke_frame.pack(fill=X, padx=8, pady=(4,8))
        Label(stroke_frame, text="Stroke width:").pack(side=LEFT)
        self.stroke_scale = Scale(stroke_frame, from_=0, to=8, orient=HORIZONTAL)
        self.stroke_scale.set(2)
        self.stroke_scale.pack(fill=X, expand=True, padx=6)

        # Preview canvas
        self.canvas = Canvas(root, width=680, height=400, bg="#333333")
        self.canvas.pack(padx=8, pady=8)

        # Live update bindings
        self.top_var.trace_add("write", lambda *args: self.update_preview())
        self.bottom_var.trace_add("write", lambda *args: self.update_preview())
        self.size_scale.bind("<ButtonRelease-1>", lambda e: self.update_preview())
        self.stroke_scale.bind("<ButtonRelease-1>", lambda e: self.update_preview())

    def open_image(self):
        path = filedialog.askopenfilename(title="Open image", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not path:
            return
        self.image = Image.open(path).convert("RGBA")
        self.img_path = path
        self.save_btn.config(state="normal")
        self.update_preview()

    def draw_text_on_image(self, base_img: Image.Image):
        if not self.image:
            return base_img
        img = base_img.copy()
        draw = ImageDraw.Draw(img)
        w, h = img.size
        font_size = int(self.size_scale.get())
        stroke_w = int(self.stroke_scale.get())
        font = get_default_font(font_size)

        # wrapping helper: target width ~ 90% of image width
        def draw_wrapped_text(text, y, anchor):
            if not text:
                return
            max_width = int(w * 0.95)
            # simple wrap: try wrapping to different char widths
            # estimate chars per line using average character width approximation
            avg_char = font.getsize("A")[0] if hasattr(font, "getsize") else font_size * 0.6
            chars_per_line = max(10, int(max_width / max(1, avg_char)))
            lines = textwrap.wrap(text.upper(), width=chars_per_line)
            total_h = sum([font.getsize(line)[1] for line in lines])
            # vertical spacing: place lines accordingly
            if anchor == "top":
                start_y = y + 0
            else:
                start_y = y - total_h
            for idx, line in enumerate(lines):
                line_w, line_h = font.getsize(line)
                x = w // 2
                line_y = start_y + sum(font.getsize(l)[1] for l in lines[:idx])
                # outline (stroke)
                if stroke_w > 0:
                    # draw multiple offsets for stroke
                    for ox in range(-stroke_w, stroke_w+1):
                        for oy in range(-stroke_w, stroke_w+1):
                            if ox == 0 and oy == 0:
                                continue
                            draw.text((x+ox, line_y+oy), line, font=font, anchor="ms", fill="black")
                # main text (white)
                draw.text((x, line_y), line, font=font, anchor="ms", fill="white")

        draw_wrapped_text(self.top_var.get(), y=int(h*0.02), anchor="top")
        draw_wrapped_text(self.bottom_var.get(), y=int(h*0.98), anchor="bottom")
        return img

    def update_preview(self):
        if not getattr(self, "image", None):
            self.canvas.delete("all")
            self.canvas.create_text(340,200,text="Open an image to start", fill="white", font=("Arial", 16))
            return
        # make a preview sized to canvas while keeping aspect ratio
        canvas_w = int(self.canvas.cget("width"))
        canvas_h = int(self.canvas.cget("height"))
        img_w, img_h = self.image.size
        scale = min(canvas_w / img_w, canvas_h / img_h)
        preview_size = (max(1, int(img_w*scale)), max(1, int(img_h*scale)))
        preview = self.image.resize(preview_size, Image.LANCZOS)
        # draw text on a copy of the preview (so font sizes scale)
        temp = self.draw_text_on_image(preview)
        self.preview_imgtk = ImageTk.PhotoImage(temp)
        self.canvas.delete("all")
        self.canvas.create_image(0,0,anchor=NW,image=self.preview_imgtk)

    def save_meme(self):
        if not getattr(self, "image", None):
            return
        # draw text on original resolution
        final = self.draw_text_on_image(self.image)
        default_name = os.path.splitext(os.path.basename(getattr(self, "img_path", "meme.png")))[0] + "_meme.png"
        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default_name, filetypes=[("PNG image", "*.png")])
        if not save_path:
            return
        final.convert("RGB").save(save_path, "PNG")
        print(f"Saved meme to {save_path}")

if __name__ == "__main__":
    root = Tk()
    app = MemeMaker(root)
    root.mainloop()
