from preparator import preprocess_query
from calculator import Calculator


class Scales:
    def __init__(self, fixinit_dict, ru_en_dict, feed_set):
        self.fix_init_dict = fixinit_dict
        self.ru_en_brands = ru_en_dict
        self.feed_set = feed_set

        self.max_list = []

    def collect_matches(self):
        n = 0
        known = set()

        for init_str in self.fix_init_dict.keys():
            query_str = preprocess_query(init_str, self.feed_set, known)
            if query_str:
                calculate_obj = Calculator(query_str, self.ru_en_brands)
                Calculator.calculate_weights(calculate_obj)

                candidate_set = calculate_obj.max_set
                for candidate_dict in candidate_set:
                    weight = candidate_dict['weight']
                    if weight < 100:
                        self.max_list.append((weight,
                                             candidate_dict['variant'],
                                             candidate_dict['ru_trans'],
                                             candidate_dict['eng_trans'],
                                             init_str))
                        known.add(candidate_dict['variant'])

            n += 1
            if n % 10 == 0:
                print(n, 'lines processed')

            if n % 100 == 0:
                outname = 'outfiles\\' + '334_analysis-' + str(n) + 'queries.csv'
                outfile = open(outname, 'w', encoding='utf-8')
                outfile.write('{}\t{}\t{}\t{}\t{}\n'.format('weight', 'variant', 'ru_trans', 'eng_trans', 'init_query'))
                for candidate_dict in self.max_list:
                    outfile.write('\t'.join([str(elt) for elt in candidate_dict]) + '\n')
                print(n, 'LINES WRITTEN')
                outfile.close()
