import os
#import magic
from app import app

import json
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter #process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO





Education = ['ecole','national','ingénieur','école','institut','supérieure','supérieur','superieur','superieure','universitaire','université',"universite","faculté"]
LangueList = ['arabic','francais','anglais','english','french','arabe','français','allmend','german','spanish','espagnol']
Project_words = ['project', 'projet','projets','projects','application','applications','mobile','web','developpement','développement','gestion','Backend','frontend',"fin","d'année",'pfa']
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../templates/static/Prog.txt")
Prog_Lang = open(path,'r')
prog_list=[]
line = Prog_Lang.readline()
while(line):
    prog_list.append(str(line).rstrip().lower())
    line = Prog_Lang.readline()



def getinfo(result , request,filename):
    with open(os.path.join(my_path, "../templates/Files/data.txt"), 'r') as json_file:
        data = json.load(json_file)
        l = len(data)
    combined = [l , result , request, filename]
    data.append(combined)
    with open(os.path.join(my_path, "../templates/Files/data.txt"), 'w') as outfile:
         json.dump(data, outfile)
    return json.dumps( combined )


def maketxt(path):
    print(path)
    fp = open(path,'rb')
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp):
         interpreter.process_page(page)
    # Get text from StringIO
    text = sio.getvalue()
    fp.close()
    txt1 = text.split('\n\n')
    txt2 = []
    for x in txt1:
        x = x.replace('\n', ' ')
        x = x.replace(',', ' ')
        txt2.append(x)
    return txt2


def getreslt(txt):
    jsonFile = {
    "Email":[],
    "Institution":[],
    "Langue":[],
    "Skill":[],
    "Project":[],
    "PhoneNumber":[]
    }
    Email=""
    Inst=""
    PragrammingTools = []
    langue = []
    Projects =[]
    Max =0
    number =[]
    for tex in txt:
         #features['Name'],features['LastName'] = getFullName(tex)
         Email = getEmail(tex)
         if(Email) :
            jsonFile["Email"].append(Email)
         jsonFile["Institution"].append(getInstitiutions(tex))
         jsonFile["Institution"] = [x for x in jsonFile["Institution"] if x !=None]
         jsonFile["Skill"].append(getProg(tex))
         jsonFile["Skill"] = [x for x in jsonFile["Skill"] if x !='']
         jsonFile["Langue"].append(getLangue(tex))
         jsonFile["Project"].append(getProject(tex))
         jsonFile["Project"] = [x for x in jsonFile["Project"] if x != None]
         jsonFile["PhoneNumber"].append(getNumber(tex))
         jsonFile["Langue"] = [x for x in jsonFile["Langue"] if x !=[]]
         jsonFile["PhoneNumber"] = [x for x in jsonFile["PhoneNumber"] if x !=None]
    return jsonFile
def getNumber(myStr):
    r = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{6,}[0-9]', myStr)
    if(r != []):
        number = r[0]
        for nbr in number:
            if(nbr in ['/','-']) :
                return([])
        return(r[0])
def getEmail(string):
    email=""
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", string)
    while(1):
        if emails == [] :
            break
        email =emails.pop(0)
        if emails == [] :
            break
    return(email)
def getInstitiutions(myStr):
    txt = myStr.split(' ')
    s=0;prob=0
    for tex in txt :
        if(tex.lower() in Education):
            prob+=1
    if(prob >= 2):
        return myStr
def getProg(myStr):
    listofProg = ""
    txt = myStr.split(' ')
    for tex in txt :
        if(tex.lower() in prog_list):
            listofProg += " " + tex
    return listofProg
def getLangue(myStr):
    lang = []
    txt = myStr.split(' ')
    for tex in txt :
        if(tex.lower() in LangueList):
            lang.append(tex)
    return lang
def getProject(myStr):
    tex = myStr.split(' ')
    if(len(tex) < 8):
        return
    nbr=0
    for x in tex:
        if(x.lower() in Project_words):
            nbr += 1
    if(nbr >= 2 ):
        return(myStr)
