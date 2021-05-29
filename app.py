#!/bin/python3

import sys
import os
import json  # To load json file
from termcolor import cprint  # To display content in colors in terminal
from difflib import get_close_matches  # To find possible words


class Dictionary:
    """
    This class used to find meaning of the given word
    """
    def __init__(self):
        # Clearing terminal
        os.system('cls||clear')
        self.words = set(item.lower() for item in sys.argv[1:])

        # Check user gave command-line input or not
        if not self.words:
            cprint("[-] Invalid syntax!", 'red')
            cprint("[-] Syntax: python3 app.py word1 word2 etc", 'red')
            sys.exit()

        # Check data file exist or not
        if os.path.exists("data/data.json"):
            self.data = json.load(open("data/data.json"))
        else:
            print("[-] Data file not found!", 'red')
            sys.exit()

    def _find_unknown(self, u_words: list) -> None:
        """
        This function gets a list of unknown words and finds possible related words and prints the meaning...
        :param u_words: list of unknown words
        :return: None
        """
        # Iterate over unknown words list
        for word in u_words:
            cprint('-' * 100, color='yellow')
            possibilities = get_close_matches(word, self.data.keys())

            # Skip word if can not find possible word
            if len(possibilities) == 0:
                cprint(f"[-] Please double check the word {word}", color='red')
                continue

            possibilities.append('None of the above')
            cprint(f'[*] {word}', 'yellow', end="")
            print(" "*20)

            # Printing possible words to enable user to choose one...
            for index, item in enumerate(possibilities):
                cprint(f'{index}. {item}', attrs=['dark'], end="")
                print(" "*20)

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

            # Skip if user chosen none of the above
            if possibilities[-1] == choice_word:
                cprint(f"!!! Sorry unable to find word {word}", color='red')

            # Else print meaning of the word.
            else:
                cprint(f'[+] {choice_word.capitalize()}', color='green', end="")
                print(" "*20)
                meaning = self.data.get(choice_word)

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
            meaning = self.data.get(word)

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
    my_dict = Dictionary()
    my_dict.find()
    print('Stopped...')
