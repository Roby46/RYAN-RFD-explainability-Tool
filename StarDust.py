import pandas as pd
import Levenshtein
import numpy as np

def equal_function(x, y, t):
    return x == y

def string_distance(x, y, t):
    return Levenshtein.distance(x, y, score_cutoff=t) <= t


def numeric_abs_function(x, y, t):
    return round(abs(np.float64(x) - np.float64(y)), 10) <= t


class PatternLoader:
    def __init__(self, dataset, separator, thresholds, df,process=1):
        self.columns_number = None
        self.dataset = dataset
        self.df = df
        self.thresholds = thresholds
        self.separator = separator
        self.process = process

    def get_distance_function(self, dtype, thr):
        if thr == 0: return equal_function
        if dtype == "float64" or dtype == "int64":
            return numeric_abs_function
        elif dtype == "object":
            return string_distance
        else:
            return None

    def get_partition(self, df=None, remove_singleton=True):
        if df is None:
            df = self.df

        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        self.row_number = len(df)
        self.columns_number = len(df.columns)
        initial_partitions = [df.groupby(c, sort=False).groups for c in df.columns]
        M = {}
        for c, column_partition in enumerate(initial_partitions):
            keys = list(column_partition.keys())
            keys.sort()
            element_similarity = {}
            for k in keys:
                element_similarity[k] = set()
            thr = self.thresholds[c]
            check_similarity = self.get_distance_function(df[c].dtype, thr)
            for i, current_element in enumerate(keys):
                element_similarity[current_element].update(column_partition[current_element])

                for j in range(i + 1, len(keys)):
                    if check_similarity(current_element, keys[j], thr):
                        element_similarity[current_element].update(column_partition[keys[j]])
                        element_similarity[keys[j]].update(column_partition[current_element])
                    else:
                        break
            M[c] = element_similarity
        if not remove_singleton:
            return M, initial_partitions
        to_remove = []
        for col in M:
            for part in M[col]:
                partition = M[col][part]
                if len(partition) <= 1:
                    to_remove.append((col, part))
        for t in to_remove:
            M[t[0]].pop(t[1])
        return M, initial_partitions

    def get_partition_local(self):
        M, initial_partitions = self.get_partition()
        return M, initial_partitions
