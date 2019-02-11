from fuzzywuzzy import fuzz
from customTypes import CandidateData


class Compare:
    from mechanics import Weights

    def __init__(self, loader_obj):
        self.ruenbrand_dict = loader_obj.ruenbrand_dict
        self.ruenother_dict = loader_obj.ruenother_dict
        self.fixed_str = loader_obj.fixed_str
        self.loader_obj = loader_obj

        self.not_found_list = []
        self.correct_list = []
        self.withtypos = CandidateData
        self.mixed_skipped = CandidateData

    def not_found(self):
        # проверяет, является ли строка точной копией транслита,
        # который почему-то не был обнаружен автоматически
        for ru_trans in self.ruenbrand_dict.keys():
            if self.fixed_str in ru_trans:
                self.not_found_list.extend((self.fixed_str, self.ruenbrand_dict[ru_trans]))

    def correct(self):
        # ищет точные соответствия транслитов
        for en_trans in set(self.ruenbrand_dict.values()):
            if en_trans == self.fixed_str:
                self.correct_list.extend((self.fixed_str, en_trans))

    def with_typos(self):
        # ищет строку с транслитом, который написан с ошибками
        weight_obj = self.Weights(fuzz.ratio, self.loader_obj)
        self.Weights.candidates_with(weight_obj)
        self.withtypos.hash_source = weight_obj.hash_source
        self.withtypos.hash_weight = weight_obj.hash_weight
        self.withtypos.hash_trans = weight_obj.hash_trans
        self.withtypos.hash_eng = weight_obj.hash_eng

    def mixed_skipped(self):
        # перемешанные и неполные строки
        weight_obj = self.Weights(fuzz.token_set_ratio, self.loader_obj)
        self.Weights.candidates_with(weight_obj)
        self.mixed_skipped.hash_source = weight_obj.hash_source
        self.mixed_skipped.hash_weight = weight_obj.hash_weight
        self.mixed_skipped.hash_trans = weight_obj.hash_trans
        self.mixed_skipped.hash_eng = weight_obj.hash_eng
