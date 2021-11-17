import json 
from re import search

# open json file
with open('peraturan.json') as f_peraturan:
  allPeraturan = json.load(f_peraturan)
with open('putusan.json') as f_putusan:
   allPutusan = json.load(f_putusan)

# take input
#getInput = input('')
#text = getInput.lower()

# slice the string 
# append the putusan list inside peraturan list
#for putusan in allPutusan:
#    if search("Undang-Undang Nomor 19 Tahun 2016", putusan['pokokPerkara']):
#        print(putusan)

for peraturan in allPeraturan:
    for putusan in allPutusan:
        if search( "Undang-undang (UU) Nomor 46 Tahun 2009", putusan['pokokPerkara'] ):
            print(True)

            #putusan.append(allPeraturan)
            #print(allPeraturan)
# iteratable
#for i in dataPeraturan:
#    if getInput in i['peraturanName']:
#        print (i['peraturanName']+" tentang "+i['peraturanDescription'] + " ["+ i['link'] + "]")
    
# Closing file
f_peraturan.close()
f_putusan.close()
