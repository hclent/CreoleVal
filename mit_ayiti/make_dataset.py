import csv
import random
from collections import defaultdict

random.seed(12)

translation_lut = {} #dict of dicts {id: {ht: '', 'en': '', ...}}
stats_dict = defaultdict(lambda:0)

with open("cleaned.csv", encoding="utf8", newline="\n") as tsvfile:
	mit_reader = list(csv.reader(tsvfile, delimiter="|"))
	# for i, row in enumerate(mit_reader):
	# 	print(f"* {i+1}: {row}\n\n") 
	print(len(mit_reader)-1)
	k = range(10000)
	entry_ids = random.sample(k, len(mit_reader)-1) #list 
	assert len(entry_ids) == len(list(set(entry_ids)))
	# ['Document','Kreyol','French','English','Spanish']
	for i, row in enumerate(mit_reader[1:]): #skip the header
		#print(f"* {i}: {row}\n\n")
		kreyol = row[0]
		french = ("fr", row[1])
		english = ("en", row[2])
		spanish = ("es", row[3])
		entry_num = entry_ids[i]
		sub_dict = {}
		sub_dict['ht'] = kreyol
		stats_dict['ht'] += 1
		for lang_sent in [french, english, spanish]:
			lang = lang_sent[0]
			sent = lang_sent[1]
			if sent != "empty":
				sub_dict[lang] = sent
				stats_dict[lang] += 1 #count how many sentences we have for each language
		translation_lut[entry_num] = sub_dict

print(stats_dict)
#print(translation_lut)

#now we should make the split files with suffled examples!
#fr-ht.src & fr-ht.trg
#en-ht.src & en-ht.trg
#es-ht.src & es-ht.trg

verify_dict = defaultdict(lambda:0)

for lang in ["fr", "en", "es"]:
	src_file = f"{lang}-ht.src"
	trg_file = f"{lang}-ht.trg"
	#init the files 
	src_out = open(src_file, 'a')
	trg_out = open(trg_file, 'a')

	for sent_id in sorted(translation_lut):
		sent_dict = translation_lut[sent_id]
		try:
			source = sent_dict[lang]
			target = sent_dict["ht"]
			verify_dict[lang] +=1
			src_out.write(f"{sent_id}\t{source}\n")
			trg_out.write(f"{sent_id}\t{target}\n")
		except Exception as e:
			#no parallel translation for this language
			pass
	src_out.close()
	trg_out.close()

print(verify_dict)









