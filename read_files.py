import os
import re
from collections import Counter
import pandas as pd
from operator import itemgetter

regex_words = r"\w[\w']*"
regex_sentence = r'[^.?!]*(?<=[.?\s!,])%s(?=[\s,.?!])[^.?!]*[.?!]'

yes = {'yes', 'y', 'ye'}
articles = ['a', 'about', 'above', 'across', 'after', 'against', 'all', 'along', 'among', 'around', 'an', 'and', 'are',
            'as', 'at', 'be', 'between', 'because', 'been', 'before', 'behind', 'below', 'beneath', 'beside', 'between',
            'beyond', 'but', 'by', 'concerning', 'can', 'despite', 'down', 'during', 'except', 'excepting',
            'for', 'from', 'i', 'if', 'in', 'inside', 'instead', 'into', 'it', 'is', 'like', 'my', 'mine', 'me', 'near',
            'not', 'nor', 'has', 'have', 'he', 'here', 'hers', 'his', 'of', 'off', 'on', 'onto', 'out', 'outside',
            'our', 'ours', 'or', 'over', 'past', 'regarding', 'since', 'so', 'she', 'than', 'that', 'this',
            'then', 'the', 'they', 'their', 'theirs', 'there',
            'these', 'through', 'throughout', 'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon', 'us', 'was',
            'we', 'what', 'who', 'when', 'where', 'why', 'will', 'with', 'within', 'without' 'would', 'you', 'your'
            ]


# regex_sentence = r'([^.]*\b%s\b[^.]*)'


def read_files(document):
    with open(document, 'r') as input_file:
        data = input_file.read().replace('\n', '').lower()
    words = re.findall(regex_words, data)  # This finds words in the document

    data = re.split(r' *[\.\?!][\'"\)\]]* *', data)
    return {'document': document, 'words': words, 'data': data}


def most_common(word_list, flag):
    word_count = Counter(word_list)

    print(word_count.most_common(10))

    if not flag:
        for item in articles:
            word_count.pop(item, None)

    return word_count


def build_dictionary(word_list, count):
    # TODO: EXACT MATCHES ONLY
    entities = []
    for key, value in count.items():
        values = dict()
        values['word'] = key
        values['count'] = value
        sentences = []
        temp = ''
        for docs in word_list:
            if key in docs['words']:
                temp = temp + ',' + docs['document'].replace(directory + '/', '')
                sentences.extend(
                    s for s in docs['data'] if
                    ' ' + key + ' ' in s or ' ' + key + ',' in s or s.endswith(' ' + key) or s.startswith(key + ' '))
                # split = docs['data'].split('.')
                # sentences.extend(re.findall(regex_sentence % key, docs['data']))
        values['documents'] = temp.lstrip(',')
        values['sentences'] = sentences
        entities.append(values)

    return sorted(entities, key=itemgetter('count'), reverse=True)


def print_table(list):
    print("{:<10} {:<15} {:<10}".format('Word (#)', 'Documents', 'Sentences'))

    for key in list:
        print("{:<10} {:<15} {:<10}".format(key['word'] + ' (' + str(key['count']) + ')', key['documents'], '\t\n'.join(key['sentences'])))
        print("\n")

if __name__ == '__main__':
    directory = 'test_docs'
    words = []
    word_list = []

    choice = input('Would you like to include articles, pronouns, and prepositions in your search? (y/n)').lower()
    if choice in yes:
        flag = True
    else:
        flag = False

    for document in os.listdir(directory):
        doc = read_files(directory + '/' + document)
        words.extend(doc['words'])
        word_list.append(doc)
    count = most_common(words, flag)

    values = build_dictionary(word_list, count)

    # print_table(values)

    # printTable(values, sep='\n')

    # print(pd.DataFrame(values))

    df=pd.DataFrame.from_dict(values)
    print(df[['word', 'count', 'documents', 'sentences']])
