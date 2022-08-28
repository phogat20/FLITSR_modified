import copy

from weffort import getTie

def precision(n, faults, ranking, groups, perc=False, worst_effort=False, collapse=False):
    fault_num,total = method(n,perc, faults, ranking, groups, worst_effort, collapse)
    return fault_num/total

def recall(n, faults, ranking, groups, perc=False, worst_effort=False, collapse=False):
    fault_num,total = method(n,perc, faults, ranking, groups, worst_effort, collapse)
    return fault_num/len(faults)

def method(n, perc, faults, ranking, groups, worst_effort, collapse):
    size = 0
    if (collapse):
        size = len(groups)
    else:
        for group in groups:
            size += len(group)
    if (n == "b"):
        n = -1
    elif (n == "f"):
        n = len(faults)
    elif (perc):
        n = n * size
    faults = copy.deepcopy(faults) # needed to remove groups of fault locations
    i = 0
    total = 0
    fault_num = 0
    while (i < len(ranking) and total < n):
        uuts,group_len,curr_faults,curr_fault_groups,i = getTie(i, faults,
                ranking, groups, worst_effort)
        if (collapse):
            add = 0
            if (total+group_len > n and curr_fault_groups > 0):
                x = n - total
                for i in range(curr_fault_groups):
                    expected_value = (i+1)*(group_len+1)/(curr_fault_groups+1)
                    if (expected_value <= x):
                        add += 1
            else:
                add = curr_fault_groups
            total += group_len
            fault_num += add
        else:
            add = 0
            if (total+len(uuts) > n and curr_faults > 0):
                x = n - total
                for i in range(curr_faults):
                    expected_value = (i+1)*(len(uuts)+1)/(curr_faults+1)
                    if (expected_value <= x):
                        add += 1
            else:
                add = curr_faults
            total += len(uuts)
            fault_num += add
    return fault_num,total
