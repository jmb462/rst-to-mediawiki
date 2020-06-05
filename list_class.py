#######################################################################
#               Godot RST File to MediaWiki converter                 #
#######################################################################

import re
import pandas as pd
import sys

source=sys.argv[1]

with open(source) as file:
    file_contents = file.read()

    class_name=file_contents.splitlines()[8]


    print("<tr><td><a target=_blank href='http://godotestarrive.ovh/index.php?title="+class_name+"_GD&action=edit'>Wiki "+class_name+"</a></td>")
    print("<td><a target=_new href='mw/"+class_name+".mw'>"+class_name+" MW File</a></td></tr>")
