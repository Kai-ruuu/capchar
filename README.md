# Capchar

**Capchar** is a simple tool I built to help create reviewers from images by capturing the text and copying it to the clipboard, enabling me to paste it into a flashcards creation website to help me prepare for my exams. It utilizes Tesseract OCR for capturing text from images and python's tkinter library to highlight or select a region to capture.

## Main Requirement
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed at:  
  `C:\Program Files\Tesseract-OCR\tesseract.exe`

## Installation & Running
1. Open Command Prompt and navigate to the root directory of the project.
2. Install python requirements with:
   ```bash
   pip install -r requirements.txt
2. Run the program with:  
   ```bash
   py main.py

| Action                                   | Shortcut           |
| ---------------------------------------- | ------------------ |
| Capture text and preserve newlines       | **Ctrl + Alt + L** |
| Capture text without preserving newlines | **Ctrl + Alt + X** |
| Terminate the program                    | **Ctrl + Alt + D** |
