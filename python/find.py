from csv import reader as csv_reader

from W2V_Relative import load_google_word2vec, vocList
from W2V_Relative import similar_above_threshold as resemb

# ------------------------------------------
# initialization
# ------------------------------------------

VOCLST = vocList()
with open('voc7000.csv', 'r', newline='', encoding='utf-8') as voc6000:
    vocs = csv_reader(voc6000, delimiter=',')
    for voc in vocs:
        VOCLST.append(Level=voc[0], voc=voc[1], part_of_speech=voc[2], translate=voc[3])

wv = load_google_word2vec(path="GoogleNews-vectors-negative300.bin")
print("len of vocabulary list:", len(VOCLST.voc))

# ------------------------------------------
# find resemble word function
# ------------------------------------------

def find_resemble_word(target_word, threshold_value:int = 0.5):

    top_words = resemb(target_word, VOCLST.voc, threshold=threshold_value, wv=wv)
    result=[]

    for w, score in top_words:
        word = VOCLST.get(VOCLST.voc.index(w))

        if word['vocabulary'] != target_word :
            vocabulary = (word['Level'], word['vocabulary'], word['translate'], word['part_of_speech'], score)
            if not vocabulary in result : result.append(vocabulary)
    
    result = sorted(result, key=lambda word: word[0])
    print(f"【 Words similar to '{target_word}' 】")
    for word in result: print(f"LEVEL {word[0]}  {word[1]: <15} {word[3]: <5} {word[2]: <30}\t {word[-1]:<.4f}")

inp = input("input > ")
while inp != "":
    find_resemble_word(inp)
    inp = input("input > ")