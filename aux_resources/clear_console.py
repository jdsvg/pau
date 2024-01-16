import os

class Clear_console:
    def __init__(self):
        if os.name == 'nt':os.system('cls')
        else:os.system('clear')