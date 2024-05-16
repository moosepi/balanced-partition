import itertools
import functools
import heapq
import math
import time

@functools.total_ordering
class Partition:
    def __init__(self, subset_list):
        self.subsets = sorted([(sum(item[1] for item in subset), subset) for subset in subset_list], reverse=True)
        self.max_diff = self.subsets[0][0] - self.subsets[-1][0]
        self.cardinalities = [len(subset[1]) for subset in self.subsets]
        self.max_card_diff = max(self.cardinalities) - min(self.cardinalities)
        
    def __eq__(self, other):
        return self.max_diff == other.max_diff
        
    def __lt__(self, other):
        # greater since python does min heap by default
        return self.max_diff > other.max_diff

    def __repr__(self):
        return str(self.subsets)
        
    def __str__(self):
        to_ret = ''
        for subset in self.subsets:
            items = sorted(subset[1], key=lambda x: x[1], reverse=True)
            for item in items:
                to_ret += f'{item[0]} ({str(item[1])}) '
            to_ret += f'= {str(subset[0])}\n'
        return to_ret
        
def combine_partitions(partition_l, partition_r, permutation):
    subsets_l = [subset[1] for subset in partition_l.subsets]
    subsets_r = [subset[1] for subset in partition_r.subsets]
    
    combined_subsets = [subsets_l[i] + subsets_r[permutation[i]] for i in range(len(permutation))]
    
    return Partition(combined_subsets)
        
def balanced_partition_rec(partition_list, best_diff, bin_count, end_time):
    '''
    recursive dfs of the subset-combining tree
    '''
    if time.time() > end_time:
        return []
    
    if len(partition_list) < 1:
        raise ValueError('need partitions to combine')
    if len(partition_list) == 1:
        if partition_list[0].max_diff > best_diff or partition_list[0].max_card_diff > 0:
            return []
        else:
            return [partition_list[0]]
        
    solution_list = []
    partition_l = heapq.heappop(partition_list)
    partition_r = heapq.heappop(partition_list)
    for perm in itertools.permutations(range(bin_count - 1, -1, -1)):
        if time.time() > end_time:
            return solution_list
        new_partition_list = partition_list.copy()
        new_partition = combine_partitions(partition_l, partition_r, perm)
        heapq.heappush(new_partition_list, new_partition)
        greatest_max_diff = 0
        greatest_card_diff = 0
        max_diff_sum = 0
        card_diff_sum = 0
        for partition in new_partition_list:
            if partition.max_diff > greatest_max_diff:
                max_diff_sum += greatest_max_diff
                greatest_max_diff = partition.max_diff
            else:
                max_diff_sum += partition.max_diff
            if partition.max_card_diff > greatest_card_diff:
                card_diff_sum += greatest_card_diff
                greatest_card_diff = partition.max_card_diff
            else:
                card_diff_sum += partition.max_card_diff
        
        if greatest_max_diff - max_diff_sum > best_diff or greatest_card_diff > card_diff_sum:
            continue
        
        new_sols = balanced_partition_rec(new_partition_list, best_diff, bin_count, end_time)
        if len(new_sols) > 0:
            new_best_diff = new_sols[0].max_diff 
            if new_best_diff < best_diff:
                solution_list = new_sols
                best_diff = new_best_diff
            elif new_best_diff == best_diff: 
                solution_list += new_sols
        
    return solution_list

def balanced_partition(value_list, partition_size, timelimit=math.inf):
    '''
    takes as input:
        a list of either:
            - numbers (int/float)
            - tuples (name, value) where name is a str 
        desired partition size (int)
        timelimit in seconds (int/float)
        
    outputs:
        list of balanced partitions, as optimal as possible
    '''
    if all(type(value) is int for value in value_list):
        value_list = [(str(value), value) for value in value_list]
    if len(value_list) % partition_size != 0:
        raise ValueError('cannot divide evenly')
    partition_count = int(len(value_list) / partition_size)
    value_list.sort(key=lambda x: x[1], reverse=True)
    initial_partition_list = []
    for val in value_list:
        initial_partition_list.append(Partition([[val]] + [[]] * (partition_count - 1)))
        
    return balanced_partition_rec(initial_partition_list, math.inf, partition_count, time.time() + timelimit)
