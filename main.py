from StarDust import PatternLoader
import sys

sys.setrecursionlimit(1500)
#pattern_loader = PatternLoader("datasets/movement_libras.csv", ",", [0] * 300)
#pattern_loader = PatternLoader("datasets/micromass.csv", ";", [0] * 11000)
# pattern_loader = PatternLoader("datasets/poker-hand.csv", ",", [3] * 11)
#pattern_loader = PatternLoader("datasets/sonar.csv", ",", [0] * 60)
pattern_loader = PatternLoader("Datasets/iris_little.csv", ",", [0.1, 0.1, 0.1, 0.1, 0.1])
# pattern_loader = PatternLoader("datasets/expIDEAS.csv", ",", [0, 1, 0, 1])
# pattern_loader = PatternLoader("datasets/tuandromd.csv", ",", [1]*300)

M, initial_partitions = pattern_loader.get_partition_local()
print(M)
print(20*'-')
print(initial_partitions)
