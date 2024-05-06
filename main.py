from StarDust import PatternLoader
import sys
import numpy as np
import pandas as pd 

sys.setrecursionlimit(1500)
#pattern_loader = PatternLoader("datasets/movement_libras.csv", ",", [0] * 300)
#pattern_loader = PatternLoader("datasets/micromass.csv", ";", [0] * 11000)
# pattern_loader = PatternLoader("datasets/poker-hand.csv", ",", [3] * 11)
#pattern_loader = PatternLoader("datasets/sonar.csv", ",", [0] * 60)
pattern_loader = PatternLoader("Datasets/prova.csv", ",", [1, 1, 1, 1])
# pattern_loader = PatternLoader("datasets/expIDEAS.csv", ",", [0, 1, 0, 1])
# pattern_loader = PatternLoader("datasets/tuandromd.csv", ",", [1]*300)

M, initial_partitions = pattern_loader.get_partition_local()
print(20*'-')
print(initial_partitions)



pattern_loader2 = PatternLoader("Datasets/prova2.csv", ",", [1, 1, 1, 1])
M2, initial_partitions2 = pattern_loader2.get_partition_local()
print(20*'-')
print(initial_partitions2)


print(initial_partitions2[0][14].to_numpy())

lhs_indexes=[0,1,3]
old_lhs_indexes=[0,1]
rhs_index=2


# Definisci i dati come un array bidimensionale
df = pd.read_csv("Datasets/prova_operations.csv", header=None)

# Filtra le righe con valore della prima colonna pari a zero
df_zero = df[df[0] == 0]

# Filtra le righe con valore della prima colonna maggiore di zero
df_insertions = df[df[0] > 0]

print(df_zero)

print(df_insertions)



def check_invalidation(lhs_indexes, old_lhs_indexes, rhs_index, df_zero, df_insertions):
    for idx, row in df_insertions.iterrows():
        print(row.values)

        


check_invalidation(lhs_indexes, old_lhs_indexes, rhs_index, df_zero, df_insertions)