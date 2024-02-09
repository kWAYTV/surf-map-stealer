import os
from pyfiglet import Figlet
from pystyle import Colors, Colorate, Center

class Utils:
    def __init__(self):
        pass

    def clear(self):
        os.system("cls||clear")

    def print_logo(self, logo_text: str = "Map Stealer", logo_font: str = "big"):
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, Figlet(font=logo_font).renderText(logo_text), 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────", 1)))