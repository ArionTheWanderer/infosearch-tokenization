import os
import re
import pymorphy2
import nltk
from nltk.corpus import stopwords
from string import punctuation


def tokenize_file(path):
    russian_stopwords = stopwords.words("russian")

    with open(path, encoding='cp1251', mode='r') as f:
        text = f.read()

    file_tokens = nltk.word_tokenize(text.lower())
    file_tokens = [file_token for file_token in file_tokens
                   if file_token not in russian_stopwords and file_token not in punctuation]
    return file_tokens


if __name__ == '__main__':
    nltk.download('popular')
    directory = 'pages'
    # только слова, удовлетворяющие этому паттерну попадут в список токенов
    token_pattern = "^[а-яА-Я]+$"
    tokens = set()
    analyzer = pymorphy2.MorphAnalyzer()

    # итерация по всем файлам директории
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # проверка на тип
        if os.path.isfile(file_path):
            # токены из файла
            returned_tokens = tokenize_file(file_path)
            # удаление дубликатов путем приведения к множеству
            returned_tokens = set(returned_tokens)
            # фильтрация по заданному паттерну
            filtered_tokens = [returned_token for returned_token in returned_tokens
                               if re.match(token_pattern, returned_token)]
            tokens.update(filtered_tokens)

    with open("tokens.txt", "w+") as f_tokens:
        f_tokens.write("")

    # Сохранение списка
    with open("tokens.txt", "a") as f_tokens:
        for token in tokens:
            f_tokens.write(f'{token}\n')

    # создание словаря лемм и соответствующих им токенов
    lemmas_dict = dict()
    for token in tokens:
        parsed_token = analyzer.parse(token)[0]
        lemma = parsed_token.normal_form
        # добавление токена по ключу (лемме)
        if lemma not in lemmas_dict.keys():
            lemmas_dict[lemma] = [token]
        else:
            lemmas_dict[lemma].append(token)

    # сохранение словаря
    with open('lemmas.txt', encoding='cp1251', mode='w') as f_lemmas:
        for key, values in lemmas_dict.items():
            f_lemmas.write(f'{key}: {" ".join(values)}\n')
