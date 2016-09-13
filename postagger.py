import codecs
import os

import sys

from character_tagging import character_tagging
from compute_maxent import load_data, generate_test, test_maxent, save_label
from feature_extract import feature_extract, gather_feature
from pos2word import character_2_word
from test_split import character_split


def main():
    # process msr_training file
    print('reading msr_training file ...')
    input_file = "icwb2-data\\training\msr_training1.utf8"
    output_file = ".\output\\train_tagging.txt"

    if not os.path.exists('.\output'):
        os.mkdir('.\output')
    character_tagging(input_file, output_file)
    # extract feature
    print('extract feature ...')
    with codecs.open('output\\train_tagging.txt', 'r', 'utf-8') as f:
        feature_extract(f, gather_feature)

    # split test file
    print('split test file ...')
    input_file = "icwb2-data\\testing\msr_test2.utf8"
    output_file = ".\output\\test_tagging.txt"
    character_split(input_file, output_file)
    # compute maxent
    print('compute maxent ...')
    train = load_data('output\context.txt')
    file_test = codecs.open('output\\test_tagging.txt', 'r', 'utf-8')
    # predict label
    print('predict label')
    test = generate_test(file_test)
    label = test_maxent('IIS', test, train)
    save_label(label)

    input_file = 'output/pos_tagging.txt'
    output_file = 'output/result.txt'
    character_2_word(input_file, output_file)
    print('\nfinish')
    sys.exit(0)


if __name__ == '__main__':
    main()
