from nltk import (
    word_tokenize,
    FreqDist,
)

from text_project import (
    settings,
)


def find_all_words(url):
    """
    Находит все слова в документе
    """
    # # при установке nltk может быть не загружен punkt
    # download('punkt')

    data = open(f'{settings.MEDIA_ROOT}/{url}', 'r').read()
    freq_dist = FreqDist(word.lower() for word in word_tokenize(data) if word.isalpha())

    return freq_dist


def find_word_in_document(url, words, match_dict={}):
    """
    Находит наличие слов в документе
    """
    with open(f'{settings.MEDIA_ROOT}/{url}', 'r') as data:
        text = data.read().lower()

        # метод concordance_list возвращает много лишнего,
        # поэтому его не используем
        # text = nltk.Text(nltk.word_tokenize(text))
        # match = text.concordance_list('заяц')
        for word in words.keys():
            if word in text:
                # для расчета IDF нам нужно знать, есть ли слово в документе, или нет
                if match_dict.get(f'{word}'):
                    match_dict[f'{word}'].append(1)
                else:
                    match_dict[f'{word}'] = [1]

        return match_dict
