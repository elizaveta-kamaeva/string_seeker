from mechanics import Loader
from comparer import Compare


class Measure:
    def __init__(self, fixinit_dict, ruen_brands, ruen_other):
        self.fix_init_dict = fixinit_dict
        self.ru_en_brands = ruen_brands
        self.ru_en_other = ruen_other

        self.not_found = []
        self.correct = []
        self.max_list = []

    def cycle(self):
        n = 0
        for fixed_string in self.fix_init_dict.keys():
            if not fixed_string:
                continue

            hash_weight_total = {}
            hash_source_total = {}
            hash_trans_total = {}
            hash_eng_total = {}

            load_obj = Loader(fixed_string, self.ru_en_brands, self.ru_en_other)
            compare_obj = Compare(load_obj)

            Compare.not_found(compare_obj)
            self.not_found = compare_obj.not_found_list

            Compare.correct(compare_obj)
            self.correct = compare_obj.correct_list

            Compare.with_typos(compare_obj)
            hash_weight_total.update(compare_obj.withtypos.hash_weight)
            hash_source_total.update(compare_obj.withtypos.hash_source)
            hash_trans_total.update(compare_obj.withtypos.hash_trans)
            hash_eng_total.update(compare_obj.withtypos.hash_eng)

            Compare.mixed_skipped(compare_obj)
            hash_weight_total.update(compare_obj.mixed_skipped.hash_weight)
            hash_source_total.update(compare_obj.mixed_skipped.hash_source)
            hash_trans_total.update(compare_obj.mixed_skipped.hash_trans)
            hash_eng_total.update(compare_obj.mixed_skipped.hash_eng)

            max_probable = {}
            for hash_key in hash_weight_total.keys():
                weight = hash_weight_total[hash_key]
                if len(max_probable.values()) == 0:
                    max_probable[hash_key] = weight
                elif weight > max(max_probable.values()):
                    max_probable = {}
                    max_probable[hash_key] = weight
                elif weight == max(max_probable.values()):
                    max_probable[hash_key] = weight

            known_trans = set()
            for hash_key in max_probable:
                max_weight = max_probable[hash_key]
                max_source = hash_source_total[hash_key]
                max_trans = hash_trans_total[hash_key]
                max_eng = hash_eng_total[hash_key]
                if max_trans not in known_trans:
                    self.max_list.append((max_weight, fixed_string, max_eng, max_trans, max_source))
                    known_trans.add(max_trans)

            n += 1
            if n % 10 == 0:
                print(n, 'lines processed')

        print('Not found:', self.not_found)
        print('Correct:', self.correct)
