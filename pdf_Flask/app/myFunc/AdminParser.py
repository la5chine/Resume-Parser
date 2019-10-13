
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
import pandas as pd
from flask import jsonify

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
        x.strip()
        if x not in [' ', '']:
            txt2.append(x)
    return txt2

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../templates/static/Skills.csv")
df = pd.read_csv(path)
cols = [x for x in df.columns]
summary = {}
for col in cols:
	summary[col] = {}
	genre = df[col].dropna(axis = 0)
	for gen in genre:
		summary[col][gen] = 0


def costum():
    All = {}
    with open(os.path.join(my_path, "../templates/Files", "data.txt")) as json_file:
        data = json.load(json_file)
        l = len(data)
    k = l - 1
    while (k >= 0):
        txt = maketxt(os.path.join(my_path, "../templates/Files", str(k) + ".pdf"))
        mysumm = summary
        mysumm["Applicant"] = data[1][2]['Name']
        for x in txt:
            for col in cols:
                genre = df[col].dropna(axis = 0)
                for gen in genre:
                    if(gen in x):
                        mysumm[col][gen] += 1
        All[data[k][2]['Name']] = mysumm
        k -= 1
    return (All)
