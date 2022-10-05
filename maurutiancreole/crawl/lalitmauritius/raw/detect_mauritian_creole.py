import os
files=os.listdir(".")
from langdetect import detect_langs, detect
ctr=0
for i in files:
	a=" ".join(open(i).readlines()).replace("\n", " ")
	if detect(a[50:]) != "en" and detect(a[50:]) != "fr":
		ctr+=1
		print(detect_langs(a[50:]),"\t", a)
		