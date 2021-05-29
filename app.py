#!/bin/python3

import sys
import os
import json
from termcolor import cprint
from difflib import get_close_matches


class Dictionary:
    def __init__(self):
        os.system('cls||clear')
        print('Running...')
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

    def find_unknown(self, u_words):
        for word in u_words:
            cprint('-' * 50, color='yellow')
            possibilities = get_close_matches(word, self.data.keys())
            if len(possibilities) == 0:
                cprint(f"[-] Please double check the word {word}", color='red')
                continue
            possibilities.append('None')
            cprint(f'[*] {word}', 'yellow')
            for index, item in enumerate(possibilities):
                print(f'{index}. {item}')
            print('Please select correct word: ', end="")
            choice = int(input())
            sys.stdout.write("\033[F" * (len(possibilities) + 2))
            if possibilities[-1] == possibilities[choice]:
                cprint(f"!!! Sorry unable to find word {word}", color='red')
            else:
                cprint(f'[+] {possibilities[choice].capitalize()}', color='green')
                meaning = self.data.get(possibilities[choice])
                for item in meaning:
                    cprint(f'-> {item}', 'cyan')
        cprint('-' * 50, color='yellow')

    def find(self):
        unknown_words = []
        for word in self.words:
            meaning = self.data.get(word)
            if meaning:
                cprint('-' * 50, color='yellow')
                cprint(f'[+] {word.capitalize()}', color='green')
                for item in meaning:
                    cprint(f'-> {item}', 'cyan')
            else:
                unknown_words.append(word)
        if unknown_words:
            self.find_unknown(unknown_words)
        else:
            cprint('-' * 50, color='yellow')


my_dict = Dictionary()
my_dict.find()
print('Stopped...')
