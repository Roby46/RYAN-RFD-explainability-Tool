# Definisci i due oggetti
M = {0: {14: {0, 1, 4}, 15: {0, 1, 2, 4}, 16: {1, 2, 4}}, 
        1: {19: {2, 4}, 20: {2, 4}, 45: {0, 1}, 46: {0, 1}}, 
        2: {1: {0, 1}, 2: {0, 1}, 10: {2, 4}, 11: {2, 4}}, 
        3: {29: {2, 4}, 30: {2, 4}, 50: {0, 1}, 51: {0, 1}}}

M2 = {0: {14: {0, 1, 4, 5}, 15: {0, 1, 2, 4, 5}, 16: {1, 2, 4}, 18:{1, 2, 4}}, 
        1: {19: {2, 4}, 20: {2, 4}, 45: {0, 1, 5}, 46: {0, 1, 5}}, 
        2: {1: {0, 1}, 2: {0, 1}, 10: {2, 4}, 11: {2, 4}}, 
        3: {29: {2, 4}, 30: {2, 4}, 50: {0, 1}, 51: {0, 1}}}


#from StarDust import PatternLoader
#import sys
#import numpy as np
#import pandas as pd
#
#
#sys.setrecursionlimit(1500)
#pattern_loader = PatternLoader("Datasets/prova.csv", ",", [1, 1, 1, 1])
#M, initial_partitions = pattern_loader.get_partition_local()
#
#pattern_loader2 = PatternLoader("Datasets/prova2.csv", ",", [1, 1, 1, 1])
#M2, initial_partitions2 = pattern_loader2.get_partition_local()
#
#print(M, M2)


# Funzione per calcolare la differenza
def compute_difference(obj1, obj2):
    diff_obj = {}
    for attribute in obj1:
        #print(attribute)
        diff_obj[attribute] = {}
        for pattern_value in obj2[attribute]:
            #print(pattern_value)
            if pattern_value in obj1.get(attribute, {}):
                diff_obj[attribute][pattern_value] = obj2[attribute][pattern_value] - obj1[attribute][pattern_value]
            else:
                diff_obj[attribute][pattern_value] = obj2[attribute][pattern_value]  # Aggiungi il valore dall'oggetto 2
    return diff_obj

# Calcola la differenza
difference = compute_difference(M, M2)

# Stampare la differenza
print(difference)