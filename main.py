import re
from time import time
import pandas as pd
from scales import Scales


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
    df['alias'] = df['alias'].replace('[\W_]+', ' ')
    ru_en_dict = df.set_index('alias')['brand'].to_dict()

    print('{} translit from {} loaded.'.format(len(ru_en_dict), filename))
    return ru_en_dict


def get_feed(filename):
    filepath = 'infiles\\' + filename
    text_list = open(filepath, 'r', encoding='utf-8').readlines()
    text = ''
    for line in text_list:
        text += re.sub('<.+?>', ' ', line, flags=re.DOTALL) + '\n'
    text = re.sub('ё', 'е', text)
    feed_set = set()
    for item in re.split('[\W_]+', text):
        if item and \
                not (re.match('full_', item) or
                     re.fullmatch('\d+', item)):
            feed_set.add(item.lower())

    print('{} unique feed words from {} found.'.format(len(feed_set), filename))
    return feed_set


filename = '334-fixed.csv'
feedfile = 'yandex_469070.php.xml'
transfile_other = '334-translit.csv'
transfile_full = '334-full.csv'
outname = 'outfiles\\' + filename.split('-')[0] + '-trans-analysis.csv'

fix_init_dict, fix_count_dict = get_query(filename)
feed = get_feed(feedfile)
ru_en_dict_other = get_translit(transfile_other)
ru_en_dict_full = get_translit(transfile_full)
ru_en_dict = {**ru_en_dict_other, **ru_en_dict_full}

common_metrics_obj = Scales(fix_init_dict, ru_en_dict, feed)
t = time()
Scales.collect_matches(common_metrics_obj)

outfile = open(outname, 'w', encoding='utf-8')
outfile.write('{}\t{}\t{}\t{}\t{}\n'.format('weight', 'variant', 'ru_trans', 'eng_trans', 'init_query'))
for candidate_tuple in common_metrics_obj.max_list:
    outfile.write('\t'.join([str(elt) for elt in candidate_tuple]) + '\n')
outfile.close()

seconds = round(time() - t)
print('Process took {0} minute{2} {1} seconds.'.format(seconds // 60,
                                                       seconds % 60,
                                                       '' if seconds // 60 == 1 else 's'))
