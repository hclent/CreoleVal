import sys
import csv

f = str(sys.argv[1])

num_tokens = 0

with open(f) as handle:
    tatoeba = csv.reader(handle, delimiter='\t')
    print(tatoeba)
    for row in tatoeba:
        creole = row[1]
        naive_tokens = len((creole).split(' '))
        num_tokens += naive_tokens

print(f"{f}: {num_tokens}")
