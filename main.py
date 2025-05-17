from morse import *
import os
import importlib

packages = ['numpy', 'simpleaudio']

def check_required_packages(packages):
    missing = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        return False
    return True

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def main_menu():
    cls()
    check_required_packages(packages)
    morse = MorsePlayer(wpm=20, tone=600)
    text = input("Enter text to convert to Morse: ")
    print("Converted => " + morse.to_morse(text))
    morse.play(text)

if __name__ == "__main__":
    main_menu()