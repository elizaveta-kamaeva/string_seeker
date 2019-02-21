import re


def preprocess_query(fixed_string, feed_set, known):
    # выкидывает английские слова, слова из фида и слова без букв
    list2watch = []
    for word in fixed_string.lower().split():
        word = re.sub('[a-z]+', '', word, flags=re.IGNORECASE).strip()
        word = re.sub('ё', 'е', word)
        if word not in known:
            if word and not (re.fullmatch('[^а-я]+', word, flags=re.IGNORECASE)):
                if word not in feed_set:
                        list2watch.append(word)
    if list2watch:
        query_str = ' '.join(list2watch)
        return query_str
    else:
        return None
