import re
from fuzzywuzzy import fuzz
# from jellyfish._jellyfish import damerau_levenshtein_distance as damerau_levenshtein
from pyxdameraulevenshtein import damerau_levenshtein_distance as damerau_levenshtein
from customTypes import CandidateData
from mechanics import fuzzy_substring


class Calculator:
    from mechanics import Weights

    def __init__(self, query_str, ru_en_dict):
        self.ru_en_dict = ru_en_dict
        self.query_str = query_str

        self.weight_query_trans_set = set()
        self.max_set = set()

    def calculate_weights(self):
        query_str = self.query_str
        for ru_trans in self.ru_en_dict.keys():
            eng_trans = self.ru_en_dict[ru_trans]

            # weight_plain = fuzz.ratio(query_str, ru_trans)
            # self.weight_query_trans_set.add((weight_plain, ru_trans, eng_trans))
            #
            # weight_mixed = fuzz.partial_ratio(query_str, ru_trans)
            # self.weight_query_trans_set.add((weight_mixed, ru_trans, eng_trans))


            # ищет неполный транслит с пробелами и без в неполном запросе
            trans_list = re.split('\W+', ru_trans)
            query_list = re.split('\W+', query_str)
            for k in range(len(query_list)):
                for m in range(k + 1, len(query_list) + 1):
                    query_piece = ' '.join(query_list[k:m])

                    for i in range(len(trans_list)):
                        for j in range(i + 1, len(trans_list) + 1):
                            trans_piece_withspace = ' '.join(trans_list[i:j])
                            weight = damerau_levenshtein(query_piece, trans_piece_withspace)
                            self.weight_query_trans_set.add((weight, ru_trans, eng_trans))

                            trans_piece_spaceless = ''.join(trans_list[i:j])
                            weight = damerau_levenshtein(query_piece, trans_piece_spaceless)
                            self.weight_query_trans_set.add((weight, ru_trans, eng_trans))

            # прикидывает вес, если слова перемешаны и находятся не все
            rebuild_list = []
            doubtful_word_num = 0
            for query_word in query_list:
                for trans_word in trans_list:
                    weight = damerau_levenshtein(query_word, trans_word)
                    if weight > 2:
                        doubtful_word_num += 1
                    rebuild_list.append(weight)
            rebuild_weight = min(rebuild_list) + doubtful_word_num
            self.weight_query_trans_set.add((rebuild_weight, ru_trans, eng_trans))

        # выбирает пару с наименьшим весом
        max_weight = 1000
        for candidate_tuple in self.weight_query_trans_set:
            if candidate_tuple[0] < max_weight:
                max_weight = candidate_tuple[0]

                self.max_set.add({'weight': candidate_tuple[0], 'variant': query_str,
                                  'ru_trans': candidate_tuple[1], 'eng_trans': candidate_tuple[2]})

