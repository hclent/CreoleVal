import csv
import math
import argparse
import numpy as np
from collections import defaultdict


def main(args):
	cluster2textLUT = defaultdict(list)

	with open(args.csvfile, encoding="utf8", newline="\n") as tsvfile:
		cluster_reader = list(csv.reader(tsvfile, delimiter=","))
		# text,text_preprocessed,LEN,label
		for i, row in enumerate(cluster_reader[1:]): #skip the header
			text = row[0]
			text_preprocessed = row[1]
			length = row[2]
			cluster = row[3]

			cluster2textLUT[int(cluster)].append(text)

	length2clustersLUT = defaultdict(list)
	for c, sent_list in cluster2textLUT.items():
		#print(f"****************{c}****************")
		#print(f'{[s for s in sent_list]}')
		length2clustersLUT[len(sent_list)].append(c)

	print("============"*20)
	print("***** Overview *****")
	print(f"*** Num clusters: {len(cluster2textLUT.keys())}")
	s = sorted(list(length2clustersLUT.keys()))
	largest = s[-1]
	smallest = s[0]
	average = np.around(np.mean(s), 0)
	median = np.around(np.median(s), 0)
	print(f"*** Largest cluster: {largest} (i.e. {length2clustersLUT[largest]})")
	print(f"*** Average cluster: {average} (i.e. {length2clustersLUT[average]})")
	print(f"*** Median cluster: {median} (i.e. {length2clustersLUT[median]})")
	print(f"*** Smallest cluster: {smallest} (i.e. {length2clustersLUT[smallest]})")
	print("============"*20)
	
	# Print examples of these
	text_val = [("Largest", largest), ("Average", average), ("Median", median), ("Smallest", smallest)]
	for pair in text_val:
		label = pair[0]
		value = pair[1]
		if label != "Largest":
			print(f" --- Example {label} Clusters --- ")
			for c in length2clustersLUT[value]:
				print(f"#### Cluster {c}")
				for line in cluster2textLUT[c]:
					print(f"{line}")
			print(f"------------")
		else:
			print(f" --- Example {label} Clusters --- ") #Largest cluster, just look at the first example
			for line in cluster2textLUT[length2clustersLUT[pair[1]][0]]:
				print(f"* {line}")
			print(f"------------")


parser = argparse.ArgumentParser(description='Select a csv file.')
parser.add_argument('csvfile', metavar='F', type=str)
args = parser.parse_args()
main(args)

