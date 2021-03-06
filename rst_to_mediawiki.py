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

    #fixing syntax error in some rst file...
    file_contents = file_contents.replace("[code]","``")

    #removing base type link
    file_contents = file_contents.replace(":ref:`float<class_float>`","float")
    file_contents = file_contents.replace(":ref:`int<class_int>`","int")
    file_contents = file_contents.replace(":ref:`bool<class_bool>`","bool")
    

    #Changing line breaks
    file_contents = re.sub("(\r\n?|\n)",'\r',file_contents)

    #Sections titles
    file_contents = re.sub("\r([@A-Za-z _]+)\r\-{4,}","\r== \\1 ==\r",file_contents)

    #remove class name and title
    file_contents = re.sub("\\r\.\. _class_[A-Za-z0-9_\.\"\!\(\) ,@]*\:\\r\\r[A-Za-z0-9_\.\"\!\(\) ,@]*\\r={2,}\\r","",file_contents)

    #Removing github comment
    file_contents = re.sub(":github_url: hide\r\r", "", file_contents)

    #parent overide tag
    file_contents = re.sub("\*{2}O:\*{2} ``([^`]+)``", "``\\1`` (parent override)", file_contents)
    
    #bold
    file_contents = re.sub("\*\*([A-Za-z0-9_\.\"\!\(\) ,@]*)\*\*", "'''\\1'''", file_contents)
    
    #italic
    file_contents = re.sub("\*([A-Za-z_0-9]*)\*", "''\\1''", file_contents)
    
    #listitems
    file_contents = re.sub("\r(\-) ",'*  ',file_contents)

    
    #table
    file_contents = re.sub("\|\r\+([\-]*\+){1,}\r\|","\r|-\r|", file_contents)
    file_contents = re.sub("\|\r\+([\-]*\+){1,}","\r|}", file_contents)
    file_contents = re.sub("\+([\-]*\+){1,}\r\|",'{| class="wikitable \r|', file_contents)
    file_contents = re.sub("( ){1,}\|",'||', file_contents)
    
    #Method in a class
    file_contents=re.sub("\:ref\:`([A-Z_][A-Za-z0-9_\.@]*)<class_([A-Z][A-Za-z0-9_\.@]*)_method_([A-Z_][A-Za-z0-9_\.@]*)>`","[[\\2 GD#\\3|\\3]]",file_contents)
   
    #Other class with method
    file_contents=re.sub("\:ref\:`([A-Z@][A-Za-z0-9_@]*)\.([A-Za-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_method_([A-Za-z0-9_\.@]*)\>`","[[\\1 GD#\\2|\\1.\\2()]]",file_contents)
    #Other class with property
    file_contents=re.sub("\:ref\:`([A-Z@][A-Za-z0-9_@]*)\.([A-Z/a-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_property_([A-Za-z0-9/_\.@]*)\>`","[[\\1 GD#\\2|\\1.\\2()]]",file_contents)
    
    #Other class with signal
    file_contents=re.sub("\:ref\:`([A-Z@][A-Za-z0-9_@]*)\.([A-Za-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_signal_([A-Za-z0-9_\.@]*)\>`","[[\\1 GD#\\2|\\1.\\2()]]",file_contents)
    #Other class with constant
    file_contents=re.sub("\:ref\:`([A-Z@][A-Za-z0-9_@]*)\.([A-Za-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_constant_([A-Za-z0-9_\.@]*)\>`","[[\\1 GD#\\2|\\1.\\2()]]",file_contents)
    #Other class with enum global scope
    file_contents=re.sub("\:ref\:`([A-Z][A-Za-z0-9_@\.]*)<enum_@GlobalScope_([A-Za-z0-9_@\.]*)>`","[[@GlobalScope GD#\\2|\\1]]",file_contents)

    file_contents=re.sub(":ref:`([@][A-Za-z0-9_@\.]*)<class_@GlobalScope_constant_([A-Z_a-z0-9@]*)>`","[[@GlobalScope GD#\\2|\\1]]",file_contents)
    
    #Constant in the same class
    file_contents=re.sub("\:ref\:`([A-Z][A-Za-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_constant_([A-Za-z0-9_\.@]*)\>`","[[\\2 GD#\\3|\\3]]",file_contents)

    #property in the same class
    file_contents=re.sub("\:ref\:`([_A-Z][A-Za-z0-9_@]*)<class_([A-Za-z0-9_\.@]*)_property_([_A-Za-z0-9_\.@]*)\>`","[[#\\1|\\1]]",file_contents)

    #Enum in the same class
    file_contents=re.sub("\:ref\:`([A-Z][A-Za-z0-9_@]*)<enum_([A-Za-z0-9_@]*)>`","[[#\\1|\\1]]",file_contents)
    file_contents=re.sub("\:ref\:`([A-Z][A-Za-z0-9_@]*)<enum_([A-Za-z0-9_@]*)>`","[[#\\1|\\1]]",file_contents)
    
    file_contents=re.sub("\:ref\:`([A-Z@][A-Za-z0-9_\.@]*)<class_([A-Za-z0-9_\.@]*)\>`","[[\\2 GD|\\1]]",file_contents)

    #inner class link
    file_contents=re.sub("\:ref\:`([a-z][A-Za-z0-9_\.@]*)<([A-Za-z0-9_\.@]*)\>`","[[#\\1|\\1]]",file_contents)
    
    #inner class link with /
    file_contents=re.sub("\:ref\:`([a-z][A-Za-z0-9_\.@/]*)<class_[A-Za-z0-9_\.@/]*_property_([a-z][A-Za-z0-9_\.@/]*)>`","[[#\\1|\\1]]",file_contents)
    
    
    #external links
    file_contents = re.sub("`([A-Za-z0-9@ ]*) <([A-Za-z0-9@#:/\._]*)>`_" ,'[\\2 \\1]',file_contents)

    #Removing some basic type links
    basic_types=["float","bool","int","bool"]
    for basic_type in basic_types:
        file_contents = re.sub("\[\["+basic_type+" GD\|"+basic_type+"\]\]",basic_type,file_contents)
    
    


    #removing --- and ===
    file_contents = re.sub("(\-){3,}|(\=){3,}\r",'', file_contents)
    
    #applying highlight box style
    #style=" style='background-color:#434649; padding-left:3px; color:#ffaa94; padding-right:3px; border:1px; border-color:#505356; border-style:solid;'"
    #style=''
    #file_contents = re.sub("\`\`([^`]+)``","<span class='highlight_box'"+style+">\\1</span>", file_contents)
    file_contents = re.sub("\`\`([^`]+)``","{{Span|\\1}}", file_contents)

    #Section titles
    #sections=["Enumerations","Description","Method Descriptions","Tutorials","Methods","Constants","Theme Properties","Property Descriptions","Properties","Signals"]
    #for section in sections:
    #        file_contents = file_contents.replace(section+"\r","== "+section+" ==\r")
    
    
    #adding missing space before links
    file_contents = re.sub("([a-z])\[\[","\\1 [[",file_contents)

    #fixin bold problems
    file_contents = file_contents.replace("''''","'''")
    file_contents = file_contents.replace("'''[","''' [")
    file_contents = file_contents.replace("''' '''(''' ''')'''"," ( )'''")
    
    #hiding TOC
    file_contents="__NOTOC__\r"+file_contents

 
    #line by line processing

    lines = file_contents.splitlines()

    exported = ""

    #anchors
    for line in lines:
        s=re.search("^\.\.",line)
        if s:
            sections=["property","method","constant","constants","signal"]
            for section in sections:
                line=re.sub("^\.\. _.*_"+section+"_([A-Za-z_@0-9]*):","=== \\1 ===",line)
            #enum anchors
            line=re.sub("^\.\. _([A-Za-z0-9_]*)_([A-Za-z0-9_/]*):","=== \\2 ===",line)
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

    with open("class_"+class_name+"_GD.mw", "w") as output_file:
        output_file.write(exported)

