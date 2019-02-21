from collections import Counter

def fuzzy_substring(needle, haystack):
    """Calculates the fuzzy match of needle in haystack,
    using a modified version of the Levenshtein distance
    algorithm.
    The function is modified from the levenshtein function
    in the bktree module by Adam Hupp"""
    m, n = len(needle), len(haystack)

    # base cases
    if m == 1:
        return not needle in haystack
    if not n:
        return m

    row1 = [0] * (n+1)
    for i in range(0,m):
        row2 = [i+1]
        for j in range(0,n):
            cost = ( needle[i] != haystack[j] )

            row2.append( min(row1[j+1]+1, # deletion
                               row2[j]+1, #insertion
                               row1[j]+cost) #substitution
                           )
        row1 = row2
    return min(row1)


class Loader:
    def __init__(self, fixed_str, ru_en_dict):
        self.fixed_str = fixed_str
        self.ru_en_dict = ru_en_dict


class Weights:
    def __init__(self, func, loader_obj):
        self.function = func
        self.fixed_str = loader_obj.fixed_str
        self.ru_en_dict = loader_obj.ru_en_dict

        self.hash_weight = {}
        self.hash_trans = {}
        self.hash_eng = {}

    def calculate_weights(self, ru_en_dict):
        # считает веса, используя поданную на вход функцию
        diff_dict = Counter()
        for ru_trans in ru_en_dict.keys():
            fuzz_measure = self.function(self.fixed_str, ru_trans)
            diff_dict[ru_trans] = fuzz_measure
        top_results = diff_dict.most_common(3)
        for pair in top_results:
            ru_trans, weight = pair
            hash_num = hash(pair)

            self.hash_weight[hash_num] = weight
            self.hash_trans[hash_num] = ru_trans
            self.hash_eng[hash_num] = ru_en_dict[ru_trans]

    def candidates_with(self):
        # ищет кандидатов, используя поданную на вход функцию
        self.calculate_weights(self.ru_en_dict)
