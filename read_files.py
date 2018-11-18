"""
 Laura Macaluso -- lauramacaluso1@gmail.com

 Programming challenge for Eigen Technologies.

 In the attached documents, find the most common occurring words, and the sentences where they are used to create the following table:

 The output is written to the screen as a pandas dataframe and also a CSV file.
"""

import os
import re
from collections import Counter
import pandas as pd
from operator import itemgetter
import csv

regex_words = r"\w[\w']*"

yes = {'yes', 'y', 'ye', 'yea'}

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


def read_files(document):
    """
    Read the given document and parse out all the words in the file into a list of words.

    :param document: The name of the document to open and read
    :return: Return a dictionary containing the document name, the list of words, and the full text
    """

    with open(document, 'r') as input_file:
        data = input_file.read().replace('\n', '').lower()
    words = re.findall(regex_words, data)  # This finds words in the document

    data = re.split(r' *[\.\?!][\'"\)\]]* *', data)
    return {'document': document, 'words': words, 'data': data}


def most_common(word_list, flag):
    """
    Given a list of words, count how many times each word appears.

    :param word_list: A list of all the words in the given texts.
    :param flag: Boolean flag that deepicts whether or not to include articles, prepositions, etc in result
    :return: A dictionary containing each word and the number of times it appears
    """
    word_count = Counter(word_list)

    if not flag:
        for item in articles:
            word_count.pop(item, None)

    return word_count


def build_dictionary(word_list, count):
    """
    Create the final output dictionary that will have each word, the number of times the word appears in the text,
    each document the word appears in, and each sentence that contains the word.

    :param word_list: A list of dictionaries that contain the document, list of words, and the text
    :param count: A dictionary containing each word and the number of times it appears
    :return: A sorted list of dictionaries containing the word, count, documents the word appears in, and each sentence
    with the word.
    """
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
        values['documents'] = temp.lstrip(',')
        values['sentences'] = sentences
        entities.append(values)

    return sorted(entities, key=itemgetter('count'), reverse=True)


def print_dataframe(list):
    """
    Print the word, count, documents, and sentences to the screen using the pandas dataframs

    :param list: A sorted list of dictionaries containing the word, count, documents the word appears in, and each sentence
    with the word.
    """
    df = pd.DataFrame.from_dict(list)
    print(df[['word', 'count', 'documents', 'sentences']])


def write_to_csv(list):
    """
    Write the list of words to a csv file separating the list into columns by their keys. This csv file will be located
    in the current directory under the name output.csv.

    :param list: A sorted list of dictionaries containing the word, count, documents the word appears in, and each sentence
    with the word.
    """
    keys = list[0].keys()
    for values in list:
        values['sentences'] = '\n'.join(values['sentences'])
    with open('output.csv', 'w') as output_file:
        writer = csv.DictWriter(output_file, keys)
        writer.writeheader()
        writer.writerows(list)


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

    print_dataframe(values)
    write_to_csv(values)
