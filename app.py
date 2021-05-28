#!/bin/python3

import sys
import os

words = sys.argv
if len(words) > 1:
    words.pop(0)
    print(words)
else:
    print("Invalid syntax!")
    print("Syntax: python3 app.py word1 word2 etc")
