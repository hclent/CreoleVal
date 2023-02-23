lang = 'pap'
with open('wikiann-'+lang+'.bio', 'r', encoding='utf8') as f:
    txt = []
    for token in f:
        txt.append(token)

sents = {}
k = 1
for tok in txt:
    if tok != '\n':
        sents.setdefault(k, []).append(tok)
    elif tok == '\n':
        k += 1     

unique_sents = {}
for key, value in sents.items():
    value = '+'.join(value)
    if value not in unique_sents:
        unique_sents[value] = 1
    elif value in unique_sents:
        unique_sents[value] += 1 
        
delkeys = []
for key, value in sents.items():
    value = '+'.join(value)
    if unique_sents[value] > 1:
        delkeys.append(key)
        
for key in delkeys:
    if key in sents:
        del sents[key] 
        
duplicates = {}
n = 0
for key, value in unique_sents.items():
    if value > 1:
        key = key.split('+')
        n += 1
        duplicates[n] = key
        
nkey = 100000
for key, value in duplicates.items():
    nkey += 1
    sents[nkey] = value 

newsents = {}
ke = 0
for key, value in sents.items():
    ke +=1
    newsents[ke] = value    #sorting the keys in a new dict to split the text
    
nr = 0
lengths = {}
for key, value in newsents.items():
    nr += 1
    lengths[nr] = len(value)
    
import pandas as pd
import re
from sklearn.model_selection import train_test_split

data = {0: newsents, 1: lengths}
df = pd.DataFrame.from_dict(data, orient="columns")
df.columns = ["sentence", "length"]
df['length'] = df['length'].astype('float')

train, test = train_test_split(df, test_size=0.20)

train, val = train_test_split(train, test_size=0.125)

train['length'].mean()
val['length'].mean()
test['length'].mean()

tokenre = re.compile(r'(\S+).*\s\S+\n$')
tagre = re.compile(r'\S+.*\s(\S+\n$)') 

clean_train = []
for listt in train['sentence']:
    listt2 = []
    for tok in listt:
        line = [tokenre.findall(tok)[0], tagre.findall(tok)[0]]
        listt2.append(line)           #removing the additional tags TRAIN
    clean_train.append(listt2)

clean_dev = []
for listt in val['sentence']:
    listt2 = []
    for tok in listt:
        line = [tokenre.findall(tok)[0], tagre.findall(tok)[0]]
        listt2.append(line)             #removing the additional tags DEV
    clean_dev.append(listt2)

clean_test = []
for listt in test['sentence']:
    listt2 = []
    for tok in listt:
        line = [tokenre.findall(tok)[0], tagre.findall(tok)[0]]
        listt2.append(line)               #removing the additional tags TEST
    clean_test.append(listt2)

tab_train = []
for sent in clean_train:
    tab_sent = []
    for tok in sent:
        tok = '\t'.join(tok)
        tab_sent.append(tok)         #adding tabs between the tags and tokens
    tab_train.append(''.join(tab_sent))
    
tab_dev = []
for sent in clean_dev:
    tab_sent = []
    for tok in sent:
        tok = '\t'.join(tok)
        tab_sent.append(tok)         #adding tabs between the tags and tokens
    tab_dev.append(''.join(tab_sent))
    
tab_test = []
for sent in clean_test:
    tab_sent = []
    for tok in sent:
        tok = '\t'.join(tok)
        tab_sent.append(tok)         #adding tabs between the tags and tokens
    tab_test.append(''.join(tab_sent))

with open(lang+"-train.txt", 'w', encoding='utf8') as outFile:
    outFile.write('\n'.join(tab_train))        #voila!
    
with open(lang+"-dev.txt", 'w', encoding='utf8') as outFile:
    outFile.write('\n'.join(tab_dev))        
    
with open(lang+"-test.txt", 'w', encoding='utf8') as outFile:
    outFile.write('\n'.join(tab_test))        


