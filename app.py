#!/bin/python3

import sys
import os
import json
from termcolor import cprint


class Dictionary:
    def __init__(self):
        self.words = set(item.lower() for item in sys.argv[1:])
        if not self.words:
            cprint("[-] Invalid syntax!", 'red')
            cprint("[-] Syntax: python3 app.py word1 word2 etc", 'red')
            sys.exit()
        if os.path.exists("data/data.json"):
            self.data = json.load(open("data/data.json"))
        else:
            print("[-] Data file not found!", 'red')
            sys.exit()

    def find(self):
        for word in self.words:
            cprint('-' * 50, color='yellow')
            cprint(f'[+] {word.capitalize()}', color='green', attrs=['bold'])
            meaning = self.data.get(word)
            if meaning:
                for item in meaning:
                    cprint(f'-> {item}', 'cyan')
            else:
                cprint("!!! Please double check the word", color='red')
        cprint('-' * 50, color='yellow')


my_dict = Dictionary()
my_dict.find()
