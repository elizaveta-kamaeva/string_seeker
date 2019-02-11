class CandidateData:
    # тип данных для кандидатов из словаря брендов и из словаря с названиямии и описаниями
    # с весами для каждого кандидата
    def __init__(self, hash_weight, hash_source, hash_trans, hash_eng):
        self.hash_weight = hash_weight
        self.hash_source = hash_source
        self.hash_trans = hash_trans
        self.hash_eng = hash_eng
