from collections import Counter


class Loader:
    def __init__(self, fixed_str, ruenbrand_dict, ruenother_dict):
        self.fixed_str = fixed_str
        self.ruenbrand_dict = ruenbrand_dict
        self.ruenother_dict = ruenother_dict


class Weights:
    def __init__(self, func, loader_obj):
        self.function = func
        self.fixed_str = loader_obj.fixed_str
        self.ru_en_brands = loader_obj.ruenbrand_dict
        self.ru_en_other = loader_obj.ruenother_dict

        self.hash_source = {}
        self.hash_weight = {}
        self.hash_trans = {}
        self.hash_eng = {}

    def calculate_weights(self, ru_en_dict, dict_type='Undefined'):
        # считает веса, используя поданную на вход функцию
        diff_dict = Counter()
        for ru_trans in ru_en_dict.keys():
            fuzz_measure = self.function(self.fixed_str, ru_trans)
            diff_dict[ru_trans] = fuzz_measure
        top_results = diff_dict.most_common(3)
        for pair in top_results:
            ru_trans, weight = pair
            hash_num = hash(pair)
            if hash_num not in self.hash_source:
                self.hash_weight[hash_num] = weight
                self.hash_source[hash_num] = dict_type
                self.hash_trans[hash_num] = ru_trans
                self.hash_eng[hash_num] = ru_en_dict[ru_trans]

    def candidates_with(self):
        # ищет кандидатов, используя поданную на вход функцию
        self.calculate_weights(self.ru_en_brands, dict_type='brand')
        self.calculate_weights(self.ru_en_other, dict_type='other')
        a = 1
