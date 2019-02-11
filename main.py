from time import time
import pandas as pd
from measure import Measure


def get_query(filename):
    filepath = 'infiles\\' + filename
    df = pd.read_csv(filepath, sep='\t', dtype=str, error_bad_lines=False)
    df = df.fillna(0).astype({'count': int})
    str_dict = df.set_index('fixed_searchstring')['searchstring'].to_dict()
    str_count_dict = df.set_index('fixed_searchstring')['count'].to_dict()

    print('{} queries from {} found.'.format(len(str_dict),filename))
    return str_dict, str_count_dict


def get_translit(filename):
    filepath = 'infiles\\' + filename
    df = pd.read_csv(filepath, sep=';', dtype=str, error_bad_lines=False)
    ru_en_dict = df.set_index('alias')['brand'].to_dict()

    print('{} translit from {} loaded.'.format(len(ru_en_dict), filename))
    return ru_en_dict


filename = '256-fixed-sampled-total.csv'
outname = 'outfiles\\' + filename.split('-')[0] + '-trans-analysis.csv'
fix_init_dict, fix_count_dict = get_query(filename)
ru_en_brands = get_translit('256-brands-full.csv')
# ru_en_brands = {}
ru_en_unknownbrands_dict = get_translit('256-translit.csv')
outfile = open(outname, 'w', encoding='utf-8')

common_metrics_obj = Measure(fix_init_dict, ru_en_brands, ru_en_unknownbrands_dict)
t = time()
Measure.cycle(common_metrics_obj)

outfile.write('{}\t{}\t{}\t{}\t{}\n'.format('probability', 'fixed_query', 'eng_words', 'generated_translit', 'source'))
for quadrum in common_metrics_obj.max_list:
    outfile.write('\t'.join([str(elt) for elt in quadrum]) + '\n')
outfile.close()

print('Process took {} seconds.'.format(round(time() - t, 2)))
