import re
import sys
import os

tmpfile = 'tmp.txt'

trinket = False
files = False
if "--trinket" in sys.argv:
    trinket = True
    intrinketfiles = False
    sys.stdout = open(tmpfile, "w")
    if "--files" in sys.argv:
        files = True 

while True:
    try:
        line = input()
    except:
        break
    
    # Use . instead of backslash to avoid regex weirdness across python versions
    x = re.findall(r'^.VerbatimInput{(.*)}', line)
    if not x : 
        if trinket and files:
            trinketfilesstart = r"\begin{trinketfiles}" in line
            trinketfilesstop = r"\end{trinketfiles}" in line
            if trinketfilesstart:
                # We've found extra trinket files to include
                print('<--')
                intrinketfiles = True
                continue
            elif trinketfilesstop:
                # We're at the end of this block
                print('-->')
                intrinketfiles = False
                continue
            elif intrinketfiles:
                # We're in a trinket files block; include the file
                print("----{" + os.path.basename(line) + "}----")
                with open(line) as filetoinclude:
                    print(filetoinclude.read())
                continue
            else:
                # Otherwise, move on
                print(line)
                continue
        else:
            print(line)
            continue
    fn = x[0]
    
    
    
    with open(fn) as fh:
        
        # Pre code
        
        # Open Wrapper
        if trinket:
            with open('trinket/trinket-script') as ts:
                print(ts.read())
        else:        
            print('~~~~ {.python}')
            blank = True
        
        # Code
        for ln in fh:
            print(ln.rstrip())
            blank = len(ln.strip()) > 0 
        
        # Post Code
        
        # Cannonical URL
        if fn.startswith('../') :
            # Add a blank unless there is one at end of file
            if blank : print() 
            fu = fn.replace('../','https://www.py4e.com/')
            print('# Code:', fu)
            if trinket:
                print("# Or select Download from this trinket's left-hand menu")
        
        # Close wrapper
        if trinket:
            print('-->')
        else:
            print('~~~~')

