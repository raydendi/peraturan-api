import json 
import re
from re import search

# open json file
with open('peraturan.json') as f_peraturan:
  allPeraturan = json.load(f_peraturan)
with open('putusan.json') as f_putusan:
   allPutusan = json.load(f_putusan)

# take input
#getInput = input('')
#text = getInput


for peraturan, putusan in zip(allPeraturan, allPutusan) :
    #nomorPeraturan = peraturan['peraturanName']
    nomorPeraturan = r"13 tahun 2003"
    a = re.search(nomorPeraturan,peraturan['peraturanName'], re.I)
    b = re.search(nomorPeraturan, putusan['pokokPerkara'], re.I )
    if  a == True and b == True:
        print(peraturan, putusan)
    elif a == True and b == False:
        print(peraturan)
    
# Closing file
f_peraturan.close()
f_putusan.close()
