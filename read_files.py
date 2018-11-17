import os
import re
from collections import Counter
import pandas as pd

regex_words = r"\w[\w']*"
regex_sentence = r'[^.?!]*(?<=[.?\s!,])%s(?=[\s,.?!])[^.?!]*[.?!]'

#regex_sentence = r'([^.]*\b%s\b[^.]*)'


def read_files(document):
    with open(document, 'r') as input_file:
        data = input_file.read().replace('\n', '').lower()
    words = re.findall(regex_words, data)  # This finds words in the document
    return {'document': document, 'words': words, 'data': data}


def most_common(word_list):
    word_count = Counter(word_list)

    print(word_count.most_common(10))
    print(word_count)
    return word_count


def build_dictionary(word_list, count):
    # TODO: EXACT MATCHES ONLY
    for key, value in count.items():
        values = dict()
        values['word'] = key
        values['count'] = value
        sentences = []
        temp = ''
        for docs in word_list:
            if key in docs['words']:
                temp = temp + ',' + docs['document'].replace(directory + '/', '')
                sentences.extend(re.findall(regex_sentence % key, docs['data']))
        values['documents'] = temp.lstrip(',')
        values['sentences'] = sentences
        print(values)


if __name__ == '__main__':
    directory = 'test_docs'
    words = []
    word_list = []

    final_list = []
    for document in os.listdir(directory):
        doc = read_files(directory + '/' + document)
        words.extend(doc['words'])
        word_list.append(doc)
    count = most_common(words)

    values = build_dictionary(word_list, count)

    # print(pd.DataFrame(values))
