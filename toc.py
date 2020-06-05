#######################################################################
#             Godot RST Files to  TOC MediaWiki converter             #
#######################################################################

import re
import pandas as pd
import sys
import os

list_class=[]
for element in os.listdir('./'):
    if element.endswith('.rst'):
        
        with open(element) as file:
            file_contents = file.read()

            class_name=file_contents.splitlines()[8]

            list_class.append(class_name)

initials="@ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for initial in initials:
    print ("== "+initial+" ==")
    for c in list_class:
        if c.startswith(initial):
            print("[["+c+" GD|"+c+"]]\r")
    print ("\r")

