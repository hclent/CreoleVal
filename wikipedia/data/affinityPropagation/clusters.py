import os
import csv
import math
import argparse
import numpy as np
from collections import defaultdict

#TODO: for file with the csv file prefix language, not the exact csv file.
# Sort them
# Load them in order

#TODO: printint out the clusters, to review by hand. 
# Get the sentences by cluster (i.e. label)
#then sort by aff_lcs within clusters
#finally, clustesr sort by score (higher = better)

def main(args):
	cluster2textLUT = defaultdict(list) #list of dicts {cluster: [{}, {}, {}, ...]}
	score2labelLUT = dict()

	with open(os.path.join('results', args.csvfile), encoding="utf8", newline="\n") as tsvfile:
		cluster_reader = list(csv.reader(tsvfile, delimiter=","))
		# no_name , text, 	text_preprocessed, 	LEN, 	label, 	score, 	aff_lcs, 	aff_lcs_label
		for i, row in enumerate(cluster_reader[1:]): #skip the header
			blank = row[0]
			text = row[1]
			text_processed = row[2]
			length = row[3] #length of tokens of preprocessed text
			cluster = row[4]
			score = row[5]
			sub_cluster = row[6] #aff_lcs
			af_lcs_label = row[7] #this just {cluster}_{sub_cluster}

			sub_dict = {'sub_cluster': sub_cluster,'text': text, 'length': length}
			cluster2textLUT[int(cluster)].append(sub_dict)
			score2labelLUT[score] = cluster

	#TODO: sort the dict by cluster
	# sort each cluster by sub-cluster
	for score in sorted(score2labelLUT.keys(), reverse=True): #highest score to lowest, henny~
		cluster = score2labelLUT[score]
		print(f"======================== {cluster} (score: {score}) ========================")
		sents_dicts = cluster2textLUT[int(cluster)]
		sub_clusters = sorted(list(set([lil_d['sub_cluster'] for lil_d in sents_dicts])))
		#This is totally inefficient~~~~ 
		for sub in sub_clusters:
			print(f"------ {sub} ------")
			for lil_d in sents_dicts:
				if lil_d['sub_cluster'] == sub:
					print(lil_d['text'])


	# length2clustersLUT = defaultdict(list)
	# for c, sent_list in cluster2textLUT.items():
	# 	#print(f"****************{c}****************")
	# 	#print(f'{[s for s in sent_list]}')
	# 	length2clustersLUT[len(sent_list)].append(c)

	# print("============"*20)
	# print("***** Overview *****")
	# print(f"*** Num clusters: {len(cluster2textLUT.keys())}")
	# s = sorted(list(length2clustersLUT.keys()))
	# largest = s[-1]
	# smallest = s[0]
	# average = np.around(np.mean(s), 0)
	# median = np.around(np.median(s), 0)
	# print(f"*** Largest cluster: {largest} (i.e. {length2clustersLUT[largest]})")
	# print(f"*** Average cluster: {average} (i.e. {length2clustersLUT[average]})")
	# print(f"*** Median cluster: {median} (i.e. {length2clustersLUT[median]})")
	# print(f"*** Smallest cluster: {smallest} (i.e. {length2clustersLUT[smallest]})")
	# print("============"*20)
	
	# Print examples of these
	# text_val = [("Largest", largest), ("Average", average), ("Median", median), ("Smallest", smallest)]
	# for pair in text_val:
	# 	label = pair[0]
	# 	value = pair[1]
	# 	if label != "Largest":
	# 		print(f" --- Example {label} Clusters --- ")
	# 		for c in length2clustersLUT[value]:
	# 			print(f"#### Cluster {c}")
	# 			for line in cluster2textLUT[c]:
	# 				print(f"{line}")
	# 		print(f"------------")
	# 	else:
	# 		print(f" --- Example {label} Clusters --- ") #Largest cluster, just look at the first example
	# 		for line in cluster2textLUT[length2clustersLUT[pair[1]][0]]:
	# 			print(f"* {line}")
	# 		print(f"------------")


parser = argparse.ArgumentParser(description='Select a csv file.')
parser.add_argument('csvfile', metavar='F', type=str)
args = parser.parse_args()
main(args)

