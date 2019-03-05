#==========================================================================
#Imports
#==========================================================================
import os, eml_parser

#==========================================================================
#Options: Unless you know what you're doing ONLY edit these
#==========================================================================
path = "J:\\Documents\\Old Laptop Emails (Prior 03-02-2019)"

#==========================================================================
#Functions
#==========================================================================
def fixWindowsFilename(string):
    illegalChars = '\\.<>:"/|?*+,;=[]'
    newString = ""

    #Remove illigal characters
    for char in string:        
        if char in illegalChars or ord(char) < 31 or ord(char) > 127:
            newString += "_"
        else:
            newString += char
            
    newString = newString.strip()
    
    while "__" in newString: newString = newString.replace("__", "_")
    while "_ " in newString: newString = newString.replace("_ ", " ")
    while "  " in newString: newString = newString.replace("  ", " ")
    
    return newString   
            
def renameFile(file):
    #Get file details
    ext = os.path.splitext(file)[1]
    subdir = os.path.normpath(os.path.splitext(file)[0] + os.sep + os.pardir)

    #Make sure it is an email file, if not delete it 
    if ext != ".eml":
        os.remove(file)
        return
    
    #Find subject line
    name = ""
    #print(file)
    with open(file, "rb") as f:
        raw_eml = f.read()
    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_eml)
    name = parsed_eml["header"]["subject"]
    name = fixWindowsFilename(name)

    #remove empty/invalid files
    if name == "":
        os.remove(file)
        return

    #output
    print(name)

    #add numbers if file exists (abc = abc_2)
    newFilePath = os.path.join(subdir, name+ext)
    if os.path.exists(newFilePath):
        count = 2
        addition = ""
        if not name.endswith("_"): addition = "_"
        
        while os.path.exists(newFilePath):
            newFilePath = os.path.join(subdir, name+addition+str(count)+ext)
            count += 1

    #Make sure name is under max pathlength
    if len(newFilePath) > 240:
        newFilePath = newFilePath[:-4][:240] + "_etc_.eml"
        
    #Rename file
    os.rename(file, newFilePath)
   
def fixFiles(rootDir):
    #Itterate through files
    for subdir, dirs, files in os.walk(rootDir):
        for f in files:
            renameFile(os.path.join(subdir, f))
    
#==========================================================================
#Run
#==========================================================================
fixFiles(path)
input("\n\nProgram complete. Press enter to continue.")


