Meme Maker (Tkinter + Pillow)
=============================

Files created:
- /mnt/data/meme_maker.py  -> the GUI script
- /mnt/data/README_meme_maker.txt -> this file

How to run
----------
1. Make sure you have Python 3.8+ installed.
2. Install Pillow:
   pip install pillow
3. Run the script:
   python /mnt/data/meme_maker.py
4. Use "Open Image" to select a photo, type top/bottom text, adjust font size and stroke, then click "Save Meme".

Packaging into a single executable (optional)
--------------------------------------------
Install pyinstaller:
   pip install pyinstaller
Create a one-file, windowed executable:
   pyinstaller --onefile --windowed meme_maker.py
The produced executable will be in the 'dist' folder after PyInstaller finishes.

Notes & tips
-----------
- If the Impact font isn't available on your system, the script falls back to DejaVuSans-Bold or the default PIL font.
- For best-looking memes, use wide images and larger font sizes.
- If you want fancier fonts, install an Impact-like font and update the font path in the script.
