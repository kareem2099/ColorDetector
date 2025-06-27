import pyperclip

def copy_with_message(text, format_name):
    pyperclip.copy(text)
    print(f"Successfully copied {format_name} to clipboard: {text}")
