import sys
import csv

f = str(sys.argv[1])

num_tokens = 0

with open(f) as handle:
    tatoeba = csv.reader(handle, delimiter=',')
    print(tatoeba)
    for row in tatoeba:
        creole = row[0]
        #print(creole)
        naive_tokens = len((creole).split(' '))
        #print(naive_tokens)
        num_tokens += naive_tokens
        #print(num_tokens)
print(f"{f}: {num_tokens}")
