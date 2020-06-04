#######################################################################
#               Godot RST File to MediaWiki converter                 #
#######################################################################

import re
import pandas as pd
import sys

source=sys.argv[1]

with open(source) as file:
    file_contents = file.read()
    
    #Changing line breaks
    file_contents = re.sub("(\r\n?|\n)",'\r',file_contents)

    #Removing github comment
    file_contents = re.sub(":github_url: hide\r\r", "", file_contents)

    #bold
    file_contents = re.sub("\*\*([A-Za-z0-9_\.\"\!\(\) ,@]*)\*\*", "'''\\1'''", file_contents)
    
    #italic
    file_contents = re.sub("\*([A-Za-z_0-9]*)\*", "''\\1''", file_contents)
    
    #listitems
    file_contents = re.sub("\r(\-) ",'*  ',file_contents)

    #Sections anchors
    sections=["property","method","constant","signal"]
    for section in sections:
        file_contents = re.sub("\:ref\:`([A-Za-z_0-9]*)<(class_[a-z_A-Z0-9]*_"+section+"_[a-z_A-Z0-9]*)>`",'[[#\\2|\\1]]',file_contents)

    #Links to other classes
    file_contents = re.sub("(\-)? \:ref\:`([A-Za-z_0-9]*)<class_([a-z_A-Z0-9]*)>`",'[[\\3 GD|\\2]]',file_contents)
    
    #Removing some basic type links
    basic_types=["float","bool","int","bool"]
    for basic_type in basic_types:
        file_contents = re.sub("\[\["+basic_type+" GD\|"+basic_type+"\]\]",basic_type,file_contents)
    
    #table
    file_contents = re.sub("\|\r\+([\-]*\+){1,}\r\|","\r|-\r|", file_contents)
    file_contents = re.sub("\|\r\+([\-]*\+){1,}","\r|}", file_contents)
    file_contents = re.sub("\+([\-]*\+){1,}\r\|",'{| class="wikitable \r|', file_contents)
    file_contents = re.sub("( ){1,}\|",'||', file_contents)

    #removing --- and ===
    file_contents = re.sub("(\-){3,}|(\=){3,}\r",'', file_contents)
    
    #applying highlight box style
    style=" style='background-color:#434649; padding-left:3px; color:#ffaa94; padding-right:3px; border:1px; border-color:#505356; border-style:solid;'"
    file_contents = re.sub("\`\`([A-Za-z0-9_\.\"\!\(\) ,@]*)\`\`","<span class='highlight_box'"+style+">\\1</span>", file_contents)
    
    #Section titles
    sections=["Description","Method Descriptions","Methods","Property Descriptions","Properties","Signals"]
    for section in sections:
            file_contents = file_contents.replace(section+"\r","== "+section+" ==\r")

    #adding missing space before links
    file_contents = re.sub("([a-z])\[\[","\\1 [[",file_contents)

    #fixin bold problems
    file_contents = file_contents.replace("''''","'''")
    file_contents = file_contents.replace("'''[","''' [")
    file_contents = file_contents.replace("''' '''(''' ''')'''","()'''")
    
    #hiding TOC
    file_contents="__NOTOC__\r"+file_contents

 
    #line by line processing

    lines = file_contents.splitlines()

    exported = ""

    #anchors
    for line in lines:
        s=re.search("^\.\.",line)
        if s:
            line=re.sub("^\.\. _([A-Za-z0-9_]*)\:","<span id='\\1'></span>",line)

        #removing top comments
        if re.search("^\.\.",line):
            line=''
        else:
            line+="\r"

        exported+=line

    #removing unused class name
    exported=re.sub("</span>\r\r([A-Za-z0-9_]*)\r\r'''","'''",exported)

    #removing some linebreaks when more than 2
    exported=re.sub("\r{3,}","\r\r",exported)

    with open(sys.argv[1]+".mw", "w") as output_file:
        output_file.write(exported)

