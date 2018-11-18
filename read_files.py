import os
import re
from collections import Counter
import pandas as pd
from operator import itemgetter

regex_words = r"\w[\w']*"
regex_sentence = r'[^.?!]*(?<=[.?\s!,])%s(?=[\s,.?!])[^.?!]*[.?!]'

yes = {'yes', 'y', 'ye', ''}
no = {'no', 'n'}


# regex_sentence = r'([^.]*\b%s\b[^.]*)'


def read_files(document):
    with open(document, 'r') as input_file:
        data = input_file.read().replace('\n', '').lower()
    words = re.findall(regex_words, data)  # This finds words in the document

    data = re.split(r' *[\.\?!][\'"\)\]]* *', data)
    return {'document': document, 'words': words, 'data': data}


def most_common(word_list):
    word_count = Counter(word_list)

    print(word_count.most_common(10))
    return word_count


def build_dictionary(word_list, count):
    # TODO: EXACT MATCHES ONLY
    entities = []
    for key, value in count.items():
        values = dict()
        values['word'] = key
        values['count'] = value
        sentences = ''
        temp = ''
        for docs in word_list:
            if key in docs['words']:
                temp = temp + ',' + docs['document'].replace(directory + '/', '')
                sentences = sentences + ','.join(s for s in docs['data'] if key in s)
                # split = docs['data'].split('.')
                # sentences.extend(re.findall(regex_sentence % key, docs['data']))
        values['documents'] = temp.lstrip(',')
        values['sentences'] = sentences
        entities.append(values)

    return entities


def print_table(list):
    print("{:<8} {:<15} {:<10}".format('Word', 'Count', 'Documents'))

    list = sorted(list, key=itemgetter('count'), reverse=True)

    print(list[0])
    # for key in list:
    #     print(key)


if __name__ == '__main__':
    directory = 'test_docs'
    words = []
    word_list = []

    choice = input('Would you like to include articles in your search? (y/n)').lower()
    if choice in yes:
        flag = True
    else:
        flag = False

    for document in os.listdir(directory):
        doc = read_files(directory + '/' + document)
        words.extend(doc['words'])
        word_list.append(doc)
    count = most_common(words)

    values = build_dictionary(word_list, count)

    print_table(values)
    # print(pd.DataFrame(values))
