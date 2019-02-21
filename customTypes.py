class CandidateData:
    # тип данных для кандидатов из словаря брендов и из словаря с названиямии и описаниями
    # с весами для каждого кандидата
    def __init__(self, weight, variant, ru_trans, eng_trans):
        self.weight = weight
        self.variant = variant
        self.ru_trans = ru_trans
        self.eng_trans = eng_trans
