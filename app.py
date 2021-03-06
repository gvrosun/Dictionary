#!/bin/python3

import sys
import os
import json  # To load json file
from termcolor import cprint  # To display content in colors in terminal
from difflib import get_close_matches  # To find possible words
import mysql.connector as mysql
import time
import threading


class Dictionary:
    def __init__(self, usage: str):
        """
        This class used to find meaning of the given word as well as meaning of the word.\n
        Example1: my_app = Dictionary(usage='local')
        Example2: my_app = Dictionary(usage='database')\n
        :param usage: choose local or database
        """
        # Clearing terminal
        os.system('cls||clear')
        self.words = set(item.lower() for item in sys.argv[1:])
        self.usage = usage
        self._file_path = 'dataa/data.json'
        self.check = True

        # Check user gave command-line input or not
        if not self.words:
            cprint("[-] Invalid syntax!", 'red')
            cprint("[-] Syntax: python3 app.py word1 word2 etc", 'red')
            sys.exit()

        if usage == 'local':
            # Check data file exist or not
            loading_thread = threading.Thread(name='loading', target=self.animated_loading,
                                              args=("[*] Loading data file ",))
            loading_thread.start()
            if os.path.exists(self._file_path):
                self.data = json.load(open(self._file_path))
                self.check = False
                if loading_thread.is_alive():
                    time.sleep(1)
                sys.stdout.write("\033[F")
                cprint('[+] Data file loaded...\n', 'green')
            else:
                self.check = False
                if loading_thread.is_alive():
                    time.sleep(1)
                sys.stdout.write("\033[F")
                cprint('[-] Data file not found!', 'red')
                cprint('[*] Switching to online mode...', 'yellow')
                self.usage = 'database'

        if self.usage == 'database':
            # Setting up database
            self.check = True
            loading_thread = threading.Thread(name='loading', target=self.animated_loading,
                                              args=("[*] Connecting to mysql server ", ))
            loading_thread.start()
            try:
                self.con = mysql.connect(
                    user="ardit700_student",
                    password="ardit700_student",
                    host="108.167.140.122",
                    database="ardit700_pm1database"
                )
                self.check = False
                self.cursor = self.con.cursor()
                # sys.stdout.write("\033[F")
                if loading_thread.is_alive():
                    time.sleep(1)
                cprint('[+] Connected to database server\n', 'green')
            except mysql.errors.InterfaceError:
                cprint('[-] Please check your internet connection and try again', 'red')
                sys.exit()

        elif self.usage != 'local':
            # If invalid value for usage
            raise Exception(f'Invalid argument \'{usage}\' Expected: \'local\' or \'database\'')

    def animated_loading(self, data):
        chars = ['/', '???', '\\', '|']
        while self.check:
            for char in chars:
                cprint(data + char, 'yellow')
                sys.stdout.write("\033[F")
                time.sleep(.1)

    def _get_meaning_from_database(self, expression):
        self.cursor.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{expression}'")
        meaning = self.cursor.fetchall()
        if meaning:
            meaning = [data[0] for data in meaning]
        return meaning

    def _find_unknown(self, u_words: list) -> None:
        """
        This function gets a list of unknown words and finds possible related words and prints the meaning...
        :param u_words: list of unknown words
        :return: None
        """
        # Get expressions based on usage
        self.check = True
        print()
        loading_thread = threading.Thread(name='loading', target=self.animated_loading,
                                          args=("[*] Trying to find unknown words ",))
        loading_thread.start()
        if self.usage == 'local':
            expressions = self.data.keys()
        else:
            self.cursor.execute(f"SELECT Expression FROM Dictionary")
            expressions = set([data[0] for data in self.cursor.fetchall()])
        self.check = False
        if loading_thread.is_alive():
            time.sleep(1)

        # Iterate over unknown words list
        for word in u_words:
            cprint('-' * 100, color='yellow')
            possibilities = get_close_matches(word, expressions)

            # Skip word if can not find possible word
            if len(possibilities) == 0:
                cprint(f"[-] Please double check the word {word}", color='red')
                continue

            possibilities.append('None of the above')
            cprint(f'[*] {word}', 'yellow', end="")
            print(" " * 50)

            # Printing possible words to enable user to choose one...
            for index, item in enumerate(possibilities):
                cprint(f'{index}. {item}', attrs=['dark'], flush=True, end="")
                print(" " * 50)

            # Getting input and cleaning
            print(f'Please select correct word (default: {possibilities[0]}): ', end="")
            try:
                choice = input()
            except KeyboardInterrupt:
                print("\n\nBye bye...")
                sys.exit()

            if choice == '':
                choice = 0
            else:
                choice = int(choice)

            choice_word = possibilities[choice]
            sys.stdout.write("\033[F" * (len(possibilities) + 2))  # Moving cursor to front...
            sys.stdout.flush()

            # Skip if user chosen none of the above
            if possibilities[-1] == choice_word:
                cprint(f"!!! Sorry unable to find word {word}", color='red')

            # Else print meaning of the word.
            else:
                cprint(f'[+] {choice_word.capitalize()}', color='green', end="")
                print(" " * 50)
                if self.usage == 'local':
                    meaning = self.data.get(choice_word)
                else:
                    meaning = self._get_meaning_from_database(choice_word)

                for item in meaning:
                    cprint(f'-> {item}', 'cyan')

        cprint('-' * 100, color='yellow')  # Just for decoration

    def find(self) -> None:
        """
        This function finds meaning of the words given
        :return: None
        """
        unknown_words = []

        # Iterate over all input words
        for word in self.words:
            if self.usage == 'local':
                meaning = self.data.get(word)
            else:
                meaning = self._get_meaning_from_database(word)

            # if word is correct
            if meaning:
                cprint('-' * 100, color='yellow')
                cprint(f'[+] {word.capitalize()}', color='green')
                for item in meaning:
                    cprint(f'-> {item}', 'cyan')
            else:
                # if word is wrong add to unknown list
                unknown_words.append(word)

        if unknown_words:
            # Send unknown list to this function to find possible words...
            self._find_unknown(unknown_words)
        else:
            cprint('-' * 100, color='yellow')


if __name__ == '__main__':
    my_dict = Dictionary(usage='local')
    my_dict.find()
    print('Stopped...')
