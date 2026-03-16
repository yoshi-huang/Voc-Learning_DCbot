import csv

voc=[]

with open('voc7000.csv', 'r', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:

        word = row[0].split("@")[0]
        if not word.isalpha(): 
            word = word.split('"')[0]

        trans = row[0].split(".")[1].split('"')[0][2:]
        try:
            if trans[0] == ")": trans = trans[1:]
        except: pass

        part_of_speech = row[0].split("(")[1].split(".")[0]+"."
        Level = int(row[1])
        
        voc.append([Level,word,part_of_speech,trans.split('"')[0]])
    
with open('o.csv', 'w', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for i in voc:
        spamwriter.writerow(i)