# your code here, including all the helpful print statements
from itertools import chain, combinations
from collections import defaultdict


# Grouping all the data by userId



# Apriori Algorithm function
def apriori(movie_list,af, sample_factor, minsup, minconf):
    item_set = set()
    for movie in movie_list:
        for i in movie:
            item_set.add(frozenset([i]))

    print("Total number of items in singleton candidate set : ", len(item_set))

    def prune(nextCandidateSet, currentFreqSet, length):
        temp = nextCandidateSet.copy()
        for i in nextCandidateSet:
            subsets = combinations(i, length)
            for s in subsets:
                if (frozenset(s) not in currentFreqSet):
                    temp.remove(i)
                    break
        return temp
    sup_map = defaultdict(int)
    item_count = defaultdict(int)
    for item in item_set:
        for item_set in movie_list:
            if item.issubset(item_set):
                sup_map[item] += 1
                item_count[item] += 1
    freq = set()
    for item, count in item_count.items():
        c = count
        if (c >= minsup * sample_factor * af):
            freq.add(item)

    curr_freq = freq
    apriori_frequency = list(curr_freq)

    iter = 2
    final_set = dict()
    # To Calculate frequent item sets
    while (curr_freq):
        x = len(curr_freq)
        print("\n" + str(iter - 1) + " sized Itemsets with support greater than " + str(
            minsup * af * sample_factor) + " are " + str(x) + "\n")
        final_set[iter - 1] = curr_freq
        # Adding the current itemset to frequent itemset
        nextCandidateSet = set([i.union(j) for i in curr_freq for j in curr_freq if len(i.union(j)) == iter])
        nextCandidateSet = prune(nextCandidateSet, curr_freq, iter - 1)
        # Swapping current itemet with new one
        curr_sup_map = sup_map

        curr_item_count = defaultdict(int)
        for item in nextCandidateSet:
            for nextCandidateSet in movie_list:
                if item.issubset(nextCandidateSet):
                    curr_sup_map[item] += 1
                    curr_item_count[item] += 1
        curr_freq_temp = set()
        for item, count in curr_item_count.items():
            c = count
            if (c >= minsup * sample_factor * af):
                curr_freq_temp.add(item)
        apriori_frequency += list(curr_freq_temp)
        iter += 1

    association_rules = []
    for _, item in final_set.items():
        for val in item:
            item_subsets = chain.from_iterable(combinations(val, i) for i in range(1, len(val)))
            for sub in item_subsets:
                conf_calc = float(sup_map[val] / sup_map[frozenset(sub)])
                if (conf_calc >= minconf):
                    association_rules.append([list(sub), list(val.difference(sub))])

    print(final_set)
    final_list = []
    for val in final_set.values():
        final_list += list(val)
    print("Size of Fnal frequence item set : ", len(final_list))
    return (association_rules, final_list)

sample_ratings = allRatings.sample(frac = 1)
sr_grpby_uid = sample_ratings.groupby('userId')
uids = sr_grpby_uid.groups.keys()
movies = []
for i in uids:
    movies.append((sr_grpby_uid.get_group(i).movieId.values))
movies_data_frame = pd.DataFrame({'userId': uids, 'movieId': movies})

result = aprioriAlgorithm(movies, 1,1, 150, 0.8)
apriori_rules = result[0]
apriori_frequency = result[1]

print("After Executing Apriori Algorithm on given data : ")
print("Total Number of Rules are : ", len(apriori_rules), "They are....")
print(apriori_rules)
